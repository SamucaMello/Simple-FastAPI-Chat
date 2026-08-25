from typing import List

from beanie import Document, Link
from pydantic import Field

from src.models.user import User

class Room(Document):
    name: str                       = Field(max_length=32, min_length=1)
    owner: Link[User]
    max_capacity: int               = Field(ge=1, le=10)
    participants: List[Link[User]]  = []
