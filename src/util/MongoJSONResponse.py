from fastapi.responses import JSONResponse
import json
from mongoengine import QuerySet, Document
from bson import ObjectId

class MongoJSONResponse(JSONResponse):

    def __init__(self, content, status_code:int = 200, *args, **kwargs):
        super().__init__(
            status_code = status_code,
            content = self._convert(content), 
            *args,
            **kwargs)

    @classmethod
    def _convert(cls, value):
                if isinstance(value, QuerySet):
                    return [cls._convert(item) for item in value]
        
                if isinstance(value, Document):
                    return cls._convert(value.to_mongo().to_dict())
        
                if isinstance(value, ObjectId):
                    return str(value)
        
                if isinstance(value, dict):
                    return {
                        key: cls._convert(val)
                        for key, val in value.items()
                    }
        
                if isinstance(value, (list, tuple)):
                    return [cls._convert(item) for item in value]
        
                return value
            
            
