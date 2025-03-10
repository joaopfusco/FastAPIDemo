from fastapi_crudrouter import SQLAlchemyCRUDRouter
from app.database import get_db
from app.models import User
from app.schemas import UserSchemaResponse, UserSchemaPayload

user_router = SQLAlchemyCRUDRouter(
    schema=UserSchemaResponse,
    create_schema=UserSchemaPayload,
    update_schema=UserSchemaPayload,
    db_model=User,
    db=get_db,
    prefix="/users",
    tags=["Users"]
)

