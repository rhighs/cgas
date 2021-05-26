from pyramid.config import Configurator
from pyrogram_api_server.controllers import HomeController
from pyrogram_api_server import PGApiServer

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include(".routes")
        config.add_handler("home", "/{action}", handler=HomeController)
        config.scan()

    return config.make_wsgi_app()
