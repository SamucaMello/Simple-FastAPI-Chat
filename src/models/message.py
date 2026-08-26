from datetime import datetime

from beanie import Document, Link
from pydantic import Field, BaseModel

from src.models.room import Room
from src.models.user import User

class Message(Document):
    content:str              = Field(max_length=250, min_length=1)
    created_at:datetime      = Field(default_factory = datetime.now)
    sent_by:Link[User]      
    room:Link[Room]              
