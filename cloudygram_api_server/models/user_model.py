from .constants     import SUCCESS_KEY, MESSAGE_KEY, DATA_KEY, DEFAULT_FAILURE
from telethon.tl.types import User

class UserModels:
    @staticmethod
    def success(message=None, data=None):
        if message != None and data != None:
            return {
                SUCCESS_KEY : True,
                MESSAGE_KEY : message,
                DATA_KEY : data
            }
        elif message != None:
            return {
                SUCCESS_KEY : True,
                MESSAGE_KEY : message,
            }
        return {
            SUCCESS_KEY : True,
            DATA_KEY : data,
        }

    @staticmethod
    def failure(message=None):
        if message != None:
            return {
                SUCCESS_KEY: False,
                MESSAGE_KEY: message
            }
        return DEFAULT_FAILURE

    @staticmethod
    def userDetails(userDetails):
        return {
            SUCCESS_KEY: True,
            DATA_KEY: {
                "userId" : userDetails.id,
                "username" : userDetails.username,
                "firstName" : userDetails.first_name,
                "lastName" : userDetails.last_name,
                "phoneNumber" : userDetails.phone
            }
        }
