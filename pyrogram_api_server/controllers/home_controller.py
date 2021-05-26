from pyramid_handlers import action
from pyramid.response import Response
from . import pyro_wrap

def class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request):
        self.pyro = pyro_wrap
        self.request = request
        
    @action(name="addAccount", renderer="json", request_method="POST")
    def add_account(self, request):
        return { "does" : "nothing"}

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self)
        phone_number = self.request.POST["phoneNumber"]
        try:
            result = self.pyro.send_code(phone_number) 
        except:
            return { "isSuccess": False, "message" : "Invalid phone number" }
        return { "isSuccess" : True, "sentCode" : result }

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        try: 
            result = self.pyro.signin(phone_number, phone_code_hash, phone_code)
        except:
            return { "isSuccess" : False, "message" : "Could not signin"}
        return { "isSuccess" : True, "userData": result }

    @action(name="sendPrivateMessage", renderer="json", request_method="POST")
    def send_private_message(self):
        self.pyro.send_private_message(request.POST["phoneNumber"], request.POST["message"])