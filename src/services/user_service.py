from src.entities.user_entity import UserRegistration, UserLogin, UserUpdate

class UserService:
    @classmethod 
    def create(cls, user:UserRegistration):
        pass 

    @classmethod
    def login(cls, user:UserLogin):
        pass 

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