from pyrogram_api_server.controllers    import HomeController
from wsgiref.simple_server              import make_server
from pyramid.config                     import Configurator
from pyrogram_api_server.scripts        import PyroWrap

pyro_wrap = None

def configure(**settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_handlers')
        config.add_handler("home", "/{action}", handler=HomeController)
        config.scan()
    return config.make_wsgi_app()

class ApiServer:
    def __init__(self, api_id, api_hash, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.api_id = api_id
        self.api_hash = api_hash
    
    def run(self):
        global pyro_wrap
        pyro_wrap = PyroWrap(api_id = self.api_id, api_hash=self.api_hash, workdir="./settings")
        pyramid_app = configure(settings=None)
        server = make_server(self.host_ip, self.port, app=pyramid_app)
        server.serve_forever()

def getPyroWrapper():
    if(type(pyro_wrap) is None):
        raise Exception("pyro is none")

    return pyro_wrap
