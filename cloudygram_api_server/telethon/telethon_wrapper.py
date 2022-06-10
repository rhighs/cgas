from email.mime import base
from gc import callbacks
import imp

from attr import attr
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse
from cloudygram_api_server.telethon.exceptions import TTUnathorizedException, TTGenericException, TTSignInException, TTFileTransferException
from telethon.tl.types import Message, MessageMediaDocument, DocumentAttributeFilename, UpdateShortMessage
from telethon.tl.types import User, InputPeerChat, InputUserSelf, PeerChat, PeerChannel, InputPeerUser
from telethon.tl.types.messages import AffectedMessages
import telethon.tl.custom
from telethon.tl.types.auth import SentCode
from telethon.tl import functions, types
from telethon import TelegramClient
from .parser import parse_updates, get_message_id, with_new_ref
from typing import List, Tuple
from pathlib import Path
from io import BytesIO
import os
#from cloudygram_api_server.scripts.utilities import Progress
import traceback
import sys

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
        self.client = TelegramClient(self.workdir, API_ID, API_HASH)

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


async def signin(phone_number: str, phone_code_hash: str, phone_code: str, phone_password: str) -> User:
    async with Client(phone_number, check_auth=False) as client:
        try:
            result: User = await client.sign_in(phone_number, phone_code, phone_code_hash=phone_code_hash)
        except Exception as e:
            message = TTSignInException(str(e))
            try:
                if (message.args[0] == "Two-steps verification is enabled and a password is required (caused by SignInRequest)"):
                    result: User = await client.sign_in(phone_number, password=phone_password)
                else:
                    raise TTSignInException(str(e))
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


async def upload_file(phone_number: str, file_name: str, file_stream: BytesIO, mime_type: str, chatid: int = 0):
    async with Client(phone_number) as client:
        if (chatid == 0):
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
        else:
            try:
                updates: telethon.tl.custom.message.Message = await client.send_file(entity = int(chatid), 
                        file=file_stream, 
                        attributes=[DocumentAttributeFilename(file_name)],
                        progress_callback=Progress.callbackUpload)
            except Exception as e:
                traceback.print_exc()
                raise TTFileTransferException(str(e))

    return updates.to_json()

async def download_file(phone_number: str, message: Message, chatid: int, file_path: str) -> CgDownloadResult:
    path = None
    async with Client(phone_number) as client:
        async def try_download():
            message_to_download: Message = await client.get_messages(chatid, ids=message.id)
            if (message_to_download is None):
                raise ValueError('Message not found')

            for attribute in message_to_download.media.document.attributes:
                if isinstance(attribute, DocumentAttributeFilename):
                    file_name = attribute.file_name
                    break
            
            path = os.path.join(file_path, file_name)
            await message_to_download.download_media(path)
        try:
            await try_download()
        except Exception as exc:  # file ref exception, dont care about getting the type
            return BaseResponse(isSuccess=False, message=str(exc))
        return BaseResponse(isSuccess=True, message=path)

async def download_profile_photo(phone_number: str, filepath: str = None, filename: str = None) -> BaseResponse:
    async with Client(phone_number) as client:
        me: User = await client.get_me()
        if filepath != None and filename is None:
            filepath += me.username
        elif filepath != None and filename is not None:
            filepath += filename
        elif filepath is None:
            filepath = os.path.join(os.getcwd(), me.username + '.jpg')

        if os.path.exists(filepath): #this helps avoiding duplicate files
            os.remove(filepath)
        download_path = await client.download_profile_photo(InputUserSelf(), file=filepath)
    return BaseResponse(isSuccess=download_path == filepath, message=download_path)

async def get_messages(phone_number: str) -> List:
    async with Client(phone_number) as client:
        result = await client.iter_messages(InputUserSelf(), None)
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

async def upload_file_path(phone_number: str, file_name: str, file_stream: str, mime_type: str):
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

async def get_dialog(phone_number: str) -> dict:
    async with Client(phone_number) as client:
        if (await client.get_me()).bot:
            await client.disconnect()
            raise TTUnathorizedException()
        result = []
        async for dialog in client.iter_dialogs(archived=False):
            result.append({'id': dialog.id, 'title': dialog.title})
    return result
