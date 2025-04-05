from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from decouple import config
# from app.db.database import create_tables
from app.configs.keycloak_config import get_current_user, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET
from app.routers.user_router import user_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_tables()
#     yield

debug = config("DEBUG", cast=bool, default=True)

app = FastAPI(
    # lifespan=lifespan,
    dependencies=[Depends(get_current_user) if not debug else Depends(lambda: None)],
    security=[{"oauth2": []} if not debug else None],
    swagger_ui_init_oauth={
        "clientId": KEYCLOAK_CLIENT_ID,
        "clientSecret": KEYCLOAK_CLIENT_SECRET,
        "appName": "Keycloak Auth",
        "scopes": "openid profile email"
    }
)

app.include_router(user_router)
