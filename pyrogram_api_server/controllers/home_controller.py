from pyramid_handlers import action
from pyramid.response import Response
from pyrogram_api_server.scripts import PyroWrap
import pyrogram_api_server

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request):
        self.request = request

    @action(name="authorize", renderer="json", request_method="POST") 
    def authorize(self):
        api_id = self.request.POST["api_id"]
        api_hash = self.request.POST["api_hash"]
        workdir = self.request.POST["workdir"]
        try:
            pyrogram_api_server.pyro_wrap = PyroWrap(api_id, api_hash, workdir, createNow=True)
        except Exception as e:
            return { "isSuccess" : False, "message" : e }
        return { "isSuccess" : True, "message" : "Wrapper created!" }
        
    @action(name="addAccount", renderer="json", request_method="POST")
    def add_account(self):
        name = self.request.PORT["accountName"]
        success = pyrogram_api_server.getPyroWrapper().create_client(name);
        return { "message": f"Account -> {name} created" } if success else { "message" : "Account not created" }

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        result = self.pyro.send_code(phone_number) 
        if(result == False):
            return { "isSuccess": False, "message" : "Invalid phone number" }
        return { "isSuccess" : True, "sentCode" : result }

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        result = self.pyro.signin(phone_number, phone_code_hash, phone_code)
        if(result == False):
            return { "isSuccess" : False, "message" : "Could not signin"}
        return { "isSuccess" : True, "userData": result }
