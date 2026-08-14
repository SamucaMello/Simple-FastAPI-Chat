from config import JWT_SECRET
from src.exceptions.user_exception import UserException
from src.models.user import User
from src.schemas.user_schema import UserRegistration, UserLogin, UserUpdate
import jwt
import bcrypt
from datetime import datetime, timezone, timedelta


class UserAuthService:
    @staticmethod
    def encode_password(original_password:str, salts:int = 12) -> str:
        salt                = bcrypt.gensalt(salts)
        password            = original_password.encode()
        encoded_password    = bcrypt.hashpw(password, salt)
        return str(encoded_password)

    @staticmethod
    def compare_password(original_password:str, encoded_password:str) -> bool:
        return bcrypt.checkpw(original_password.encode(), encoded_password.encode())
    
    
    @staticmethod
    def create_access_token(data:dict):
        pl = data.copy()
        expiration_date = datetime.now(timezone.utc) + timedelta(hours=12)
        pl.update({"exp":expiration_date})
        return jwt.encode(pl, JWT_SECRET, algorithm="HS256")
    
    @staticmethod
    def decode_access_token(token:str):
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    
    @staticmethod
    def is_strong_password(password:str):
        return True
        

class UserService:
    @classmethod 
    async def create(cls, user:UserRegistration):
        user.password = UserAuthService.encode_password(user.password)
        
        if await User.find_one(User.email == user.email):
            raise UserException("Esse e-mail já está cadastrado")
        
        new_user = User(
            name      = user.name,
            email     = user.email,
            password  = user.password
            )
        await new_user.insert()
        
    @classmethod
    async def login(cls, user:UserLogin):
        if (found_user := await User.find_one(User.email == user.email)) and UserAuthService.compare_password(user.password, found_user.password):
            return UserAuthService.create_access_token({"id": found_user.id})
        raise UserException("Verifique o e-mail ou a senha e tente novamente mais tarde")
        

    @classmethod
    def update(cls, id:str, user:UserUpdate):
        pass

    @classmethod
    def delete(cls, id:str):
        pass 

    @classmethod
    def get_all(cls):
        pass 

    @classmethod
    def get_by_id(cls):
        pass 