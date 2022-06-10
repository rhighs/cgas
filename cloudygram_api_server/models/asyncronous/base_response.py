from pydantic import BaseModel, ClassError
from typing import Optional

class BaseResponse(BaseModel):
    isSuccess: bool
    message: Optional[str]

class BaseResponseData(BaseResponse, BaseModel):
    data: str
