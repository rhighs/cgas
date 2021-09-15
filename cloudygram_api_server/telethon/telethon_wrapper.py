from telethon                       import TelegramClient
from io                             import BytesIO
from .parser                        import parse_updates, get_message_id, with_new_ref
from cloudygram_api_server.models   import TtModels
from telethon.tl.types.auth         import SentCode
from telethon.tl                    import functions, types
from telethon.tl.types              import Message, MessageMediaDocument, DocumentAttributeFilename, UpdateShortMessage
from telethon.tl.types              import User, InputPeerChat, InputUserSelf
import pyramid.httpexceptions       as exc
import os

class TtWrap:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.initial_ref = b'initialfilereference'

    def create_client(self, phone_number):
        workdir = os.path.join(os.getcwd(), "sessions", phone_number)
        return TelegramClient(api_id=self.api_id, api_hash=self.api_hash, session=workdir)
    
    async def is_authorized(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        result = await client.is_user_authorized()
        await client.disconnect()
        return result

    async def send_private_message(self, phone_number, message):
        client = self.create_client(phone_number) 
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        await client.send_message("me", message)
        await client.disconnect()

    async def create_session(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        await client.disconnect()

    async def send_code(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        try:
            code: SentCode = await client.send_code_request(phone_number)
        except Exception as e :
            await client.disconnect()
            return TtModels.send_code_failure(str(e))
        await client.disconnect()
        return code.phone_code_hash

    async def signin(self, phone_number, phone_code_hash, phone_code):
        client = self.create_client(phone_number)
        await client.connect()
        try:
            result: User = await client.sign_in(phone=phone_number, phone_code_hash=phone_code_hash, code=phone_code)
        except Exception as e:
            await client.disconnect()
            return TtModels.sing_in_failure(str(e))
        await client.disconnect()
        return result #of type User

    async def signup(self, phone_number, code, phone_code_hash, first_name, last_name, phone=None):
        client = self.create_client(phone_number)
        await client.connect()
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
            return TtModels.sing_in_failure(str(e))
        await client.disconnect()
        return result

    async def get_me(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        result = await client.get_me()
        await client.disconnect()
        return result

    async def upload_file(self, phone_number, file_name, file_stream: BytesIO, mime_type):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            client.disconnect()
            raise exc.HTTPUnauthorized()
        uploaded_file = await client.upload_file(file=file_stream)
        me = await client.get_me()
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
            print(str(e))
        await client.disconnect()
        return updates.to_json()

    async def download_file(self, phone_number, message_json, path):
        client = self.create_client(phone_number)
        media: MessageMediaDocument = parse_updates(message_json)
        message_id = get_message_id(message_json)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        async def try_download():
            if path is not None:
                await client.download_media(media, path)
            else:
                await client.download_media(media)
        try:
            await try_download()
        except Exception as e: #file ref
            ref = await file_refresh(client, message_id)
            media.document.file_reference = ref
            await try_download()
            await client.disconnect() 
            return { "hasRefChanged": True, "message" : with_new_ref(message_json, ref) }
        await client.disconnect() 
        return { "messageId": get_message_id(message_json), "hasRefChanged": False, "message": media.to_json() }

    async def download_profile_photo(self, phone_number, file_path=None):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            client.disconnect()
            raise exc.HTTPUnauthorized()
        path = await client.download_profile_photo("me", file=file_path)
        await client.disconnect()
        return path

    async def qr_login(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        result = await client.qr_login()
        await client.disconnect()
        return result

    async def logout(self, phone_number):
        client = self.create_client(phone_number)
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        await client.connect()
        result = await client.log_out()
        await client.disconnect()
        return result

    async def get_messages(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        result = await client.get_messages(InputUserSelf(), None)
        await client.disconnect()
        return result

"""
    Amongst all the private messages, find the one with the mathing document id
    then gather the file_reference and return it to the caller.
    This operation might require some time since its fetching all user messages,
    fairly enough this procedure is not called much frequently.

    Returns: bytes, None in case of no result found
"""
async def file_refresh(client_instance: TelegramClient, message_id: int) -> bytes:
    async for m in client_instance.iter_messages(InputUserSelf(), ids=message_id):
        return m.media.document.file_reference
