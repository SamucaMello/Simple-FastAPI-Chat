from pymongo import AsyncMongoClient
from config import MONGO_URI

class DatabaseManager:
    _client:AsyncMongoClient = None
    _name = "minha_db"
    
    @classmethod
    def init_client(cls):
        cls._client = AsyncMongoClient(MONGO_URI)
        
    @classmethod
    async def close_client(cls):
        await cls._client.close()

    @classmethod
    def get_database(cls):
        return cls._client[cls._name]