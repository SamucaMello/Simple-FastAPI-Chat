from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from beanie import init_beanie
from src.database.db import DatabaseManager
import uvicorn
from src.routes.user_route import user_router



from config import BEANIE_MODELS

@asynccontextmanager
async def lifespan(app:FastAPI):
    DatabaseManager.init_client()
    await init_beanie(DatabaseManager.get_database(), document_models = BEANIE_MODELS)
    yield 
    await DatabaseManager.close_client()


app = FastAPI(
    title = "Websocket Chat",
    lifespan=lifespan
)

app.include_router(user_router)




if __name__ == "__main__":
    uvicorn.run(app)