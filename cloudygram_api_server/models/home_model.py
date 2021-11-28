from .constants import DEFAULT_SUCCESS, SUCCESS_KEY, MESSAGE_KEY, DEFAULT_FAILURE, SENT_CODE_KEY

class HomeModels:
    @staticmethod
    def success(message=None) -> dict:
        if message != None:
            return {
                SUCCESS_KEY : True,
                MESSAGE_KEY : message
            }
        return DEFAULT_SUCCESS

    @staticmethod
    def failure(message=None) -> dict:
        if message != None:
            return {
                SUCCESS_KEY : False,
                MESSAGE_KEY : message
            }
        return DEFAULT_FAILURE

    @staticmethod
    def sent_code(code) -> dict:
        return {
            SUCCESS_KEY : True,
            SENT_CODE_KEY : code
        }