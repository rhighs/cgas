def class HomeController:
    def __init__(self, pyro_wrapper):
        self.pyro = pyro_wrapper
        
    def add_account(self, request):
        return { "does" : "nothing"}

    def signin(self, phone_number):
        return { "does" : "nothing" }

    def send_private_message(self, request):
        self.pyro.send_private_message(request.POST["accountName"], request.POST["message"])