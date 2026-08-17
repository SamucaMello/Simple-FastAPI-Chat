from beanie import PydanticObjectId
from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from src.services.user_service import UserService
from src.schemas.user_schema import UserRegistration, UserLogin, UserUpdate
from src.util.api_response import ApiResponse

user_router = APIRouter(prefix = "/user")

@user_router.get("/")
async def get_all_users():
    return await UserService.find_all()

@user_router.post("/register", description="creates user")
async def create_user(user: UserRegistration):
    new_user = await UserService.create(user)
    return {"message":"Usuario criado com sucesso!", "user": new_user}


@user_router.post("/login", description="autentica usuario")
async def login(user:UserLogin):
    token = await UserService.login(user)
    return JSONResponse({
        "message": "Logado com sucesso!",
        "token":token
    })

@user_router.delete("/{id}")
async def delete_user(id:PydanticObjectId):
    deleted_user = await UserService.delete(id)
    return JSONResponse({
        "message": f"Usuario {deleted_user} apagado"
    })

@user_router.put("/{id}")
def update_user(id:PydanticObjectId, data:UserUpdate):
    return UserService.update(data)
    
@user_router.get("/{id}")
async def get_by_id(id:PydanticObjectId):
    return await UserService.get_by_id(id)

@user_router.websocket("/oi")
async def socket(websocket:WebSocket):
    pass