from pyrogram_api_server.controller import HomeController

def class RoutesConfigurator:
    def __init__(self, configurator):
        self.configurator = configurator
        self.routes = [
            ("index", "/"),
            ("signin", "/signin"),
            ("sendCode", "/sendCode")
            ]

    def setup_routes(self):
        for name, path in self.routes:
            self.configurator.add_route()
