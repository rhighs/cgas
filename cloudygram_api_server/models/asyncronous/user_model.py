from pydantic import BaseModel
from telethon.tl.types import User
from typing import Optional
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse

class UserData(BaseModel):
    userId : Optional[str]
    username : Optional[str]
    firstName : Optional[str]
    lastName : Optional[str]
    phoneNumber : Optional[str]


class UserBase(BaseResponse, BaseModel):
    data : Optional[UserData]

def set_value(isSuccess: bool, UserDetails: User = None, message: str = None) -> UserBase:
    user = UserBase(isSuccess=isSuccess)
    
    if (not UserDetails is None):
        user.data = UserData(userId=UserDetails.id, 
                            username=UserDetails.username, 
                            firstName=UserDetails.first_name, 
                            lastName=UserDetails.last_name, 
                            phoneNumber=UserDetails.phone)

    if (not message is None):
        user.message = message
    
    return user
