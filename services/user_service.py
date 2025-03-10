from services.base_service import BaseService
from models.user import User
from schemas.user_schema import UserSchemaResponse, UserSchemaPayload

class UserService(BaseService[User, UserSchemaResponse, UserSchemaPayload]):
    def __init__(self):
        super().__init__(User)
