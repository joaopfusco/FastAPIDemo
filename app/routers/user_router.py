from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserSchema, UserCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from app.routers.base_router import BaseRouter
from app.services.user_service import UserService

class UserRouter(BaseRouter):
    pass

user_router = UserRouter(
    service=UserService,
    schema=UserSchema,
    create_schema=UserCreate,
    update_schema=UserCreate,
    model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"],
)

@user_router.get("/teste/", response_model=dict)
def test_route(session: Session = Depends(get_db)):
    return {"message": "Hello, World!"}
