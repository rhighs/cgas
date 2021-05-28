from pyrogram_api_server.models import UserModels
from pyramid_handlers           import action
import pyrogram_api_server

class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request = request

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        try:
            result = pyrogram_api_server.getPyroWrapper().get_me(phone_number)
        except Exception as e: 
            return { "state" : "exception occurred"}
        return { "username" : result.username, "phoneNumber" : result.phone_number, "lastOnline" : result.last_online_date }

    @action(name="uploadFile", renderer="json", request_method="GET")
    def upload_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        file_path = self.request.GET("filePath")

        try:
            result = pyrogram_api_server.getPyroWrapper().upload_file(phone_number, file_path)
        except Exception as e:
            return UserModels.failure(message=e)
        return UserModels.success(data=result)
