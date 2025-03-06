from services.base_service import BaseService
from models.user import User
from schemas.user_schema import UserSchema, UserCreateSchema

class UserService(BaseService[User, UserSchema, UserCreateSchema]):
    def __init__(self):
        super().__init__(User)
