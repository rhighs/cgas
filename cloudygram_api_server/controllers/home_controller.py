from pyrogram_api_server.models     import UserModels
from pyramid_handlers               import action
from pyramid.response               import Response
from pyramid.request                import Request
from cloudygram_api_server.models     import HomeModels
from cloudygram_api_server.scripts    import PyroWrap
from cloudygram_api_server.models     import SUCCESS_KEY
import cloudygram_api_server

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.request = request

    @action(name="changeApiKeys", renderer="json", request_method="POST") 
    def authorize(self):
        api_id = self.request.POST["api_id"]
        api_hash = self.request.POST["api_hash"]
        workdir = self.request.POST["workdir"]
        try:
            cloudygram_api_server.pyro_wrap = PyroWrap(api_id, api_hash, workdir)
        except Exception as e:
            return HomeModels.failure(message=f"Exception occurred --> {str(e)}")
        return HomeModels.success(message="Wrapper created!")
        
    @action(name="addSession", renderer="json", request_method="POST")
    def add_account(self):
        phoneNumber = self.request.POST["phoneNumber"][1:]
        cloudygram_api_server.getPyroWrapper().create_session(phoneNumber)
        return HomeModels.success(message=f"Session with: {phoneNumber} created.")

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        result = cloudygram_api_server.getPyroWrapper().send_code(phone_number) 
        if type(result) is dict and SUCCESS_KEY in result:
            return result
        return HomeModels.sent_code(result)

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        result = cloudygram_api_server.getPyroWrapper().signin(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)
        if(result[SUCCESS_KEY] == False):
            return result
        return UserModels.userDetails(result)
