from cloudygram_api_server.models       import UserModels
from pyramid_handlers                   import action
from pyramid.response                   import Response
from pyramid.request                    import Request
from cloudygram_api_server.models       import HomeModels
from cloudygram_api_server.scripts      import TtWrap
from cloudygram_api_server.models       import SUCCESS_KEY
import cloudygram_api_server
import asyncio, concurrent.futures


class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.request = request

    @action(name="changeApiKeys", renderer="json", request_method="POST") 
    def authorize(self):
        api_id = self.request.POST["api_id"]
        api_hash = self.request.POST["api_hash"]
        workdir = self.request.POST["workdir"]
        try:
            cloudygram_api_server.pyro_wrap = TtWrap(api_id, api_hash)
        except Exception as e:
            return HomeModels.failure(message=f"Exception occurred --> {str(e)}")
        return HomeModels.success(message="Wrapper created!")
        
    @action(name="addSession", renderer="json", request_method="POST")
    def add_account(self):
        phoneNumber = self.request.POST["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        wrap.create_session(phoneNumber)
        return HomeModels.success(message=f"Session with: {phoneNumber} created.")

    @action(name="sendCode", renderer="json", request_method="POST")
    def send_code(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(asyncio.run, wrap.send_code(phone_number)).result() 
        if type(result) is dict and SUCCESS_KEY in result:
            return result
        return HomeModels.sent_code(result)

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        phone_number = self.request.POST["phoneNumber"][1:]
        phone_code_hash = self.request.POST["phoneCodeHash"]
        phone_code = self.request.POST["phoneCode"]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(asyncio.run, wrap.signin(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)).result()
        if(result[SUCCESS_KEY] == False):
            return result
        return UserModels.userDetails(result)

    @action(name="qrLogin", renderer="json", request_method="GET")
    def qr_login(self):
        phone_number=self.request.GET["phoneNumber"]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(asyncio.run, wrap.qr_login(phone_number)).result()
        self.pool.submit(asyncio.run, result.wait())
        return UserModels.success(data=result.url)
