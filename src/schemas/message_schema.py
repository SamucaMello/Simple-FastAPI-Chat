from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class CreateMessage(BaseModel):
    content:str                 = Field(max_length=250, min_length=1)
    sent_by:PydanticObjectId
    room:PydanticObjectId
    