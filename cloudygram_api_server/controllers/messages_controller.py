from cloudygram_api_server.models import UserModels, TtModels
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.telethon.exceptions import *
from cloudygram_api_server.scripts import jres
from pyramid_handlers import action
from pyramid.request import Request
import asyncio, concurrent.futures
from typing import List, Union


class MessagesController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.expected_errors = (TTGenericException, TTUnathorizedException, Exception)

    def handle_exceptions(self, exception: Union[TTGenericException, TTUnathorizedException, Exception]) -> dict:
        if type(exception) is TTGenericException or type(exception) is Exception:
            return jres(UserModels.failure(str(exception)), status=500)
        elif type(exception) is TTUnathorizedException:
            return jres(UserModels.failure(str(exception)), status=401)
        else:
            return jres(UserModels.failure(str(exception)), status=500)

    @action(name="getMessages", renderer="json", request_method="GET")
    def get_messages_req(self):
        phone_number: str = self.request.matchdict["phoneNumber"][1:]
        try:
            result = self.pool.submit(
                    asyncio.run,
                    get_messages(phone_number)
                    ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(TtModels.message_list(result), status=200)

    @action(name="deleteMessages", renderer="json", request_method="POST")
    def delete_messages_req(self):
        phone_number: str = self.request.matchdict["phoneNumber"][1:]
        message_ids: List[str] = self.request.json_body["ids"]
        try:
            self.pool.submit(
                asyncio.run,
                delete_messages(phone_number, message_ids)
            ).result()
        except self.expected_errors as exc:
            return self.handle_exceptions(exc)
        return jres(UserModels.success(), status=200)

