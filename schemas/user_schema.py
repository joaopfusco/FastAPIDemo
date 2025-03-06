from pydantic import BaseModel
from schemas.entity_schema import EntitySchema

class UserSchema(EntitySchema):
    username: str
    password: str

class LoginSchema(BaseModel):
    token: str
    user: UserSchema
