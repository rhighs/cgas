from pyramid_handlers               import action
from pyramid.request                import Request
from pyramid.httpexceptions         import HTTPUnauthorized
from cloudygram_api_server.models   import UserModels, TtModels
from telethon.tl.types              import MessageMediaDocument
from telethon.tl.patched            import Message
from cloudygram_api_server.scripts  import jres
import asyncio, concurrent.futures
import cloudygram_api_server

class MessagesController(object):
    __autoexpose__ = None

    def __init__(self, request):
        self.request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.wrap = cloudygram_api_server.get_tt()

    @action(name="getMessages", renderer="json", request_method="GET")
    def get_messages(self):
        phone_number= self.request.matchdict["phoneNumber"][1:]
        self.wrap.create_session(phone_number) 
        result = self.pool.submit(
                asyncio.run,
                self.wrap.get_messages(phone_number)
                ).result()
        return jres(TtModels.message_list(result), status=200)
