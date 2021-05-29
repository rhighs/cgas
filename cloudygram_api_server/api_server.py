from cloudygram_api_server.controllers      import HomeController
from cloudygram_api_server.controllers      import UserController
from wsgiref.simple_server                  import make_server
from pyramid.config                         import Configurator
from cloudygram_api_server.scripts          import TtWrap

tt_wrap = None

def configure(**settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_handlers')
        config.add_handler("home", "/{action}", handler=HomeController)
        config.add_handler("user", "/user/{phoneNumber}/{action}", handler=UserController)
        config.scan()
    return config.make_wsgi_app()

class ApiServer:
    def __init__(self, api_id, api_hash, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.api_id = api_id
        self.api_hash = api_hash
    
    def run(self):
        global tt_wrap
        tt_wrap = TtWrap(api_id = self.api_id, api_hash=self.api_hash)
        pyramid_app = configure(settings=None)
        server = make_server(self.host_ip, self.port, app=pyramid_app)
        server.serve_forever()

def getPyroWrapper():
    if(type(tt_wrap) is None):
        raise Exception("pyro is nonetype")
    return tt_wrap
