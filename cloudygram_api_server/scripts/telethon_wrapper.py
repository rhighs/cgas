from telethon                       import TelegramClient
from pathlib                        import Path
from pyrogram                       import types
from os                             import path
from cloudygram_api_server.models   import TtModels

class TtWrap:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash

    def create_client(self, phone_number):
        return TelegramClient(api_id=self.api_id, api_hash=self.api_hash, session=phone_number)

    def send_private_message(self, phone_number, message):
        if not self.is_authenticated(phone_number):
            return
        client = self.create_client(phone_number) 
        client.connect()
        client.send_message("me", message)
        client.disconnect()

    def create_session(self, phone_number):
        client = self.create_client(phone_number)
        client.connect()
        client.disconnect()

    def send_code(self, phone_number):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.create_client(phone_number) 
        client.connect()
        try:
            code = client.send_code_request(phone_number)
        except Exception as e :
            client.disconnect()
            return TtModels.send_code_failure(str(e))
        client.disconnect()
            
        return code.phone_code_hash

    def signin(self, phone_number, phone_code_hash, phone_code):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.create_client(phone_number)
        client.connect()
        try:
            result: types.SentCode = client.sign_in(phone=phone_number, phone_code_hash=phone_code_hash, code=phone_code)
        except Exception as e:
            client.disconnect()
            return TtModels.sing_in_failure(str(e))
        if type(result) is types.TermsOfService:
            client.disconnect()
            return TtModels.sing_in_failure("Requires terms of service acceptance")
        client.disconnect()
        return result #of type User

    def get_me(self, phone_number):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.create_client(phone_number)
        client.connect()
        result = client.get_me()
        client.disconnect()
        return result

    def upload_file(self, phone_number, file_path):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.create_client(phone_number)
        client.connect()
        result = client.upload_file(file=None)
        client.disconnect()
        return result

    def is_authenticated(self, phone_number):
        return True
        session_file = Path(f"{self.workdir}/{phone_number}.session")
        return session_file.exists()
