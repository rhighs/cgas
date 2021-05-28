from pyrogram_api_server.models.user_model import UserModels
from pyramid_handlers import action
from pyramid.response               import Response
from pyramid.request                import Request
from pyrogram_api_server.models     import HomeModels
from pyrogram_api_server.scripts    import PyroWrap
import pyrogram_api_server

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.request = request

    @action(name="authorize", renderer="json", request_method="POST") 
    def authorize(self):
        api_id = self.request.POST["api_id"]
        api_hash = self.request.POST["api_hash"]
        workdir = self.request.POST["workdir"]
        try:
            pyrogram_api_server.pyro_wrap = PyroWrap(api_id, api_hash, workdir, createNow=True)
        except Exception as e:
            return HomeModels.failure(message=f"Exception occurred --> {str(e)}")
        return HomeModels.success(message="Wrapper created!")
        
    @action(name="addAccount", renderer="json", request_method="POST")
    def add_account(self):
        name = self.request.POST["accountName"] 
        pyrogram_api_server.getPyroWrapper().create_client(name);
        return HomeModels.success(message=f"Account -> {name} created.")

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        result = self.pyro.send_code(phone_number) 
        if(result == False):
            return HomeModels.failure("Invalid phone number.")
        return HomeModels.sent_code(result)

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        result = self.pyro.signin(phone_number, phone_code_hash, phone_code)
        if(result == False):
            return HomeModels.failure("Could not signin.")
        return UserModels.userDetails(result)
