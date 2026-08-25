from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    name:str 
    max_capacity: int = Field(ge=1, le=10)

class RoomUpdate(RoomCreate):
    pass 

