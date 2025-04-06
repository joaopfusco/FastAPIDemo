from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserOut, UserIn
from sqlalchemy.orm import Session
from fastapi import Depends
from app.routers.base_router import BaseRouter
from app.services.user_service import UserService

class UserRouter(BaseRouter):
    pass

user_router = UserRouter(
    service=UserService,
    schema=UserOut,
    create_schema=UserIn,
    update_schema=UserIn,
    model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"],
)

@user_router.get("/teste/", response_model=dict)
async def test_route():
    return {"message": "Hello, World!"}
