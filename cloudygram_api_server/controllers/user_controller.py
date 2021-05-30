from cloudygram_api_server.models import UserModels
from pyramid_handlers           import action
import cloudygram_api_server
import asyncio, concurrent.futures

class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        try:
            user = self.pool.submit(asyncio.run, cloudygram_api_server.getPyroWrapper().get_me(phone_number)).result()
        except Exception as e: 
            return UserModels.failure(message=f"Exception occurred --> {str(e)}")
        return UserModels.userDetails(user)

    @action(name="uploadFile", renderer="json", request_method="GET")
    def upload_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        file_path = self.request.GET("filePath")
        try:
            result = cloudygram_api_server.getPyroWrapper().upload_file(phone_number, file_path)
        except Exception as e:
            return UserModels.failure(message=e)
        return UserModels.success(data=result)
