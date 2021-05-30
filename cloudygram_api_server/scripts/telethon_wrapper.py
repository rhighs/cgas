from telethon                       import TelegramClient
from pathlib                        import Path
from pyrogram                       import types
from os                             import path
from cloudygram_api_server.models   import TtModels
from telethon.tl.types.auth         import SentCode
from telethon.utils import get_input_location
from telethon.tl.types import Document

class TtWrap:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash

    def create_client(self, phone_number):
        return TelegramClient(api_id=self.api_id, api_hash=self.api_hash, session=phone_number)

    def send_private_message(self, phone_number, message):
        client = self.create_client(phone_number) 
        client.connect()
        if not client.is_user_authorized():
            return
        client.send_message("me", message)
        client.disconnect()

    def create_session(self, phone_number):
        client = self.create_client(phone_number)
        client.connect()
        client.disconnect()

    async def send_code(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        if not client.is_user_authorized():
            raise Exception("Invalid phone number, not authenticated")
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
        if not client.is_user_authorized():
            raise Exception("Invalid phone number, not authenticated")
        try:
            result: types.SentCode = await client.sign_in(phone=phone_number, phone_code_hash=phone_code_hash, code=phone_code)
        except Exception as e:
            await client.disconnect()
            return TtModels.sing_in_failure(str(e))
        if type(result) is types.TermsOfService:
            await client.disconnect()
            return TtModels.sing_in_failure("Requires terms of service acceptance")
        await client.disconnect()
        return result #of type User

    async def get_me(self, phone_number):
        client = self.create_client(phone_number)
        await client.connect()
        if not client.is_user_authorized():
            raise Exception("Invalid phone number, not authenticated")
        result = await client.get_me()
        await client.disconnect()
        return result

    async def upload_file(self, phone_number, file_stream):
        client = self.create_client(phone_number)
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            raise Exception("Invalid phone number, not authenticated")
        result = await client.upload_file(file=file_stream)
        print(f"uploaded file for {phone_number} with id: {result.id} and md5 {result.md5_checksum} and parts {result.parts}")
        await client.disconnect()

    async def download_file(self, phone_number, file_id):
        client = self.create_client(phone_number)
        await client.connect()
        doc = Document(id=-8114692116561779292, access_hash=0, date=None, file_reference="", mime_type="text/plain", size=20, dc_id=1, attributes=[])
        dc_id, loc  = get_input_location(doc)
        if not await client.is_user_authorized():
            await client.disconnect()
            raise Exception("Invalid phone number, not authenticated")
        await client.download_file(loc)
        await client.disconnect() 
