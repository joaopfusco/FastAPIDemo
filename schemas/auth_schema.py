from pydantic import BaseModel
from schemas.user_schema import UserSchemaResponse

class LoginSchemaPayload(BaseModel):
    username: str
    password: str

class LoginSchemaResponse(BaseModel):
    token: str
    user: UserSchemaResponse