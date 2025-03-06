from pydantic import BaseModel
from datetime import datetime
from schemas.entity_schema import EntitySchema

class UserSchemaPayload(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserSchemaResponse(EntitySchema, UserSchemaPayload):
    pass