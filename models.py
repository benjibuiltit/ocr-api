from pydantic import BaseModel

class ResponseModel(BaseModel):
    text: str
