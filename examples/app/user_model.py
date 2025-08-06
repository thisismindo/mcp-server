from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class CreateUser(BaseModel):
    """
    CreateUser basemodel
    """
    username: str
    email_address: str
    active: Optional[bool] = True

class UpdateUser(BaseModel):
    """
    UpdateUser basemodel
    """
    id: str
    email_address: str

class UserResponse(BaseModel):
    """
    UserResponse basemodel
    """
    id: str
    username: str
    email_address: str
    created_at: str
    updated_at: str

class StatusResponse(BaseModel):
    """
    StatusResponse basemodel
    """
    status: bool
    message: List[str]
    response: Dict[str, Any]

class SignupResponse(BaseModel):
    """
    SignupResponse basemodel
    """
    status: bool
    message: List[str]
    response: UserResponse

class UpdateUserResponse(BaseModel):
    """
    UpdateUserResponse basemodel
    """
    status: bool
    message: List[str]
    response: UserResponse

class UserDefaultResponse(BaseModel):
    """
    UserDefaultResponse basemodel
    """
    status: bool
    message: List[str]
    response: Dict[str, Any]
