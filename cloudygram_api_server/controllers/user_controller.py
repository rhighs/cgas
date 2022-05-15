from email.policy import HTTP
from http import HTTPStatus
from cloudygram_api_server.payload_keys import telegram_keys, download_keys, file_keys
from cloudygram_api_server.telethon.parser import document_to_input_document_file_location
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.models import UserModels
from cloudygram_api_server.scripts import jres
from pyramid_handlers import action
from pyramid.request import Request
from typing import Union
import concurrent.futures
import asyncio
import math
import json


class UserController:
    __autoexpose__ = None

    def __init__(self, request):
        self.request: Request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.expected_errors = (TTGenericException, TTUnathorizedException, TTFileTransferException, Exception)

    def handle_exceptions(self, exception: Union[TTGenericException, TTUnathorizedException, TTFileTransferException, Exception]) -> dict:
        if type(exception) is TTGenericException or type(exception) is Exception or type(exception) is TTFileTransferException:
            return jres(UserModels.failure(str(exception)), status=500)
        elif type(exception) is TTUnathorizedException:
            return jres(UserModels.failure(str(exception)), status=401)
        else:
            return jres(UserModels.failure(str(exception)), status=500)

    @action(name="userInfo", renderer="json", request_method="GET")
    def user_info_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        try:
            user = self.pool.submit(
                asyncio.run,
                get_me(phone_number)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(UserModels.userDetails(user), 200)

    @action(name="uploadFile", renderer="json", request_method="POST")
    def upload_file_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        file_stream = self.request.POST[file_keys.name].file
        file_name = self.request.POST[file_keys.name].filename
        mime_type = self.request.POST[file_keys.mime_type]
        try:
            result = self.pool.submit(
                asyncio.run,
                upload_file(phone_number, file_name, file_stream, mime_type)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(result, 200)

    @action(name="downloadFile", renderer="json", request_method="POST")
    def download_file_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        message_json = self.request.json_body[download_keys.message]
        if type(message_json) is str:
            message_json = json.loads(message_json)
        path = None
        if file_keys.path in self.request.json_body:
            path = self.request.json_body[file_keys.path]
        try:
            result = self.pool.submit(
                asyncio.run,
                download_file(phone_number, message_json, path)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(result.dict(), 200)

    @action(name="isAuthorized", renderer="json", request_method="GET")
    def is_authorized_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        try:
            result = self.pool.submit(
                asyncio.run,
                is_authorized(phone_number)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        response = (
            UserModels.success("User is authorized")
            if result
            else UserModels.failure("User is not authrized")
        )
        return jres(response, 200)

    @action(name="downloadProfilePhoto", renderer="json", request_method="GET")
    def download_profile_photo_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        filepath: str = ""
        filename: str = ""
        if file_keys.path in self.request.GET:
            filepath = self.request.GET[file_keys.path]
        if file_keys.filename in self.request.GET:
            filename = self.request.GET[file_keys.filename]
        try:
            result = self.pool.submit(
                asyncio.run,
                download_profile_photo(phone_number, filepath, filename)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)

        if result is None:
            response = UserModels.failure(
                message="User has no profile photo."
            )
        else:
            response = UserModels.success(
                message="Profile photo downloaded.",
                data=result  # path where the picture got downloaded
            )
        return jres(response, 200)

    @action(name="contacts", renderer="json", request_method="GET")
    def contacts_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        try:
            result = self.pool.submit(
                asyncio.run,
                get_contacts(phone_number)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        response = UserModels.success(
            message="Contacts fetched.",
            data=result
        )
        return jres(response, 200)

    @action(name="logout", renderer="json", request_method="DELETE")
    def logout_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        try:
            result = self.pool.submit(
                asyncio.run,
                logout(phone_number)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        if not result:
            return jres(UserModels.failure(message="Clouldn't log out"), 200)
        response = UserModels.success(
            message="Log out successful.",
            data=result
        )
        return jres(response, 200)

    @action(name="sessionValid", renderer="json", request_method="GET")
    def session_valid_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        try:
            result = self.pool.submit(
                asyncio.run,
                session_valid(phone_number)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        if result:
            response = UserModels.success(
                message="Session is still valid."
            )
        else:
            response = UserModels.failure(
                message="Session is not valid."
            )
        return jres(response, 200)

    @action(name="streamContent", renderer="json", request_method="POST")
    def stream_content_req(self):
        phone_number = self.request.matchdict[telegram_keys.phone_number][1:]
        message_json = self.request.json_body[download_keys.message]
        file = parse_updates(message_json).ducument
        file_location = document_to_input_document_file_location(file)

        def chunk_size(length):
            return 2 ** max(min(math.ceil(math.log2(length / 1024)), 10), 2) * 1024

        def offset_fix(offset, chunksize):
            offset -= offset % chunksize
            return offset

        if "Range" in self.request.headers:
            range_header = self.request.headers["Range"]
            from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
            from_bytes = int(from_bytes)
            until_bytes = int(until_bytes) if until_bytes else file.size - 1
        else:
            return jres(UserModels.failure("Range header not present or invalid"), HTTPStatus.BAD_REQUEST)

        req_length = until_bytes - from_bytes
        chunk_size = chunk_size(req_length)
        offset = offset_fix(from_bytes, chunk_size)
        first_part_cut = from_bytes - offset
        last_part_cut = (until_bytes % chunk_size) + 1
        part_count = math.ceil(req_length / chunk_size)

        response = self.request.response
        response.content_type = "application/octet-stream"
        response.headers["Range"] = f"bytes={from_bytes}-{until_bytes}"
        response.headers["Content-Range"] = f"bytes {from_bytes}-{until_bytes}/{file.size}"
        response.headers["Content-Disposition"] = f"attachment; filename=\"{file.name}\""
        response.headers["Accept-Ranges"] = "bytes"

        try: 
            result = self.pool.submit(
                asyncio.run,
                yield_file_sync(phone_number, file_location, from_bytes, first_part_cut, last_part_cut, part_count)
            )
        except:
            pass

        response.file_iter = result
        return response
