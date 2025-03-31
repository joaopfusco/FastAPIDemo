from app.database import get_db
from app.models import User
from app.schemas import UserSchemaResponse, UserSchemaPayload
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter as CRUDRouter

user_router = CRUDRouter(
    schema=UserSchemaResponse, 
    create_schema=UserSchemaPayload,
    update_schema=UserSchemaPayload,
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"],
)

@user_router.get("", response_model=list[UserSchemaResponse])
def get_all_users(db: Session = Depends(get_db)):
    print("override no getAll")
    users = db.query(User).all()
    return users
