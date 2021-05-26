from .hoome_controller import HomeController
from pyrogram-api-server.scripts import PyroWrap

#instance used by controllers, any way to make this sort of private thingy?
pyro_wrap = PyroWrap(api_id=0, api_hash="", workdir="./sessions")