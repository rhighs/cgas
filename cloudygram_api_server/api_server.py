from distutils.log import debug
from cloudygram_api_server.controllers import HomeController, UserController, MessagesController
from cloudygram_api_server.telethon.telethon_wrapper import init_telethon
from telethon import __version__
from typing import Union
from fastapi import FastAPI

app = FastAPI()

class ApiServer:
    def __init__(self, api_id, api_hash, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        init_telethon(api_id, api_hash)
    
    def run(self):
        app = FastAPI()
    
    @app.get("/")
    def read_root():
        return {"Hello": "World"}
