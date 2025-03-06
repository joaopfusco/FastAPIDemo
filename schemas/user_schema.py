from pydantic import BaseModel
from datetime import datetime
from schemas.entity_schema import EntitySchema

class UserCreateSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserSchema(EntitySchema, UserCreateSchema):
    pass

class LoginSchema(BaseModel):
    token: str
    user: UserSchema
