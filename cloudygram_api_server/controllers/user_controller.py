from email.policy import HTTP
from http.client import OK
from operator import truediv
from cloudygram_api_server.models.asyncronous.user_model import *
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse, BaseResponseData
from cloudygram_api_server.payload_keys import telegram_keys, download_keys, file_keys
from cloudygram_api_server.telethon.telethon_wrapper import *
from typing import Union
import json
from fastapi import APIRouter, Response, status, UploadFile, Form, Body
from fastapi.encoders import jsonable_encoder
from telethon.tl.types import Message, MessageMediaDocument, PeerUser

class UserController:
    __autoexpose__ = None
    router = APIRouter()

    @router.get("/{phonenumber}/userInfo", response_model=UserBase, response_model_exclude_unset=True)
    async def user_info_req(phonenumber: str, response: Response):
        response.headers["Content-Type"] = "application/json"
        try:
            result = await get_me(phonenumber)
            user = set_value(True, result)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return set_value(isSuccess=False, message=str(exc))
        return user

    @router.post("/{phonenumber}/uploadFile")
    async def upload_file_req(phonenumber: str, file: UploadFile, response: Response, mimeType: str = Form(), chatid: str = Form()):
        response.headers["Content-Type"] = "application/json"
        phone_number = phonenumber
        file_stream = file
        file_name = file.filename
        mime_type = mimeType
        chatId = chatid
        try:
            result = await upload_file(phone_number, file_name, file_stream, mime_type, chatId)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        result = json.loads(result)
        return result

    @router.post("/{phonenumber}/downloadFile")
    async def download_file_req(phonenumber: str, response: Response, message: str = Body(), path: str = Body()):
        response.headers["Content-Type"] = "application/json"
        try:
            phone_number = phonenumber
            message = json.loads(message)
            #Remove json attribute not need for convert to TLObject --> Message
            #del message['_']
            #del message['peer_id']['_']
            #del message['media']['_']
            #del message['media']['document']['_']
            #
            #for rows in range(len(message['media']['document']['attributes'])):
            #    del message['media']['document']['attributes'][rows]['_']
            #
            #for rows in range(len(message['media']['document']['thumbs'])):
            #    del message['media']['document']['thumbs'][rows]['_']

            message_media = Message(
                id = 			      message['id'],
                peer_id =             PeerUser(message['peer_id']),
                date =                message['date'],
                message =             message['message'],
                out =                 message['out'],
                mentioned =           message['mentioned'],
                media_unread =        message['media_unread'],
                silent =              message['silent'],
                post =                message['post'],
                from_scheduled =      message['from_scheduled'],
                legacy =              message['legacy'],
                edit_hide =           message['edit_hide'],
                pinned =              message['pinned'],
                from_id =             message['from_id'],
                fwd_from =            message['fwd_from'],
                via_bot_id =          message['via_bot_id'],
                reply_to =            message['reply_to'],
                media =               MessageMediaDocument(document = message['media']['document'], ttl_seconds = message['media']['ttl_seconds']),
                reply_markup =	      message['reply_markup'],
                entities =            message['entities'],
                views =               message['views'],
                forwards =            message['forwards'],
                replies =             message['replies'],
                edit_date =           message['edit_date'],
                post_author =         message['post_author'],
                grouped_id =          message['grouped_id'],
                restriction_reason =  message['restriction_reason'],
                ttl_period =          message['ttl_period']      
            )
            result: BaseResponse = await download_file(phone_number, message_media, message['peer_id']['user_id'], file_path=path)
            if (result.isSuccess == False):
                raise ValueError(result.message)

        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return result

    @router.get("/{phonenumber}/isAuthorized")
    async def is_authorized_req(phonenumber: str, response: Response):
        response.headers["Content-Type"] = "application/json"
        try:
            result = await is_authorized(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        if (result):
            response = BaseResponse(isSuccess=True, message="User is authorizated")
        else:
            response = BaseResponse(isSuccess=False, message="User is NOT authorizated")
        return response

    @router.get("/{phonenumber}/downloadProfilePhoto")
    async def download_profile_photo_req(phonenumber: str, response: Response, path: str = None, filename: str = None):
        response.headers["Content-Type"] = "application/json"
        try:
            result: BaseResponse = await download_profile_photo(phonenumber, path, filename)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))

        if result.isSuccess == False:
            response = BaseResponse(isSuccess=False, message="User has no profile photo")
        else:
            response = BaseResponseData(isSuccess=True, message="Profile photo downloaded", data=result.message)  # path where the picture got downloaded
        return response

    @router.get("/{phonenumber}/contacts")
    async def contacts_req(phonenumber: str, response: Response):
        response.headers["Content-Type"] = "application/json"
        try:
            result = await get_contacts(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return {"isSuccess":True, "data":result}

    @router.delete("/{phonenumber}/logout")
    async def logout_req(phonenumber: str, response: Response):
        try:
            result = await logout(phonenumber)
        except Exception as exc:
             response.status_code = handle_exception(str(exc))
             return BaseResponse(isSuccess=False, message=str(exc))
        if not result:
            return BaseResponse(isSuccess=False, message="Can't log out")
        response = BaseResponseData(isSuccess=False, message="Log out successful.", data=result)
        return response

    @router.get("/{phonenumber}/sessionValid")
    async def session_valid_req(phonenumber: str, response: Response):
        response.headers["Content-Type"] = "application/json"
        try:
            result = await session_valid(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        if result:
            response = BaseResponse(isSuccess=True, message="Session is still valid")
        else:
            response = BaseResponse(isSuccess=False, message="Session is not valid")
        return response

    @router.get("/{phonenumber}/dialogs")
    async def contacts_req(phonenumber: str, response: Response):
        try:
            result = await get_dialog(phonenumber)
        except Exception as exc:
            response.status_code = handle_exception(str(exc))
            return BaseResponse(isSuccess=False, message=str(exc))
        return {"isSuccess":True, "data":result}

def handle_exception(exception: Union[TTGenericException, TTUnathorizedException, TTFileTransferException, Exception]) -> status:
        if type(exception) is TTGenericException or type(exception) is Exception or type(exception) is TTFileTransferException:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        elif type(exception) is TTUnathorizedException:
            return status.HTTP_401_UNAUTHORIZED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR