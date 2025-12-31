from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_token(payload: dict, expires_delta: timedelta):
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_access_token(payload: dict):
    return create_token(
        payload,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

def create_refresh_token(payload: dict):
    return create_token(
        payload,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
