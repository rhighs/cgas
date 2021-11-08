from cloudygram_api_server.telethon.exceptions import TTUnathorizedException, TTGenericException, TTSignInException, TTFileTransferException
from cloudygram_api_server.models import TtModels
from telethon.tl.types import Message, MessageMediaDocument, DocumentAttributeFilename, UpdateShortMessage
from telethon.tl.types import User, InputPeerChat, InputUserSelf
from telethon.tl.types.messages import AffectedMessages
from telethon.tl.types.auth import SentCode
from telethon.tl import functions, types
from telethon import TelegramClient
from .parser import parse_updates, get_message_id, with_new_ref
from typing import List, Tuple
from pathlib import Path
from io import BytesIO
import os

class TtWrap:

    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.initial_ref = b'initialfilereference'
        self.workdir = os.path.join(os.getcwd(), "sessions")

    async def connect(self, phone_number: str) -> TelegramClient:
        client = self.create_client(phone_number)
        await client.connect()
        if (await client.is_user_authorized()):
            return client
        else:
            raise TTUnathorizedException()

    def create_client(self, phone_number: str) -> TelegramClient:
        workdir = self.workdir + "/" + phone_number
        return TelegramClient(api_id=self.api_id, api_hash=self.api_hash, session=workdir)
    
    async def clean(self):
        sessions = os.listdir(self.workdir)
        files = [file for file in sessions if os.path.isfile(os.path.join(self.workdir, file))]
        for file in files:
            session_name = Path(file).stem
            if not self.session_valid(session_name):
                os.remove(self.workdir + "/" + file)

    async def session_valid(self, phone_number: str) -> bool:
        client = self.create_client(phone_number)
        await client.connect()
        result = await client.get_me()
        await client.disconnect()
        return result is not None

    async def is_authorized(self, phone_number: str) -> bool:
        client: TelegramClient = self.create_client(phone_number)
        await client.connect()
        me: User = await client.get_me()
        authorized = await client.is_user_authorized()
        await client.disconnect()
        return authorized and (me is not None)

    async def send_private_message(self, phone_number: str, message: Message):
        client: TelegramClient = await self.connect(phone_number) 
        await client.send_message(InputUserSelf(), message)
        await client.disconnect()

    async def create_session(self, phone_number):
        client: TelegramClient = self.create_client(phone_number)
        await client.disconnect()

    async def send_code(self, phone_number: str) -> str:
        client: TelegramClient = self.create_client(phone_number)
        await client.connect()
        try:
            code: SentCode = await client.send_code_request(phone_number)
        except Exception as e:
            await client.disconnect()
            raise TTGenericException(str(e))
        await client.disconnect()
        return code.phone_code_hash

    async def signin(self, phone_number: str, phone_code_hash: str, phone_code: str) -> User:
        client: TelegramClient = self.create_client(phone_number)
        await client.connect()
        try:
            result: User = await client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash)
        except Exception as e:
            await client.disconnect()
            raise TTSignInException(str(e))
        await client.disconnect()
        return result #of type User

    async def signup(self, phone_number: str, code: str, phone_code_hash: str,
            first_name: str, last_name: str, phone: str = None) -> User:
        client: TelegramClient = self.create_client(phone_number)
        try:
            result: User = await client.sign_up(
                    code=code,
                    first_name=first_name, 
                    last_name=last_name, 
                    phone=phone,
                    phone_code_hash=phone_code_hash
                    )
        except Exception as e:
            await client.disconnect()
            raise TTSignInException(str(e))
        await client.disconnect()
        return result

    async def qr_login(self, phone_number: str):
        client: TelegramClient = self.create_client(phone_number)
        await client.connect()
        result = await client.qr_login()
        await client.disconnect()
        return result

    async def logout(self, phone_number: str) -> bool:
        client: TelegramClient = await self.connect(phone_number)
        result: bool = await client.log_out()
        await client.disconnect()
        return result

    async def get_me(self, phone_number: str) -> User:
        client: TelegramClient = await self.connect(phone_number)
        result: User = await client.get_me()
        await client.disconnect()
        return result

    async def upload_file(self, phone_number: str, file_name: str, file_stream: BytesIO, mime_type: str):
        client: TelegramClient = await self.connect(phone_number)
        uploaded_file = await client.upload_file(file=file_stream)
        me: User = await client.get_me()
        media = types.InputMediaUploadedDocument(
            file=uploaded_file,
            stickers=[types.InputDocument(
                id=uploaded_file.id,
                access_hash=uploaded_file.id,
                file_reference=self.initial_ref
            )],
            ttl_seconds=100,
            mime_type=mime_type,
            attributes=[
                DocumentAttributeFilename(file_name)
                ]
        )

        try: 
            updates: UpdateShortMessage = await client(functions.messages.SendMediaRequest(
                peer = me,
                media = media,
                message = "document id: " + str(media.stickers[0].id)
                ))
        except Exception as e:
            raise TTFileTransferException(str(e))
        await client.disconnect()
        return updates.to_json()

    async def download_file(self, phone_number: str, message_json: str, file_path: str) -> Tuple[dict, bool]:
        client: TelegramClient = await self.connect(phone_number)
        media: MessageMediaDocument = parse_updates(message_json)
        message_id = get_message_id(message_json)
        async def try_download():
            if file_path is not None:
                await client.download_media(media, file_path)
            else:
                await client.download_media(media)
        try:
            await try_download()
        except: #file ref exception, dont care about getting the type
            ref: bytes = await file_refresh(client, message_id)
            media.document.file_reference = ref
            await try_download()
            await client.disconnect() 
            return True, with_new_ref(message_json, ref)
        await client.disconnect() 
        return False, message_json

    async def download_profile_photo(self, phone_number: str, file_path: str = None) -> bool:
        client: TelegramClient = await self.connect(phone_number)
        me: User = await client.get_me()
        if file_path != None:
            file_path += me.username
        if os.path.exists(file_path): #avoid duplicate files
            os.remove(file_path)
        download_path = await client.download_profile_photo(InputUserSelf(), file=file_path)
        await client.disconnect()
        return download_path == file_path

    async def get_messages(self, phone_number: str) -> List:
        client: TelegramClient = await self.connect(phone_number)
        result = await client.get_messages(InputUserSelf(), None)
        await client.disconnect()
        return result

    async def delete_messages(self, messages_id: List[str], phone_number: str, chat_id: str = None) -> AffectedMessages:
        entity = InputPeerChat(chat_id) if chat_id else InputUserSelf()
        client: TelegramClient = await self.connect(phone_number)
        result: AffectedMessages = await client.delete_messages(entity, messages_id)
        await client.disconnect()
        return result

    async def get_contacts(self, phone_number: str) -> str:
        client: TelegramClient = await self.connect(phone_number)
        if (await client.get_me()).bot:
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        result = await client(functions.contacts.GetContactsRequest(
            hash=0
        ))
        await client.disconnect()
        return result.stringify()


async def file_refresh(client_instance: TelegramClient, message_id: int) -> bytes:
    async for m in client_instance.iter_messages(InputUserSelf(), ids=message_id):
        return m.media.document.file_reference

