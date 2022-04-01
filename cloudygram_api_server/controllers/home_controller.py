from cloudygram_api_server.payload_keys import telegram_keys
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.models import UserModels
from cloudygram_api_server.models import HomeModels
from cloudygram_api_server.scripts import jres
from cloudygram_api_server.telethon.exceptions import TTUnathorizedException
from pyramid_handlers import action
from pyramid.request import Request
from typing import Union
import concurrent.futures
import asyncio

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.request = request
        self.expected_errors = (TTGenericException, TTUnathorizedException, Exception)

    def handle_exceptions(self, exception: Union[TTGenericException, TTUnathorizedException, Exception]) -> dict:
        if type(exception) is TTGenericException or type(exception) is Exception:
            return jres(HomeModels.failure(str(exception)), status=500)
        elif type(exception) is TTUnathorizedException:
            return jres(HomeModels.failure(str(exception)), status=401)
        else:
            return jres(HomeModels.failure(str(exception)), status=500)

    @action(name="sendCode", renderer="json", request_method="GET")
    def send_code_req(self):
        phone_number = self.request.GET[telegram_keys.phone_number][1:]
        try:
            result = self.pool.submit(
                    asyncio.run,
                    send_code(phone_number)
                    ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(HomeModels.sent_code(result), 200)

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
        return jres(UserModels.userDetails(result), 200)

    @action(name="qrLogin", renderer="json", request_method="GET")
    def qr_login_req(self):
        phone_number = self.request.GET[telegram_keys.phone_number]
        try:
            result = self.pool.submit(
                    asyncio.run,
                    qr_login(phone_number)
                    ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        self.pool.submit(asyncio.run, result.wait())
        return jres(UserModels.success(data=result.url), 200)

    @action(name="singup", renderer="json", request_method="POST")
    def sign_up_req(self):
        body = self.request.json_body
        phone_number = body[telegram_keys.phone_number]
        first_name = body[telegram_keys.first_name]
        last_name = body[telegram_keys.last_name]
        phone_code = body[telegram_keys.phone_code]
        phone_code_hash = body[telegram_keys.phone_code_hash]
        try:
            result = self.pool.submit(
                    asyncio.run,
                    signup(
                        phone_number,
                        phone_code,
                        phone_code_hash,
                        first_name,
                        last_name
                    )
                ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(UserModels.userDetails(result), 200)

    @action(name="cleanSessions", renderer="json", request_method="DELETE")
    def clean_req(self):
        clean()
        return HomeModels.success("Unused sessions cleaned.")

