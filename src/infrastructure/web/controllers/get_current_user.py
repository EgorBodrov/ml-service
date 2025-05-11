from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from pydantic import ValidationError

from src.utils import decode_access_token
from src.core.entities.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/sign_in")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    try:
        user = User(id=payload["sub"], name=payload["name"], email=payload["email"], hashed_password="")
        return user
    except (KeyError, ValidationError):
        raise HTTPException(status_code=401, detail="Invalid token payload")
