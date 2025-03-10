from fastapi import Depends, FastAPI
from db.database import create_tables
from configs.auth_config import get_current_user
from routers.user_router import router as user_router

app = FastAPI(dependencies=[Depends(get_current_user)])

create_tables()

app.include_router(user_router)