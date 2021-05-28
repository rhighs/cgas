from .constants import *

class PyroModels:
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