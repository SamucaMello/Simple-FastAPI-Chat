from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union

class ApiResponse:
    def __init__(self, message:str, status_code:int = 200, **kwargs, ):
        return JSONResponse(content = {
            "message":message,
             **kwargs   
            }, 
            status_code= status_code
                )
