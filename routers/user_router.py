from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user_schema import UserSchemaResponse, UserSchemaPayload
from services.user_service import UserService
from fastapi.encoders import jsonable_encoder

router = SQLAlchemyCRUDRouter(
    schema=UserSchemaResponse,
    create_schema=UserSchemaPayload,
    update_schema=UserSchemaPayload,
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"]
)

service = UserService()

@router.post("", response_model=UserSchemaResponse)
def create(user: UserSchemaPayload, db: Session = Depends(get_db)):
    created_user = service.create(db, user)
    return jsonable_encoder(created_user)

@router.put("/{item_id}", response_model=UserSchemaResponse)
def update(item_id: int, user: UserSchemaPayload, db: Session = Depends(get_db)):
    updated_user = service.update(db, item_id, user)
    return jsonable_encoder(updated_user)
