from fastapi import APIRouter
from src.services.user_service import UserService
from src.entities.user_entity import UserRegistration, UserLogin, UserUpdate
from bson import ObjectId

from src.util.MongoJSONResponse import MongoJSONResponse

user_router = APIRouter(prefix = "/user")

@user_router.get("/")
def get_all_users():
    return UserService.get_all_users()

@user_router.post("/", description="creates user")
def create_user(user: UserRegistration):
    return UserService.create(user)

@user_router.patch("/{id}")
def update_user(data:UserUpdate):
    return UserService.update(data)
    
@user_router.get("/test")
def test():
    return MongoJSONResponse(content=ObjectId())