from .constants import SUCCESS_KEY, MESSAGE_KEY

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