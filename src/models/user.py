"""Users model
"""
from typing import Optional, List, Dict
from pydantic import BaseModel
from src.constants import IS_TRUE

class CreateUser(BaseModel):
    """CreateUser basemodel
    """
    username: str
    email_address: str
    active: Optional[bool] = IS_TRUE

class UpdateUser(BaseModel):
    """UpdateUser basemodel
    """
    id: str
    email_address: str

class UserResponse(BaseModel):
    """UserResponse basemodel
    """
    id: str
    username: str
    email_address: str
    created_at: str
    updated_at: str

class UpdateUserResponse(BaseModel):
    """UpdateUserResponse basemodel
    """
    status: bool
    message: List[str]
    response: UserResponse

class SignupResponse(BaseModel):
    """SignupResponse basemodel
    """
    status: bool
    message: List[str]
    response: UserResponse

class UserDefaultResponse(BaseModel):
    """UserDefaultResponse basemodel
    """
    status: bool
    message: List[str]
    response: Dict
