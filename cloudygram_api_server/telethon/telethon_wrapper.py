from cloudygram_api_server.telethon.exceptions import TTNeeds2FAException, TTUnathorizedException, TTGenericException, TTSignInException, TTFileTransferException
from telethon.tl.types import Message, MessageMediaDocument, DocumentAttributeFilename, UpdateShortMessage
from telethon.tl.types import User, InputPeerChat, InputUserSelf
from telethon.tl.types.messages import AffectedMessages
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types.auth import SentCode
from telethon.tl import functions, types
from telethon import TelegramClient
from .parser import parse_updates, get_message_id, with_new_ref
from typing import List, Tuple, Optional
from pathlib import Path
from io import BytesIO
import os

WORKDIR = ""
API_ID = ""
API_HASH = ""
INITIAL_FILE_REF: bytes = b'initialfilereference'


def init_telethon(api_id: str, api_hash: str, workdir: str = "sessions"):
    global WORKDIR, API_ID, API_HASH
    API_ID = api_id
    API_HASH = api_hash
    WORKDIR = os.path.join(os.getcwd(), workdir)


class CgDownloadResult():

    def __init__(self, message_json, has_ref_changed):
        if has_ref_changed:
            self.message_id = get_message_id(message_json)
        self.message_json = message_json
        self.has_ref_changed = has_ref_changed

    def dict(self):
        if self.has_ref_changed:
            return { "messageId": self.message_id, "hasRefChanged": self.has_ref_changed, "message": self.message_json }
        return { "hasRefChanged": self.has_ref_changed, "message": self.message_json }


class Client:

    def __init__(self, phone_number: str, check_auth: bool = True):
        self.workdir = WORKDIR + "/" + phone_number
        self.phone_number = phone_number
        self.check_auth = check_auth
        self.client = TelegramClient(api_id=API_ID, api_hash=API_HASH, session=self.workdir)

    async def __aenter__(self):
        await self.client.connect()
        if (await self.client.is_user_authorized()) or not self.check_auth:
            return self.client
        else:
            raise TTUnathorizedException()

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.disconnect()


async def clean():
    sessions = os.listdir(WORKDIR)
    files = [file for file in sessions if os.path.isfile(
        os.path.join(WORKDIR, file))]
    for file in files:
        session_name = Path(file).stem
        if not session_valid(session_name):
            os.remove(WORKDIR + "/" + file)


async def session_valid(phone_number: str) -> bool:
    async with Client(phone_number) as client:
        result = await client.get_me()
    return result is not None


async def is_authorized(phone_number: str) -> bool:
    async with Client(phone_number) as client:
        me: User = await client.get_me()
        authorized = await client.is_user_authorized()
    return authorized and (me is not None)


async def send_private_message(phone_number: str, message: Message):
    async with Client(phone_number) as client:
        await client.send_message(InputUserSelf(), message)


async def send_code(phone_number: str) -> str:
    async with Client(phone_number, check_auth=False) as client:
        try:
            code: SentCode = await client.send_code_request(phone_number)
        except Exception as e:
            raise TTGenericException(str(e))
    return code.phone_code_hash


async def signin(phone_number: str, phone_code_hash: str, phone_code: str, password: Optional[str] = None) -> User:
    async with Client(phone_number, check_auth=False) as client:
        try:
            result: User = await client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash, password=password)
        except SessionPasswordNeededError:
            raise TTNeeds2FAException()
        except Exception as e:
            raise TTSignInException(str(e))
    return result  #of type User


async def signup(phone_number: str, code: str, phone_code_hash: str,
                 first_name: str, last_name: str, phone: str = None) -> User:
    async with Client(phone_number, check_auth=False) as client:
        try:
            result: User = await client.sign_up(
                code=code,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                phone_code_hash=phone_code_hash
            )
        except Exception as e:
            raise TTSignInException(str(e))
    return result


async def qr_login(phone_number: str):
    async with Client(phone_number, check_auth=False) as client:
        result = await client.qr_login()
    return result


async def logout(phone_number: str) -> bool:
    async with Client(phone_number) as client:
        result: bool = await client.log_out()
    return result


async def get_me(phone_number: str) -> User:
    async with Client(phone_number) as client:
        result: User = await client.get_me()
    return result


async def upload_file(phone_number: str, file_name: str, file_stream: BytesIO, mime_type: str):
    async with Client(phone_number) as client:
        uploaded_file = await client.upload_file(file=file_stream)
        me: User = await client.get_me()
        media = types.InputMediaUploadedDocument(
            file=uploaded_file,
            stickers=[types.InputDocument(
                id=uploaded_file.id,
                access_hash=uploaded_file.id,
                file_reference=INITIAL_FILE_REF
            )],
            ttl_seconds=100,
            mime_type=mime_type,
            attributes=[
                DocumentAttributeFilename(file_name)
            ]
        )

        try:
            updates: UpdateShortMessage = await client(functions.messages.SendMediaRequest(
                peer=me,
                media=media,
                message="document id: " + str(media.stickers[0].id)
            ))
        except Exception as e:
            raise TTFileTransferException(str(e))
    return updates.to_json()


async def download_file(phone_number: str, message_json: str, file_path: str) -> CgDownloadResult:
    async with Client(phone_number) as client:
        media: MessageMediaDocument = parse_updates(message_json)
        message_id = get_message_id(message_json)

        async def try_download():
            if file_path is not None:
                await client.download_media(media, file_path)
            else:
                await client.download_media(media)
        try:
            await try_download()
        except:  # file ref exception, dont care about getting the type
            ref: bytes = await file_refresh(client, message_id)
            media.document.file_reference = ref
            await try_download()
            return CgDownloadResult(with_new_ref(message_json, ref), True)
        return CgDownloadResult(message_json, False)


async def download_profile_photo(phone_number: str, filepath: str = None, filename: str = None) -> bool:
    async with Client(phone_number) as client:
        me: User = await client.get_me()
        if filepath != None and filename is None:
            filepath += me.username
        elif filepath != None and filename is not None:
            filepath += filename
        if os.path.exists(filepath): #this helps avoiding duplicate files
            os.remove(filepath)
        download_path = await client.download_profile_photo(InputUserSelf(), file=filepath)
    return download_path == filepath


async def get_messages(phone_number: str) -> List:
    async with Client(phone_number) as client:
        result = await client.get_messages(InputUserSelf(), None)
    return result


async def delete_messages(phone_number: str, message_ids: List[str], chat_id: str = None) -> AffectedMessages:
    entity = InputPeerChat(chat_id) if chat_id else InputUserSelf()
    async with Client(phone_number) as client:
        result: AffectedMessages = await client.delete_messages(entity, message_ids)
    return result


async def get_contacts(phone_number: str) -> str:
    async with Client(phone_number) as client:
        if (await client.get_me()).bot:
            await client.disconnect()
            raise TTUnathorizedException()
        result = await client(functions.contacts.GetContactsRequest(
            hash=0
        ))
    return result.stringify()


async def file_refresh(client_instance: TelegramClient, message_id: int) -> bytes:
    async for m in client_instance.iter_messages(InputUserSelf(), ids=message_id):
        return m.media.document.file_reference

