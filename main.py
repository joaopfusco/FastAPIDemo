from fastapi import FastAPI
from db.database import create_tables
from routers.user_router import router as user_router

create_tables()

app = FastAPI()

app.include_router(user_router)
