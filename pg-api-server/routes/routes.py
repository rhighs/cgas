from ..controllers import HomeController

def class RoutesConfigurator:

    def __init__(self, configurator):
        self.configurator = configurator
        self.routes = [
            ("index", "/"),
            ("signin", "/signin")
            ]

    def setup_routes(self):
        for name, path in self.routes:
            self.configurator.add_route()
