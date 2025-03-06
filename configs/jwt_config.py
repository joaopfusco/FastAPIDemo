from fastapi import Depends
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from decouple import config

class Settings(BaseModel):
    authjwt_secret_key: str = config("SECRTE_KEY")
    authjwt_access_token_expires: int = 3600 * 5

@AuthJWT.load_config
def get_config():
    return Settings()

def authentication(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()