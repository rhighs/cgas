from .constants import SUCCESS_KEY, MESSAGE_KEY, DATA_KEY
from cloudygram_api_server.scripts  import CGMessage
from typing import List

class TtModels:
    @staticmethod
    def sing_in_failure(message) -> dict:
        return {
            SUCCESS_KEY : False,
            MESSAGE_KEY : message
        }

    @staticmethod
    def send_code_failure(message) -> dict:
        return {
            SUCCESS_KEY : False,
            MESSAGE_KEY : message
        }

    @staticmethod
    def message_list(messages) -> dict:
        mapped_messages: List[str] = []
        for m in messages:
            mapped_messages.append(CGMessage.map_from_tt(m))
        return {
            SUCCESS_KEY: True,
            DATA_KEY: mapped_messages
        }
