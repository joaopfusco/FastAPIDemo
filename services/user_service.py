from services.base_service import BaseService
from models.user import User
from schemas.user_schema import UserSchema

class UserService(BaseService[User, UserSchema]):
    def __init__(self):
        super().__init__(User)
