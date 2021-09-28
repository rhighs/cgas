from pyramid_handlers                   import action
from pyramid.request                    import Request
from pyramid.httpexceptions             import HTTPUnauthorized
from cloudygram_api_server.models       import UserModels
from telethon.tl.types                  import MessageMediaDocument
from cloudygram_api_server.scripts      import jres
from cloudygram_api_server.payload_keys import tg_data, dl, file
import asyncio, concurrent.futures
import cloudygram_api_server
import json

class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request: Request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info(self):
        phone_number = self.request.matchdict[tg_data.phone][1:] #remove + at the beginning
        wrap = cloudygram_api_server.get_tt()
        try:
            user = self.pool.submit(
                asyncio.run,
                wrap.get_me(phone_number)
            ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code),
        except Exception as e:
            return jres(UserModels.failure(str(e)), 500)
        return jres(UserModels.userDetails(user), 200)

    @action(name="uploadFile", renderer="json", request_method="POST")
    def upload_file(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        file_stream = self.request.POST[file.name].file
        file_name = self.request.POST[file.name].filename
        mime_type = self.request.POST[file.mime]
        wrap = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                asyncio.run,
                wrap.upload_file(phone_number, file_name, file_stream, mime_type)
            ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code)
        except Exception as e:
            return jres(UserModels.failure(str(e)), status=500)
        return jres(result, 200)
    
    @action(name="downloadFile", renderer="json", request_method="POST")
    def download_file(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        message_json = self.request.json_body[dl.message]
        if type(message_json) is str:
            message_json = json.loads(message_json)
        path = None
        if file.path in self.request.json_body:
            path = self.request.json_body[file.path]
        try:
            result = self.pool.submit(
                asyncio.run,
                cloudygram_api_server.get_tt().download_file(phone_number, message_json, path)
            ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code)
        except Exception as e:
            return jres(UserModels.failure(str(e)), 500)
        return jres(result, 200)

    @action(name="isAuthorized", renderer="json", request_method="GET")
    def is_authorized(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
            asyncio.run,
            wrap.is_authorized(phone_number)
        ).result()
        response = (
            UserModels.success("User is authorized")
            if result
            else UserModels.failure("User is not authrized")
        )
        return jres(response, 200)

    @action(name="downloadProfilePhoto", renderer="json", request_method="GET")
    def download_profile_photo(self):
        requestDict: dict = self.request.matchdict
        phone_number = requestDict[tg_data.phone][1:]
        path = None
        if file.path in requestDict:
            path = requestDict[file.path]
        wrap = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                asyncio.run,
                wrap.download_profile_picture(phone_number, path)
            ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code)
        except Exception as e:
            return jres(UserModels.failure(str(e)), 500)
        response = UserModels.success(
            message="Profile photo downloaded.",
            data=result #path where the picture got downloaded
        )
        return jres(response, 200)

    @action(name="contacts", renderer="json", request_method="GET")
    def contacts(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        wrap = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                    asyncio.run,
                    wrap.get_contacts(phone_number)
                    ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code)
        except Exception as e:
            return jres(UserModels.failure(message=str(e)), 500)
        response = UserModels.success(
                message="Contacts fetched.",
                data=result
                )
        return jres(response, 200)

    @action(name="logout", renderer="json", request_method="DELETE")
    def logout(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        wrap = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                asyncio.run, 
                wrap.logout(phone_number)
            ).result()
        except HTTPUnauthorized as u:
            return jres(UserModels.unauthorized(), u.status_code)
        except Exception as e:
            return jres(UserModels.failure(message=str(e)), 500)
        if not result:
            return jres(UserModels.failure(message="Clouldn't log out"), 200)
        response = UserModels.success(
            message="Log out successful.",
            data=result
        )
        return jres(response, 200)

    @action(name="sessionValid", renderer="json", request_method="GET")
    def session_valid(self):
        phone_number = self.request.matchdict[tg_data.phone][1:]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
                asyncio.run,
                wrap.session_valid(phone_number)
                ).result()
        if result:
            response = UserModels.success(
                    message="Session is still valid."
                    )
        else:
            response = UserModels.failure(
                    message="Session is not valid."
                    )
        return jres(response, 200)

