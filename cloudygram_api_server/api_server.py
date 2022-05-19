from distutils.log import debug
import imp
from cloudygram_api_server.controllers import HomeController, UserController, MessagesController
from cloudygram_api_server.telethon.telethon_wrapper import init_telethon
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from telethon import __version__

def configure(**settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_handlers')
        config.add_handler("home", "/{action}", handler=HomeController)
        config.add_handler("user", "/user/{phoneNumber}/{action}", handler=UserController)
        config.add_handler("messages", "/user/{phoneNumber}/messages/{action}", handler=MessagesController)
        config.scan()
    return config.make_wsgi_app()

class ApiServer:
    def __init__(self, api_id, api_hash, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        init_telethon(api_id, api_hash)
    
    def run(self):
        pyramid_app = configure(settings=None)
        with make_server(self.host_ip, self.port, app=pyramid_app) as server:
            print("Server start...")
            print("Version " + __version__)
            server.serve_forever()
