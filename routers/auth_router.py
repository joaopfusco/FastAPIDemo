from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from schemas.auth_schema import LoginSchemaPayload, LoginSchemaResponse
from models.user import User
from db.database import get_db
from fastapi.encoders import jsonable_encoder
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])

service = UserService()

@router.post("/login", response_model=LoginSchemaResponse)
def login(data: LoginSchemaPayload, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user or not service.verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = Authorize.create_access_token(subject=str(user.id), expires_time=3600 * 5)

    return jsonable_encoder(LoginSchemaResponse(token=token, user=user))
