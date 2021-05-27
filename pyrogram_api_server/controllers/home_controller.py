from pyramid_handlers import action
from pyramid.response import Response
import pyrogram_api_server

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request):
        self.request = request
        
    @action(name="addAccount", renderer="json", request_method="POST")
    def add_account(self):
        name = self.request.PORT["accountName"]
        success = pyrogram_api_server.getPyroWrapper().create_client(name);
        return { "message": f"Account -> {name} created" } if success else { "message" : "Account not created" }

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self):
        phone_number = self.request.POST["phoneNumber"]
        result = self.pyro.send_code(phone_number) 
        if(result == False):
            return { "isSuccess": False, "message" : "Invalid phone number" }
        return { "isSuccess" : True, "sentCode" : result }

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        result = self.pyro.signin(phone_number, phone_code_hash, phone_code)
        if(result == False):
            return { "isSuccess" : False, "message" : "Could not signin"}
        return { "isSuccess" : True, "userData": result }

    @action(name="sendPrivateMessage", renderer="json", request_method="POST")
    def send_private_message(self):
        self.pyro.send_private_message(self.request.POST["phoneNumber"], self.request.POST["message"])
