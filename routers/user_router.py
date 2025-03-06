from fastapi_crudrouter import SQLAlchemyCRUDRouter
from db.database import get_db
from models.user import User
from schemas.user_schema import UserSchema
from routers.base_router import BaseRouter
from services.user_service import UserService

# router = SQLAlchemyCRUDRouter(
#     schema=UserSchema,
#     create_schema=UserSchema,
#     update_schema=UserSchema, 
#     db_model=User,
#     db=get_db,
#     prefix="/users",
#     tags=["Users"]
# )

class UserRouter(BaseRouter[User, UserService, UserSchema]):
    def __init__(self):
        super().__init__(model=User, service=UserService, prefix="/users", tag="Users")

router = UserRouter().get_router()