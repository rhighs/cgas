from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from . import main

class PGApiServer:
    def __init__(self, api_id, api_hash, host_ip, port):
        self.api_id = api_id
        self.api_hash = api_hash
        self.host_ip = host_ip
        self.port = port
    
    def run(self):
        pyramid_app = main(settings=None)
        server = make_server(self.host_ip, self.port, app=pyramid_app)
        server.serve_forever()
