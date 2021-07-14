from .constants                     import SUCCESS_KEY, MESSAGE_KEY, DATA_KEY
from cloudygram_api_server.scripts  import CGMessage

class TtModels:
    @staticmethod
    def sing_in_failure(message):
        return {
            SUCCESS_KEY : False,
            MESSAGE_KEY : message
        }

    @staticmethod
    def send_code_failure(message):
        return {
            SUCCESS_KEY : False,
            MESSAGE_KEY : message
        }

    @staticmethod
    def message_list(messages):
        message_list = []
        for m in messages:
            message_list.append(CGMessage.map_from_tt(m))
        return {
            SUCCESS_KEY: True,
            DATA_KEY: message_list
        }
