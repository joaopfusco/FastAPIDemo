from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)

    def get(self, session: Session):
        print("Override no get")
        return super().get(session)
