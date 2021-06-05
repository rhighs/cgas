from pyramid.url import static_url
from pyramid_handlers               import action
from pyramid.request                import Request
from pyramid.httpexceptions         import HTTPUnauthorized
from cloudygram_api_server.models   import UserModels
from telethon.tl.types              import MessageMediaDocument
from pyramid.response               import Response
import json
import asyncio, concurrent.futures
import cloudygram_api_server

class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request: Request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        wrap = cloudygram_api_server.get_tt()
        try:
            user = self.pool.submit(
                asyncio.run,
                wrap.get_me(phone_number)
            ).result()
        except HTTPUnauthorized as u:
            return Response(json.dumps(UserModels.unauthorized()),
                            status=u.status_code)
        except Exception as e:
            response = UserModels.failure(message=str(e))
            return Response(json.dumps(response), status=500)
        response = UserModels.userDetails(user)
        return Response(json.dumps(response), status=200)

    @action(name="uploadFile", renderer="json", request_method="POST")
    def upload_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:] #remove + at the beginning
        file_stream = self.request.POST["file"].file
        file_name = self.request.POST["file"].filename
        mime_type = self.request.POST["mimeType"]
        wrap = cloudygram_api_server.get_tt()
        print(file_name)
        try:
            result = self.pool.submit(
                asyncio.run,
                wrap.upload_file(phone_number=phone_number, file_name=file_name, file_stream=file_stream, mime_type=mime_type)
            ).result()
        except HTTPUnauthorized as u:
            response = UserModels.unauthorized
            return Response(json.dumps(response), status=401)
        except Exception as e:
            print(str(e))
            response = UserModels.failure(message=str(e))
            return Response(json.dumps(response), status=500)
        return Response(body=json.dumps(result), status=200, content_type="application/json", charset="UTF-8")
    
    @action(name="downloadFile", renderer="json", request_method="POST")
    def download_file(self):
        phone_number = self.request.matchdict["phoneNumber"][1:]
        message_json = self.request.json_body["message"]
        path=None
        if "path" in self.request.json_body:
            path = self.request.json_body["path"]
        try:
            result: MessageMediaDocument = self.pool.submit(
                asyncio.run,
                cloudygram_api_server.get_tt().download_file(phone_number=phone_number, message_json=message_json, path=path)
            ).result()
            response = UserModels.success(message=f"File witd id: {result.document.id} downloaded successfully!") 
        except HTTPUnauthorized as u:
            return Response(json.dumps(UserModels.unauthorized()),
                            charset="UTF-8",
                            content_type="application/json",
                            status=u.status_code)
        except Exception as e:
            response = UserModels.failure(message=str(e))
            return Response(json.dumps(response),
                            charset="UTF-8",
                            content_type="application/json",
                            status=500)
        return Response(body=json.dumps(response), charset="UTF-8", content_type="application/json", status=200)

    @action(name="isAuthorized", renderer="json", request_method="GET")
    def is_authorized(self):
        phone_number = self.request.GET["phoneNumber"] 
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
            asyncio.run,
            wrap.is_authorized(phone_number)
        ).result()
        response = (
            UserModels.success(message="User is authorized")
            if result
            else UserModels.failure(message="User is not authrized")
        )
        return Response(json.dumps(response), status=200)

    @action(name="downloadProfilePhoto", renderer="json", request_method="GET")
    def download_profile_photo(self):
        phone_number = self.request.matchdict["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                asyncio.run,
                wrap.download_profile_picture(phone_number)
            ).result()
        except HTTPUnauthorized as u:
            return Response(json.dumps(UserModels.unauthorized()),
                            status=u.status_code)
        except Exception as e:
            response = UserModels.failure(message=str(e))
            return Response(json.dumps(response), status=500)
        response = UserModels.success(
            message="profile photo downloaded!",
            data=result #path where thw picture got downloaded
        )
        return Response(json.dumps(result), status=200)

    @action(name="logout", renderer="json", request_method="DELETE")
    def logout(self):
        phone_number = self.request.matchdict["phoneNumber"][1:]
        wrap  = cloudygram_api_server.get_tt()
        try:
            result = self.pool.submit(
                asyncio.run, 
                wrap.logout(phone_number)
            ).result()
        except HTTPUnauthorized as u:
            return Response(json.dumps(UserModels.unauthorized()),
                            status=u.status_code)
        except Exception as e:
            return Response(json.dumps(UserModels.failure(message=str(e))),
                            status=500)
        if not result:
            return Response(json.dumps(UserModels.failure(message="Clouldn't log out")),
                            status=200)
        response = UserModels.success(
            message="log out successful!",
            data=result
        )
        return Response(body=json.dumps(response), status=200, content_type="application/json", charset="UTF-8")
