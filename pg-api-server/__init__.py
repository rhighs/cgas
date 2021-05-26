from pyramid.config import Configurator

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include(".routes")
        config.scan()

    return config.make_wsgi_app()
