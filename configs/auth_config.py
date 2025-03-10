from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from decouple import config
from jose import jwt, jwk
from jose.exceptions import JWTError
from fastapi.encoders import jsonable_encoder
import httpx

KEYCLOAK_URL = config("KEYCLOAK_URL")
KEYCLOAK_REALM = config("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = config("KEYCLOAK_CLIENT_ID")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
    auto_error=False
)

async def validate_token(token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL)
            response.raise_for_status()
            jwks = response.json()

        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Token missing 'kid' header")

        key_data = next((key for key in jwks["keys"] if key["kid"] == kid), None)
        if not key_data:
            raise HTTPException(status_code=401, detail="Matching key not found in JWKS")

        public_key = jwk.construct(key_data).public_key()

        payload = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            audience=KEYCLOAK_CLIENT_ID
        )

        username = payload.get("preferred_username")
        if not username:
            raise HTTPException(status_code=401, detail="Token missing required claims")

        return jsonable_encoder({ "username": username })

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await validate_token(token)
