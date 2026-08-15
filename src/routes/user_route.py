from beanie import PydanticObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.user_service import UserService
from src.schemas.user_schema import UserRegistration, UserLogin, UserUpdate

user_router = APIRouter(prefix = "/user")

@user_router.get("/")
async def get_all_users():
    return await UserService.find_all()

@user_router.post("/register", description="creates user")
async def create_user(user: UserRegistration):
    return JSONResponse(content = {
        "message":""
        })
    return await UserService.create(user)

@user_router.post("/login", description="autentica usuario")
async def login(user:UserLogin):
    return 

@user_router.delete("/{id}")
async def delete_user(id:PydanticObjectId):
    return await UserService.delete(id)

@user_router.put("/{id}")
def update_user(id:PydanticObjectId, data:UserUpdate):
    return UserService.update(data)
    
@user_router.get("/{id}")
async def get_by_id(id:PydanticObjectId):
    return await UserService.get_by_id(id)