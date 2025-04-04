from pydantic import BaseModel
from app.schemas.entity_schema import EntitySchema

class UserPayload(BaseModel):
    username: str
    password: str

class UserResponse(EntitySchema, UserPayload):
    pass