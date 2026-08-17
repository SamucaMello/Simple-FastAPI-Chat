from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId

class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(UserRegistration):
    name:str
    email:str

class UserResponse(BaseModel):
    name:str
    email:EmailStr
    id:PydanticObjectId