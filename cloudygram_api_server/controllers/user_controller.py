from cloudygram_api_server.models import UserModels
from pyramid_handlers           import action
from pyramid.request import Request
import cloudygram_api_server
import asyncio, concurrent.futures

class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request: Request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        try:
            user = self.pool.submit(asyncio.run, cloudygram_api_server.get_tt().get_me(phone_number)).result()
        except Exception as e: 
            return UserModels.failure(message=f"Exception occurred --> {str(e)}")
        return UserModels.userDetails(user)

    @action(name="uploadFile", renderer="json", request_method="POST")
    def upload_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        file_stream = self.request.POST["file"].file
        file_name = self.request.POST["file"].filename
        print(file_name)
        try:
            self.pool.submit(asyncio.run, cloudygram_api_server.get_tt().upload_file(phone_number=phone_number, file_name=file_name, file_stream=file_stream)).result()
        except Exception as e:
            return UserModels.failure(message=e)
        return 
    
    @action(name="downloadFile", renderer="json", request_method="POST")
    def download_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:]
        try:
            self.pool.submit(asyncio.run, cloudygram_api_server.get_tt().download_file(phone_number=phone_number, file_id=123)).result()
        except Exception as e:
            return UserModels.failure(message=e)
        return 
        
