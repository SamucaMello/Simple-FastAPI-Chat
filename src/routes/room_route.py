from fastapi import APIRouter
from fastapi.websockets import WebSocket
from fastapi.requests import Request

from src.services.room_service import RoomClient
from src.services.user_service import UserService, UserAuthService
room_router = APIRouter(prefix="/room")


@room_router.websocket("/")
async def room(websocket:WebSocket, token:str = "", room:str = ""):
    data        = UserAuthService.decode_access_token(token)
    user        = await UserService.get_by_id(data.get("id"))

    client = RoomClient(user, room, websocket)
    await client.accept()

    try:
        while True:
            data = await client.receive_message()
            await client.broadcast(data)
    except Exception as ex:
        print(f"{ex}")
    finally:
        await client.disconnect()
   

    