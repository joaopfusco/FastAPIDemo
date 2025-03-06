from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi_jwt_auth.exceptions import MissingTokenError
from configs.jwt_config import authentication
from db.database import create_tables
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router

app = FastAPI()

create_tables()

@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Missing access token in request header."}
    )

bearer_scheme = HTTPBearer()

app.include_router(auth_router)
app.include_router(user_router, dependencies=[Depends(authentication), Depends(bearer_scheme)])