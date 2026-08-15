from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from beanie import init_beanie
from fastapi.responses import JSONResponse
from src.database.db import DatabaseManager
import uvicorn
from src.routes.user_route import user_router
from src.exceptions.base_exception import BaseException

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


@app.exception_handler(BaseException)
def common_handler(request:Request, exc:BaseException):
    return JSONResponse(content = str(exc), status_code = exc.status_code)


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app)