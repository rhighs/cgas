from pyrogram import Client, filters
from pathlib import Path
import os.path
import pyrogram.types as types

class PyroWrap:
    def __init__(self, api_id, api_hash, workdir, createNow=False):
        self.workdir = workdir
        self.api_id = api_id
        self.api_hash = api_hash
        if(createNow):
            try:
                self.client = Client("pyrogram_api_server")
            except:
                raise Exception("Failed creating client, invalid id or api hash")

    def create_client(self, account_name):
        self.client = Client(account_name)
        self.client.api_id = self.api_id
        self.client.api_hash = self.api_hash
        self.client.workdir = self.workdir

    def send_private_message(self, phone_number, message):
        if self.is_authenticated(phone_number) == False:
            return
        self.client = Client(phone_number)
        self.client.start()
        self.client.send_message("me", message)
        self.client.stop()

    def send_code(self, phone_number):
        if self.is_authenticated(phone_number) == False:
            raise Exception("Invalid phone number, not authenticated")
        client = Client(phone_number)
        client.start()
        code = ""

        try:
            code = client.send_code(phone_number)
        except:
            client.stop()
            return False

        client.stop()
        return code

    def signin(self, phone_number, phone_code_hash, phone_code):
        if self.is_authenticated(phone_number) == False:
            raise Exception("Invalid phone number, not authenticated")
        client = Client(phone_number)
        client.start()

        try:
            result = client.signin(phone_number, phone_code_hash, phone_code)
        except:
            client.stop()
            return False

        if type(result) is types.TermsOfService:
            client.stop()
            return False

        client.stop()
        return result #should be of type User

    def is_authenticated(self, phone_number):
        phone_number = phone_number[1:] 
        session_file = Path(f"{self.workdir}/{phone_number}.session")
        return session_file.exists()
