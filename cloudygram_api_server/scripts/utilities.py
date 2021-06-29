from pyramid.response   import Response
from telethon.tl.types  import Message
import                  json

def jres(model, status):
    return Response(json.dumps(model),
                    charset="UTF-8",
                    content_type="application/json",
                    status=status)

class CGMessage:
    def __init__(self, id, from_peer: str, str_content: str):
        self.id_key = "id"
        self.from_key = "from_peer"
        self.content_key = "content"
        self.id = id
        self.from_peer = from_peer
        self.str_content = str_content

    def as_dict(self):
        return {
            "id": self.id,
            "from_peer": self.from_peer,
            "content": self.str_content
        }

    def __setitem__(self, key, item):
        if key == self.id_key:
            self.id = item
        if key == self.from_key:
            self.from_peer = item
        if key == self.content_key:
            self.str_content = item

    def __getitem__(self, key):
        if key == self.id_key:
            return self.id
        if key == self.from_key:
            return self.from_peer
        if key == self.content_key:
            return self.str_content

    @staticmethod
    def map_from_tt(t_message: Message):
        return CGMessage(
                t_message.id,
                t_message.peer_id.user_id,
                t_message.message
                )

