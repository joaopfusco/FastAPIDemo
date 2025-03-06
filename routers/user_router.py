from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user_schema import LoginSchema, UserSchema
from routers.base_router import BaseRouter
from services.user_service import UserService

router = SQLAlchemyCRUDRouter(
    schema=UserSchema,
    create_schema=UserSchema,
    update_schema=UserSchema, 
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"]
)

service = UserService()

@router.get("", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return service.get_all(db)

@router.post("", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    return service.create(db, user)

@router.put("/{item_id}", response_model=UserSchema)
def update_user(item_id: int, user: UserSchema, db: Session = Depends(get_db)):
    return service.update(db, item_id, user)

@router.post("/login", response_model=LoginSchema)
def login(user: UserSchema, db: Session = Depends(get_db)):
    return