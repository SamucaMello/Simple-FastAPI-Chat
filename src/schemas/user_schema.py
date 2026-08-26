from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId


class UserOut(BaseModel):
    name: str 
    #da p colocar o campo do email tb 

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