from pydantic import BaseModel
from telethon.tl.types import User
from typing import Optional
from cloudygram_api_server.models.asyncronous.base_response import BaseResponse

class HomeResponse(BaseResponse, BaseModel):
    sendCode: Optional[str]