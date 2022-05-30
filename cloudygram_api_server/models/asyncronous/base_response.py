from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    isSuccess: bool
    message: Optional[str]