def class RoutesConfigurator(configurator):
    routes = [
            ("index", "/"),
            ("signin", "/signin")
            ]

    def setup_routes():
        for name, path in routes:
            configurator.add_route()
