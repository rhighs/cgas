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
        self.request = request
    
    @action(name="deleteSession", renderer="json", request_method="DELETE")
    def delete_account(self):
        phoneNumber = self.request.GET["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        wrap.deleteSession(phoneNumber)
        return HomeModels.success(message=f"Session with: {phoneNumber} deleted.")

    @action(name="addSession", renderer="json", request_method="GET")
    def add_account(self):
        phoneNumber = self.request.GET["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        wrap.create_session(phoneNumber)
        return HomeModels.success(message=f"Session with: {phoneNumber} created.")

    @action(name="sendCode", renderer="json", request_method="GET")
    def send_code(self):
        phone_number = self.request.GET["phoneNumber"][1:]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
            asyncio.run,
            wrap.send_code(phone_number)
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
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
            asyncio.run,
            wrap.signin(phone_number=phone_number,
                        phone_code_hash=phone_code_hash,
                        phone_code=phone_code)
        ).result()
        if type(result) is dict and SUCCESS_KEY in result:
            return result
        return UserModels.userDetails(result)

    @action(name="qrLogin", renderer="json", request_method="GET")
    def qr_login(self):
        phone_number=self.request.GET["phoneNumber"]
        wrap = cloudygram_api_server.get_tt()
        result = self.pool.submit(
            asyncio.run,
            wrap.qr_login(phone_number)
        ).result()
        self.pool.submit(asyncio.run, result.wait())
        return UserModels.success(data=result.url)
