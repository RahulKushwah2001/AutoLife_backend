from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.schemas.auth_schema import UserCreate, LoginSchema
from app.schemas.token_schema import AccessToken, Token
from app.db.user_repository import find_user_by_email, create_user
from app.utils.hashing import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token
from app.models.auth_model import user_document
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

# REGISTER
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    # CHECK IF EMAIL EXISTS
    if await find_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)
    user_doc = user_document(user, hashed_password)
    new_user = await create_user(user_doc)

    access_token = create_access_token(
        {"sub": new_user["email"], "type": "access"}
    )
    refresh_token = create_refresh_token(
        {"sub": new_user["email"], "type": "refresh"}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# LOGIN
@router.post("/login", response_model=Token)
async def login(credentials: LoginSchema):
    user = await find_user_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {"sub": user["email"], "type": "access"}
    )
    refresh_token = create_refresh_token(
        {"sub": user["email"], "type": "refresh"}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# REFRESH TOKEN
@router.post("/refresh", response_model=AccessToken)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        access_token = create_access_token(
            {"sub": email, "type": "access"}
        )

        return AccessToken(access_token=access_token)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

# GET CURRENT USER
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return email

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

@router.get("/me")
async def profile(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
