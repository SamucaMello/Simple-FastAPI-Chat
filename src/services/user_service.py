

from fastapi import Request

from config import JWT_SECRET
from src.exceptions.auth_exception import AuthException
from src.schemas.pagination_schema import PaginationParams

from src.exceptions.user_exception import UserException
from src.models.user import User
from src.schemas.user_schema import UserOut, UserRegistration, UserLogin, UserResponse, UserUpdate
import jwt
import bcrypt
from beanie import PydanticObjectId
from datetime import datetime, timezone, timedelta
from src.services.auth_service import AuthService




class UserService:
    @classmethod 
    async def create(cls, user:UserRegistration) -> User:
        if not AuthService.is_strong_password(user.password):
            raise AuthException("Senha muito fraca")
        user.password = AuthService.encode_password(user.password)
        
        
        if await User.find_one(User.email == user.email):
            raise UserException("Esse e-mail já está cadastrado")
        
        new_user    = User( **user.model_dump() )
        added_user  = await new_user.insert()
        return UserResponse(**added_user.model_dump())
        
        
    @classmethod
    async def find_all(cls, pagination:PaginationParams):
        skip = (pagination.page - 1) * pagination.size
        return await User.find_all(projection_model=UserOut, skip = skip, limit = pagination.size ).to_list()
        
    @classmethod
    async def login(cls, user:UserLogin):
        if (found_user := await User.find_one(User.email == user.email)) and AuthService.compare_password(user.password, found_user.password):
            return AuthService.create_access_token({"id": str(found_user.id)})
        raise UserException("Verifique o e-mail ou a senha e tente novamente mais tarde")
        

    @classmethod
    async def update(cls, id:PydanticObjectId, user:UserUpdate):
        user_found = await User.find_one(User.id == id)
        if user_found:
            for attr, value in user.model_fields.items():
                setattr(user_found, attr, value)
                
            user_found.replace()
            return user_found

    @classmethod
    async def delete(cls, id:PydanticObjectId):
        user = await cls.get_by_id(id)
        user.delete()

    @classmethod
    async def get_by_id(cls, id:PydanticObjectId):
        if user := await User.get(id):
            return user
        raise UserException("Usuário não encontrado")

    @classmethod
    async def get_user_on_header(cls, request:Request) -> User:
        decoded_token = cls.decode_access_token( request.headers.get("authorization", "") )
        return await UserService.get_by_id( decoded_token["id"] ) 
    
    
