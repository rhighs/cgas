from pyrogram import Client, filters
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import json

with open("keys.json", "r") as myfile:
    data=myfile.read()

obj = json.loads(data)

api_id = obj["api_id"]
api_hash = str(obj["api_hash"])

pyro_client = Client("my_account", api_id, api_hash)

def index(request):
    pyro_client.start()
    pyro_client.send_photo("me", "here.png")
    pyro_client.stop()
    return Response("message sent!")

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_view(index, route_name="index")
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
