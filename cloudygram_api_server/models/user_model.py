from .constants import DEFAULT_SUCCESS, SUCCESS_KEY, MESSAGE_KEY, DATA_KEY, DEFAULT_FAILURE
from telethon.tl.types import User
from typing import Any


class UserModels:
    @staticmethod
    def success(message: str = None, data: Any = None) -> dict:
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
        elif data != None:
            return {
                SUCCESS_KEY : True,
                DATA_KEY : data,
            }
        return DEFAULT_SUCCESS

    @staticmethod
    def failure(message: str = None) -> dict:
        if message != None:
            return {
                SUCCESS_KEY: False,
                MESSAGE_KEY: message
            }
        return DEFAULT_FAILURE

    @staticmethod
    def userDetails(userDetails: User) -> dict:
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

    @staticmethod
    def unauthorized() -> dict:
        return {
            SUCCESS_KEY: False,
            MESSAGE_KEY: "Invalid phone number or session expired!"
        }