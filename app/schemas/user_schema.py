from pydantic import BaseModel
from app.schemas.entity_schema import EntitySchema

class UserCreate(BaseModel):
    username: str
    password: str

class UserSchema(EntitySchema, UserCreate):
    pass