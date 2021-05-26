from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from . import main

PORT=5000
HOST_IP="0.0.0.0" # -> 127.0.0.1

if __name__ == '__main__':
    app = main(settings=None)
    server = make_server(HOST_IP, PORT, app)
    server.serve_forever()