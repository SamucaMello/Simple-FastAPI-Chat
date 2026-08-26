from beanie import PydanticObjectId

from src.models.user import User
from src.models.room import Room
from src.schemas.message_schema import CreateMessage
from src.models.message import Message

class MessageService:
    @classmethod
    async def create(cls, message_data:CreateMessage) -> Message:
        message = Message(**message_data.model_dump())
        return await message.insert()

    @classmethod
    async def list_by_room(cls, room:Room, page:int, size:int) -> list[Message]:
        skip = (page - 1) * size
        messages = await Message.find_many(
            Message.room == room, 
            skip = skip,
            limit = size
            )
        return messages

    @classmethod
    async def get_by_id(cls, id:PydanticObjectId) -> Message:
        return await Message.get(id)
    
    @classmethod 
    async def delete(cls,user:User, id:PydanticObjectId):
        if (message := await cls.get_by_id(id)).sent_by == user:
            await message.delete()
            return 

