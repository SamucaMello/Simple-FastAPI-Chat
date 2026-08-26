from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from beanie import Document, Indexed, Link
from pydantic import Field

from src.models.user import User


class Room(Document):
    name: str                       = Field(max_length=32, min_length=1)
    
    owner: Link[User]

    max_capacity: int               = Field(ge=1, le=10)

    participants: List[Link[User]]  = []
                                        #vai expirar em 2h
    created_at:Annotated[datetime, Indexed(expireAfterSeconds=7200)] = datetime.now
