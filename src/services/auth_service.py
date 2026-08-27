from config import JWT_EXPIRES_IN
from datetime import datetime, timedelta, timezone
from typing import TypedDict, Union
import bcrypt
from beanie import PydanticObjectId
import jwt
from pydantic import EmailStr
from fastapi import Request
from config import JWT_SECRET
from models.user import User
from src.services.user_service import UserService
from src.exceptions.auth_exception import AuthException


class AccessTokenData(TypedDict):
    id:Union[PydanticObjectId, str]
    email:EmailStr



class AuthService:
    @staticmethod
    def encode_password(original_password:str, salts:int = 12) -> str:
        salt                = bcrypt.gensalt(salts)
        password            = original_password.encode()
        encoded_password    = bcrypt.hashpw(password, salt)
        return encoded_password.decode()

    @staticmethod
    def compare_password(original_password:str, encoded_password:str) -> bool:
        return bcrypt.checkpw(original_password.encode(), encoded_password.encode())
    
    @staticmethod
    def create_access_token(data:AccessTokenData):
        expiration_date = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRES_IN)
        pl = {"exp":expiration_date, **data}
        return jwt.encode(pl, JWT_SECRET, algorithm="HS256")
    
    @staticmethod
    def decode_access_token(token:str) -> Union[dict, AccessTokenData]:
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthException("Token Expirado.")
    
    @staticmethod
    def is_strong_password(password:str):
        return True


    @classmethod
    async def get_user_on_header(cls, request:Request) -> User:
        decoded_token = cls.decode_access_token( request.headers.get("authorization", "") )
        return await UserService.get_by_id( decoded_token["id"] ) 
