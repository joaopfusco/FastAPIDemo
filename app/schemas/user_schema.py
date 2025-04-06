from pydantic import BaseModel
from app.schemas.entity_schema import EntitySchema

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(EntitySchema, UserIn):
    pass