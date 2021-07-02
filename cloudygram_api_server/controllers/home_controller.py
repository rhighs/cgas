from cloudygram_api_server.models       import UserModels
from pyramid_handlers                   import action
from pyramid.request                    import Request
from cloudygram_api_server.models       import HomeModels
from cloudygram_api_server.models       import SUCCESS_KEY
import cloudygram_api_server
import asyncio, concurrent.futures
import os
from pathlib import Path
from os import path

class HomeController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.wrap = cloudygram_api_server.get_tt()
        self.request = request

    @action(name="addSession", renderer="json", request_method="GET")
    def add_account(self):
        phoneNumber = self.request.GET["phoneNumber"][1:]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.create_session(phoneNumber)
                ).result()
        return HomeModels.success(message=f"Session with: {phoneNumber} created.")

    @action(name="sendCode", renderer="json", request_method="GET")
    def send_code(self):
        phone_number = self.request.GET["phoneNumber"][1:]
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
        phone_number = body["phoneNumber"][1:]
        phone_code_hash = body["phoneCodeHash"]
        phone_code = body["phoneCode"]
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
        phone_number=self.request.GET["phoneNumber"]
        result = self.pool.submit(
                asyncio.run,
                self.wrap.qr_login(phone_number)
                ).result()
        self.pool.submit(asyncio.run, result.wait())
        return UserModels.success(data=result.url)

    @action(name="singup", renderer="json", request_method="POST")
    def sign_up(self):
        body = self.request.json_body
        phone_code = body["phoneCode"]
        phone_number = body["phone_number"]
        first_name = body["firstName"]
        last_name = body["lastName"]
        phone_code_hash = body["phoneCodeHash"]
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

