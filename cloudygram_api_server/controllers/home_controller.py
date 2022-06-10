from mimetypes import guess_extension
from cloudygram_api_server.models.asyncronous.home_model import HomeResponse
from cloudygram_api_server.models.asyncronous.user_model import set_value
from cloudygram_api_server.payload_keys import telegram_keys
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.telethon.exceptions import TTUnathorizedException
from typing import Union
from fastapi import APIRouter
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse, BaseResponseData
from fastapi import APIRouter, Response, status, UploadFile, Form, Body
from fastapi.encoders import jsonable_encoder

class HomeController(object):
    __autoexpose__ = None
    router = APIRouter()

    @router.get("/sendCode")
    async def send_code_req(phonenumber: str, response: Response):
        try:
            result = await send_code(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return HomeResponse(isSuccess=True, sendCode=result)


    @router.post("/signin")
    async def signin_req(response: Response, 
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


    @router.delete("/cleanSessions")
    async def clean_req(phonenumber: str):
        await clean()
        return BaseResponse(isSuccess=True, message="Unused sessions cleaned")


def handle_exception(exception: Union[TTGenericException, TTUnathorizedException, TTFileTransferException, Exception]) -> status:
        if type(exception) is TTGenericException or type(exception) is Exception or type(exception) is TTFileTransferException:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        elif type(exception) is TTUnathorizedException:
            return status.HTTP_401_UNAUTHORIZED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR