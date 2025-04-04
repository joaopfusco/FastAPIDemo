from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserResponse, UserPayload
from sqlalchemy.orm import Session
from fastapi import Depends
from app.routers.base_router import BaseRouter

class UserRouter(BaseRouter):
    def get_all(self, session: Session):
        print("Override no getAll")
        return super().get_all(session)

user_router = UserRouter(
    schema=UserResponse,
    create_schema=UserPayload,
    update_schema=UserPayload,
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"],
)

@user_router.get("/teste/", response_model=dict)
def test_route(session: Session = Depends(get_db)):
    return {"message": "Hello, World!"}
