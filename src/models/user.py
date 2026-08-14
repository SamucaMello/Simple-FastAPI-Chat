from beanie import Document
from datetime import datetime

from pydantic import EmailStr, Field

class User(Document):
    name:str
    email:EmailStr
    password:str
    created_at:datetime = Field(default_factory=datetime.now)
    