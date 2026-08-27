from typing import List, TypedDict, Union

from beanie import PydanticObjectId
from fastapi.websockets import WebSocket
from pydantic import BaseModel

from src.exceptions.room_exception import RoomException
from src.schemas.room_schema import RoomCreate
from src.models.user import User
from src.models.room import Room
import re


class ClientMessagePayload(BaseModel):
    content:str

class CompleteMessagePayload(ClientMessagePayload):
    author:str = "N/A"

'''class CommandPayload:
    command:str
    target:RoomClient


class RoomAdminCommands:
    @staticmethod
    async def kick(victim:RoomClient, reason:str):
        await victim.disconnect(reason)

    @staticmethod
    async def ban(victim:RoomClient, reason:str, minutes:int):
        pass 
'''
ROOMS = {}
class RoomClient:
    id:str
    room_id: str
    socket:WebSocket

    def __init__(self, user:User, room_id:str, websocket:WebSocket):
        self.id         = str(user.id)
        self.room_id    = room_id
        self.socket     = websocket
        ROOMS.setdefault(self.room_id, [])
        

    async def check_if_user_is_in_a_room(self):
        for client in self.get_all_clients():
            if client.id == self.id: 
                await self.disconnect("Você ja está em uma sala")

    async def accept(self):
        await self.socket.accept()

        await self.check_if_user_is_in_a_room()

        ROOMS.update({
            self.room_id : [*self.get_all_clients(), self]
        })

    def get_all_clients(self) -> list:
        return ROOMS.get(self.room_id)

    async def broadcast(self, message:CompleteMessagePayload):
        for socket in self.get_all_clients():
           await socket.send_message(message.model_dump_json())

    async def receive_message(self) -> CompleteMessagePayload:
        data    = await self.socket.receive_text()
        message = ClientMessagePayload.model_validate_json(data)
        return CompleteMessagePayload(**message.model_dump(), author = self.id)

    async def disconnect(self, reason:str = "N/A"):
        await self.socket.close(reason=reason)
        ROOMS.update({
            self.room_id: [c for c in self.get_all_clients() if c.id != self.id]
            })
        
    async def send_message(self, message:str):
        return await self.socket.send_text(message)

         

class RoomService:
    @classmethod
    async def user_in_room(cls, user:User) -> Room:
        return await Room.find_one(Room.participants == user)

    @classmethod
    async def connect(cls, user:User, room_id:PydanticObjectId, socket:WebSocket):
        if room := await cls.user_in_room(user):
            raise RoomException(f"Você já está na sala '{room.name}'")
        room = await cls.get_by_id(room_id)
        room.participants.append(user)

    @classmethod
    async def disconnect(cls, user:User):
        room = await cls.user_in_room(user)
        new_participants = []
        for p in room.participants:
            if (participant := await p.fetch()) and participant.id != user.id:
                new_participants.append(participant)

        room.participants = new_participants
        await room.save()
        
    @classmethod
    async def get_by_name(cls, name:str) -> list[Room]:
        search_pttr = re.compile(name, re.IGNORECASE)
        return await Room.find(Room.name == search_pttr)

    @classmethod 
    async def get_by_id(cls, id:PydanticObjectId) -> Room:
        if not (room := await Room.get(id)):
            raise RoomException("Não foi possível encontrar a sala")
        return room

    @classmethod
    async def user_owns_room(cls, user:User, room_id:PydanticObjectId) -> bool:
        return (await cls.get_by_id(room_id)).owner == user

    @classmethod
    async def create_room(cls, user:User, room_data:RoomCreate) -> Room:
        #não pode criar uma salinha se ja estiver em uma
        if (await cls.user_in_room(user)):
            raise RoomException("Você já está conectado(a) em uma sala.")
        return 

    
    @classmethod
    async def delete_room(cls, user:User, id:PydanticObjectId):
        room = await cls.get_by_id(id)
        if await cls.user_owns_room(user, id):
            await room.delete()
            return room
        raise RoomException("Você não tem permissão para excluir essa sala")

    

        