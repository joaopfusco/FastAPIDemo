from fastapi_crudrouter import SQLAlchemyCRUDRouter
from db.database import get_db
from models.user import User
from schemas.user_schema import UserSchemaResponse, UserSchemaPayload

router = SQLAlchemyCRUDRouter(
    schema=UserSchemaResponse,
    create_schema=UserSchemaPayload,
    update_schema=UserSchemaPayload,
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"]
)
