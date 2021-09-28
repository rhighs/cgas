from cloudygram_api_server.models       import UserModels
from pyramid_handlers                   import action
from pyramid.request                    import Request
from cloudygram_api_server.models       import HomeModels
from cloudygram_api_server.models       import SUCCESS_KEY
from cloudygram_api_server.payload_keys import tg_data
from pathlib                            import Path
from os                                 import path
import cloudygram_api_server
import asyncio, concurrent.futures
import os

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.wrap = cloudygram_api_server.get_tt()
        self.request = request

    @action(name="addSession", renderer="json", request_method="GET")
    def add_account(self):
        phone_number = self.request.GET[tg_data.phone][1:]
        self.pool.submit(
                asyncio.run,
                self.wrap.create_session(phone_number)
                ).result()
        return HomeModels.success(message=f"Session with: {phone_number} created.")

    @action(name="sendCode", renderer="json", request_method="GET")
    def send_code(self):
        phone_number = self.request.GET[tg_data.phone][1:]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.send_code(phone_number)
                ).result()
        if type(result) is dict and SUCCESS_KEY in result:
            return result
        return HomeModels.sent_code(result)

    @action(name="signin", renderer="json", request_method="POST")
    def signin(self):
        body = self.request.json_body
        phone_number = body[tg_data.phone][1:]
        phone_code_hash = body[tg_data.code_hash]
        phone_code = body[tg_data.code]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.signin(
                    phone_number,
                    phone_code_hash,
                    phone_code
                    )
                ).result()
        if type(result) is dict and SUCCESS_KEY in result:
            return result
        return UserModels.userDetails(result)

    @action(name="qrLogin", renderer="json", request_method="GET")
    def qr_login(self):
        phone_number=self.request.GET[tg_data.phone]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.qr_login(phone_number)
                ).result()
        self.pool.submit(asyncio.run, result.wait())
        return UserModels.success(data=result.url)

    @action(name="singup", renderer="json", request_method="POST")
    def sign_up(self):
        body = self.request.json_body
        phone_code = body[tg_data.code]
        phone_number = body[tg_data.phone]
        first_name = body[tg_data.fname]
        last_name = body[tg_data.lname]
        phone_code_hash = body[tg_data.code_hash]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.signup(
                    phone_number,
                    phone_code,
                    phone_code_hash,
                    first_name,
                    last_name
                    )
                ).result()
        return UserModels.userDetails(result)

    @action(name="cleanSessions", renderer="json", request_method="DELETE")
    def clean(self):
        self.pool.submit(
                asyncio.run,
                self.wrap.clean()
                ).result()
        return HomeModels.success("Unused sessions cleaned.")

