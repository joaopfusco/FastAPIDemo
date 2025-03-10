from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from decouple import config
from keycloak import KeycloakOpenID
from jose import jwt, JWTError
from fastapi.encoders import jsonable_encoder

KEYCLOAK_URL = config("KEYCLOAK_URL")
KEYCLOAK_REALM = config("KEYCLOAK_REALM")
KEYCLOAK_AUDIENCE = config("KEYCLOAK_AUDIENCE")
KEYCLOAK_CLIENT_ID = config("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = config("KEYCLOAK_CLIENT_SECRET")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    realm_name=KEYCLOAK_REALM,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{keycloak_openid.public_key()}"
            "\n-----END PUBLIC KEY-----"
        )
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=KEYCLOAK_AUDIENCE,
            options={"verify_aud": True}
        )
        username = decoded_token.get("preferred_username")
        if username is None:
            raise HTTPException(status_code=403, detail="Token inválido")
        return {"username": username}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )