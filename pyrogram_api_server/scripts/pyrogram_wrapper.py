from pyrogram import Client, filters
from pathlib import Path
import os.path
import pyrogram.types as types

def class PyroWrap:
    def __init__(self, api_id, api_hash, workdir):
        self.workdir = workdir
        self.api_ip = api_id
        slef.api_hash = api_hash

    def create_client(account_name, phone_number):
        client = Client(account_name, api_id = self.api_id, api_hash = self.api_hash, workdir)

    def send_private_message(phone_number, message):
        if !is_authenticated(phone_number):
            return
        client = Client(phone_number)
        client.start()
        client.send_message("me", message)
        client.stop()

    def send_code(self, phone_number):
        if !is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = Client(phone_number)
        client.start()
        code = ""

        try:
            code = client.send_code(phone_number)
        except:
            client.stop()
            raise Exception("Invalid phone number")

        client.stop()
        return code

    def signin(self, phone_number, phone_code_hash, phone_code):
        if !is_authenticated(phone_number):
            raise Exception("Invalid phone number, not authenticated")
        client = Client(phone_number)
        client.start()

        try:
            result = client.signin(phone_number, phone_code_hash, phone_code)
        except:
            client.stop()
            raise Exception("Ivalid arguments or password needed")

            if type(result) is types.TermsOfService:
                client.stop()
                raise Exception("Ivalid arguments or password needed") #temporary, assume every number to be logged already

        client.stop()
        return result #should be of type User

    def is_authenticated(self, phone_number):
        phone_number = phone_number[1:] 
        session_file = Path(f"{self.workdir}/{phone_number}.session")
        return session_file.exists()