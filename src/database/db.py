from pymongo import AsyncMongoClient
from config import MONGO_URI


class DatabaseManager:
    _client:AsyncMongoClient = None
    _name = "minha_db"
    
    @classmethod
    def init_client(cls):
        print("conectando no banco de dados")
        cls._client = AsyncMongoClient(MONGO_URI)
        print("conectado")
        
    @classmethod
    async def close_client(cls):
        print("fechando conexão com banco de dados")
        await cls._client.close()
        print("conexão com bando de dados fechada")

    @classmethod
    def get_database(cls):
        return cls._client[cls._name]