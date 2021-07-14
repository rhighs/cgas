from telethon                       import TelegramClient
from io                             import BytesIO
from .parser                        import parse_message
from cloudygram_api_server.models   import TtModels
from telethon.tl.types.auth         import SentCode
from telethon.tl                    import functions, types
from telethon.tl.types              import MessageMediaDocument, DocumentAttributeFilename, User, InputPeerChat, InputUserSelf
import pyramid.httpexceptions       as exc
import os

class TtWrap:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.test_msg = None

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
        result: MessageMediaDocument = await client(functions.messages.UploadMediaRequest(
            peer = me,
            media = types.InputMediaUploadedDocument(
                file=uploaded_file,
                stickers=[types.InputDocument(
                    id=uploaded_file.id,
                    access_hash=uploaded_file.id,
                    file_reference=b'a\x7ffile\xfareference'
                )],
                ttl_seconds=100,
                mime_type=mime_type,
                attributes=[
                    DocumentAttributeFilename(file_name)
                    ]
            )
        ))
        await client.disconnect()
        return result.to_json()

    async def download_file(self, phone_number, message_json, path):
        client = self.create_client(phone_number)
        m = parse_message(message_json)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise exc.HTTPUnauthorized()
        if path is not None:
            await client.download_media(m, path)
        else:
            await client.download_media(m)
        await client.disconnect() 
        return m

    async def download_profile_photo(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            client.disconnect()
            raise exc.HTTPUnauthorized()
        path = await client.download_profile_photo("me")
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
