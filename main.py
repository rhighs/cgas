import sys
import json
from os import path
import uvicorn
from cloudygram_api_server.controllers.messages_controller import MessagesController
from cloudygram_api_server.telethon.telethon_wrapper import init_telethon
from fastapi import FastAPI
from cloudygram_api_server.controllers import HomeController, UserController
from telethon import __version__

PATH = "keys.json"

app = FastAPI()

app.include_router(
    HomeController.router,
    prefix="",
    tags=["Home"],
)

app.include_router(
    UserController.router,
    prefix="/user",
    tags=["User"],
)

app.include_router(
    MessagesController.router,
    prefix="/user/messages",
    tags=["Messages"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/version")
def version():
    return {"version": __version__}

def startup():
    if path.exists(PATH):
        with open(PATH, "r") as f:
            data = json.load(f)
    else:
        print("File keys.json: You must insert api_id!")
        exit(1)

    init_telethon(data["api_id"], data["api_hash"])

if __name__ == "__main__":
    startup()
    uvicorn.run("__main__:app", host="0.0.0.0", port=5000)
