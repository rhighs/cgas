from cloudygram_api_server.models import UserModels, TtModels
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.telethon.exceptions import *
from cloudygram_api_server.scripts import jres
from pyramid_handlers import action
from pyramid.request import Request
import asyncio, concurrent.futures
from typing import List, Union
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse, BaseResponseData
from fastapi import APIRouter, Response, status, UploadFile, Form, Body
from fastapi.encoders import jsonable_encoder

class MessagesController(object):
    router = APIRouter()
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.expected_errors = (TTGenericException, TTUnathorizedException, Exception)

    @router.get("/{phonenumber}/getMessages")
    async def get_messages_req(phonenumber: str, response: Response):
        try:
            result = await get_messages(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return BaseResponse(isSuccess=False, message=result)

    @router.post("/{phonenumber}/deleteMessages")
    async def delete_messages_req(phonenumber: str, response: Response, ids: List[str] = Body()):
        message_ids = ids
        try:
            await delete_messages(phonenumber, message_ids)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return BaseResponse(isSuccess=True)


def handle_exceptions(self, exception: Union[TTGenericException, TTUnathorizedException, Exception]) -> dict:
    if type(exception) is TTGenericException or type(exception) is Exception:
        return jres(UserModels.failure(str(exception)), status=500)
    elif type(exception) is TTUnathorizedException:
        return jres(UserModels.failure(str(exception)), status=401)
    else:
        return jres(UserModels.failure(str(exception)), status=500)

def handle_exception(exception: Union[TTGenericException, TTUnathorizedException, TTFileTransferException, Exception]) -> status:
        if type(exception) is TTGenericException or type(exception) is Exception or type(exception) is TTFileTransferException:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        elif type(exception) is TTUnathorizedException:
            return status.HTTP_401_UNAUTHORIZED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR