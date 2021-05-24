from pyrogram import Client, filters
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

api_id= 5558646
api_hash = "30d3b4c9958fd165911d09254124d3bc"

pyro_server = Client("my_account", api_id, api_hash)

def index(request):
    pyro_server.start()
    pyro_server.send_photo("me", "here.png")
    pyro_server.stop()
    return Response("message sent!")

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_view(index, route_name="index")
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
