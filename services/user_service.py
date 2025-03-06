from services.base_service import BaseService
from models.user import User
from schemas.user_schema import UserSchemaResponse, UserSchemaPayload
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserSchemaResponse, UserSchemaPayload]):
    def __init__(self):
        super().__init__(User)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create(self, db, item):
        hashed_password = self.hash_password(item.password)
        db_user = UserSchemaPayload(username=item.username, password=hashed_password)  
        return super().create(db, db_user)
    
    def update(self, db, id, item):
        hashed_password = self.hash_password(item.password)
        db_user = UserSchemaPayload(username=item.username, password=hashed_password)
        return super().update(db, id, db_user)
