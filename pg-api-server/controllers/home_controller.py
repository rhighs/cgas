def class HomeController:
    def __init__(self, pyro_wrapper):
        self.pyro = pyro_wrapper
        
    def add_account(self, request):
        return { "does" : "nothing"}

    def send_code(self, request)
        phone_number = request.POST["phoneNumber"]

        try:
            result = self.pyro.send_code(phone_number) 
        except:
            return { "isSuccess": False, "message" : "Invalid phone number" }

        return { "isSuccess" : True, "sentCode" : result }

    def signin(self, request):
        phone_number = request.POST["phoneNumber"]
        phone_code_hash = request.POST["phoneCodeHash"]
        phone_code = request.POST["phoneCode"]

        try: 
            result = self.pyro.signin(phone_number, phone_code_hash, phone_code)
        except:
            return { "isSuccess" : False, "message" : "Could not signin"}

        return { "isSuccess" : True, "userData": result }

    def send_private_message(self, request):
        self.pyro.send_private_message(request.POST["accountName"], request.POST["message"])
