from pyrogram import Client, filters
from pathlib import Path
import os.path

def class PyroWrap:
    def __init__(self):
        return

    def create_session(account_name, api_id, api_hash, phone_number):
        client = Client(account_name, api_id, api_hash)

    def send_private_message(account_name, message):
        if !is_authenticated(account_name):
            return
        client = Client(account_name)
        client.start()
        client.send_message("me", message)
        client.stop()

    def is_authenticated(account_name):
        #save valid sessions in a db?
        session_file = Path("./" + account_name + ".session")
        return session_file.exists()