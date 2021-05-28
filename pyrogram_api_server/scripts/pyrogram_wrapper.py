from pyrogram   import Client
from pathlib    import Path
from pyrogram   import types
from os         import path

class PyroWrap:
    def __init__(self, api_id, api_hash, workdir):
        self.workdir = workdir
        self.api_id = api_id
        self.api_hash = api_hash
        self.cc = lambda phone_number: Client(api_id=self.api_id, api_hash=self.api_hash, phone_number=phone_number, session_name=phone_number)

    def send_private_message(self, phone_number, message):
        if not self.is_authenticated(phone_number):
            return
        client = self.cc(phone_number) 
        client.connect()
        client.send_message("me", message)
        client.disconnect()

    def create_session(self, phone_number):
        client = self.cc(phone_number)
        client.connect()
        client.disconnect()

    def send_code(self, phone_number):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.cc(phone_number) 
        try:
            code = client.send_code(phone_number)
        except:
            client.disconnect()
            return False
        client.disconnect()
        return code

    def signin(self, phone_number, phone_code_hash, phone_code):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.cc(phone_number)
        client.connect()
        try:
            result = client.signin(phone_number, phone_code_hash, phone_code)
        except:
            client.disconnect()
            return False
        if type(result) is types.TermsOfService:
            client.disconnect()
            return False
        client.disconnect()
        return result #should be of type User

    def get_me(self, phone_number):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.cc(phone_number)
        client.connect()
        result = client.get_me()
        client.disconnect()
        return result

    def upload_file(self, phone_number, file_path):
        if not self.is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = self.cc(phone_number)
        client.connect()
        result = client.save_file(path=file_path)
        client.disconnect()
        return result

    def is_authenticated(self, phone_number):
        return True
        session_file = Path(f"{self.workdir}/{phone_number}.session")
        return session_file.exists()
