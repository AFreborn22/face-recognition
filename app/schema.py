from pydantic import BaseModel

class FaceResponse(BaseModel):
    id: int
    name: str

class RegisterRequest(BaseModel):
    name: str