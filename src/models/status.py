"""Status model
"""
from typing import List, Dict
from pydantic import BaseModel

class StatusResponse(BaseModel):
    """StatusResponse basemodel
    """
    status: bool
    message: List[str]
    response: Dict
