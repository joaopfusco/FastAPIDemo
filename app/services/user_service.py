from sqlalchemy.orm import Session
from app.services.base_service import BaseService

class UserService(BaseService):
    def get(self, session: Session):
        print("Override no get")
        return super().get(session)
