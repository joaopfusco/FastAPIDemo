from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.database import create_tables
from app.configs import get_current_user, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET
from app.routers import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(get_current_user)],
    security=[{"oauth2": []}],
    swagger_ui_init_oauth={
        "clientId": KEYCLOAK_CLIENT_ID,
        "clientSecret": KEYCLOAK_CLIENT_SECRET,
        "appName": "Keycloak Auth",
        "scopes": "openid profile email"
    }
)

app.include_router(user_router)