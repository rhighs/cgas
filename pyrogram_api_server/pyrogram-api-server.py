from pyrogram import Client, filters
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from .pyro_wrapper import PyroWrap
from . import main
import json

with open("keys.json", "r") as myfile:
    data=myfile.read()

obj = json.loads(data)
api_id = obj["api_id"]
api_hash = str(obj["api_hash"])

pyro = PyroWrap(api_id, api_hash, workdir="./sessions")

pyro_client = Client("my_account", api_id, api_hash)

@view_config(route_name='index', renderer='json')
def index(request):
    return { "isSuccess" : True }

@view_config(route_name='values', renderer='json')
def values(request):
    return { "message" : [1,2,3,4,5] }

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_route('values', '/values')
        config.scan()
        app = config.make_wsgi_app()
    app = main(settings=None)
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
