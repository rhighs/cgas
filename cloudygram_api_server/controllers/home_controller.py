from mimetypes import guess_extension
import mimetypes
from cloudygram_api_server.models.asyncronous.home_model import HomeResponse
from cloudygram_api_server.models.asyncronous.user_model import set_value
from cloudygram_api_server.payload_keys import telegram_keys
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.models import UserModels
from cloudygram_api_server.models import HomeModels
from cloudygram_api_server.scripts import jres
from cloudygram_api_server.telethon.exceptions import TTUnathorizedException
from pyramid_handlers import action
from pyramid.request import Request
from typing import Union
from http import HTTPStatus
import concurrent.futures
import asyncio
from fastapi import APIRouter
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse, BaseResponseData
from fastapi import APIRouter, Response, status, UploadFile, Form, Body
from fastapi.encoders import jsonable_encoder

class HomeController(object):
    __autoexpose__ = None
    router = APIRouter()

    def __init__(self, request: Request):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.request = request
        self.expected_errors = (TTGenericException, TTUnathorizedException, Exception)

    @router.get("/{phonenumber}/sendCode")
    async def send_code_req(phonenumber: str, response: Response):
        try:
            result = await send_code(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return HomeResponse(isSuccess=True, sendCode=result)

    @router.post("/signin")
    async def signin_req(phonenumber: str, 
                        response: Response, 
                        phoneNumber: str = Body(), 
                        phoneCodeHash: str = Body(), 
                        phoneCode: str = Body(), 
                        password: str = Body()):
        try:
            result = await signin(
                        phoneNumber,
                        phoneCodeHash,
                        phoneCode,
                        password
                        )
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return set_value(isSuccess=True, UserDetails=result)

    #@action(name="singup", renderer="json", request_method="POST")
    #def sign_up_req(self):
    #    body = self.request.json_body
    #    phone_number = body[telegram_keys.phone_number]
    #    first_name = body[telegram_keys.first_name]
    #    last_name = body[telegram_keys.last_name]
    #    phone_code = body[telegram_keys.phone_code]
    #    phone_code_hash = body[telegram_keys.phone_code_hash]
    #    try:
    #        result = self.pool.submit(
    #                asyncio.run,
    #                signup(
    #                    phone_number,
    #                    phone_code,
    #                    phone_code_hash,
    #                    first_name,
    #                    last_name
    #                )
    #            ).result()
    #    except self.expected_errors as exc:
    #        return self.handle_exceptions(exc)
    #    return jres(UserModels.userDetails(result), 200)

    @action(name="cleanSessions", renderer="json", request_method="DELETE")
    def clean_req(self):
        clean()
        return HomeModels.success("Unused sessions cleaned.")

    @action(name="signin", renderer="json", request_method="POST")
    def signin_req(self):
        body = self.request.json_body
        phone_number = body[telegram_keys.phone_number][1:]
        phone_code_hash = body[telegram_keys.phone_code_hash]
        phone_code = body[telegram_keys.phone_code]
        phone_password = body[telegram_keys.phone_password]
        try:
            result = self.pool.submit(
                    asyncio.run,
                    signin(
                        phone_number,
                        phone_code_hash,
                        phone_code,
                        phone_password
                        )
                    ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(UserModels.userDetails(result), HTTPStatus.OK)

    #@action(name="qrLogin", renderer="json", request_method="GET")
    #def qr_login_req(self):
    #    phone_number = self.request.GET[telegram_keys.phone_number]
    #    try:
    #        result = self.pool.submit(
    #                asyncio.run,
    #                qr_login(phone_number)
    #                ).result()
    #    except self.expected_errors as exc:
    #        return self.handle_exceptions(exc)
    #    self.pool.submit(asyncio.run, result.wait())
    #    return jres(UserModels.success(data=result.url), 200)

    @router.get("/mimetype")
    async def mimetype_get(file: str):
        try:
            result = mimetypes.guess_type(file)[0]
            file = os.fspath(file)
            print(file)
            print(os.path.basename(file))
        except Exception as e:
                traceback.print_exc()
        return result

    @router.get("/mimetype/{phonenumber}")
    async def mimetype_get(file: str, phonenumber: str):
        try:
            result = mimetypes.guess_type(file)[0]
            file = os.fspath(file)
            print(file)
            print(os.path.basename(file))
            phone = phonenumber[1:]
        except Exception as e:
                traceback.print_exc()
        return {"file": file, "phoneNumber": phone}


def handle_exceptions(self, exception: Union[TTGenericException, TTUnathorizedException, Exception]) -> dict:
        if type(exception) is TTGenericException or type(exception) is Exception:
            return jres(HomeModels.failure(str(exception)), status=500)
        elif type(exception) is TTUnathorizedException:
            return jres(HomeModels.failure(str(exception)), status=401)
        else:
            return jres(HomeModels.failure(str(exception)), status=500)

def handle_exception(exception: Union[TTGenericException, TTUnathorizedException, TTFileTransferException, Exception]) -> status:
        if type(exception) is TTGenericException or type(exception) is Exception or type(exception) is TTFileTransferException:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        elif type(exception) is TTUnathorizedException:
            return status.HTTP_401_UNAUTHORIZED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
