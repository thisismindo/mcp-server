"""Users model
"""
from typing import Optional, List, Dict
from pydantic import BaseModel, UUID4, StrictStr, EmailStr, field_validator
from datetime import datetime
from src.constants import IS_TRUE

class CreateUser(BaseModel):
    """CreateUser basemodel
    """
    username: StrictStr
    email_address: EmailStr
    active: Optional[bool] = IS_TRUE

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UpdateUser(BaseModel):
    """UpdateUser basemodel
    """
    id: UUID4
    email_address: EmailStr

class UserResponse(BaseModel):
    """UserResponse basemodel
    """
    id: UUID4
    username: StrictStr
    email_address: EmailStr
    created_at: datetime
    updated_at: datetime

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
