from fastapi import FastAPI
import uvicorn

from src.routes.user_route import user_router



app = FastAPI(
    title = "Websocket Chat"
)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app)