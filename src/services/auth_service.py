from config import JWT_EXPIRES_IN
from datetime import datetime, timedelta, timezone
from typing import TypedDict, Union
import bcrypt
from beanie import PydanticObjectId
import jwt
from pydantic import EmailStr

from config import JWT_SECRET


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
    def is_strong_password(password: str) -> bool:
        checker = {
            "has_good_length": len(password) >= 8,
            "has_uppercase": False,
            "has_lowercase": False,
            "has_number": False
        }
    
        for char in password:
            if char.islower():
                checker["has_lowercase"] = True
            elif char.isupper():
                checker["has_uppercase"] = True
            elif char.isdigit():
                checker["has_number"] = True

        return all(checker.values())



    
