from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth_schema import UserCreate, UserOut, LoginSchema
from app.schemas.token_schema import Token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.user_repository import find_user_by_email, create_user
from app.utils.hashing import hash_password, verify_password
from app.core.security import create_access_token
from app.models.auth_model import user_document
from jose import JWTError, jwt
from app.core.config import settings

router = APIRouter()
auth_scheme = HTTPBearer()

# REGISTER
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    # CHECK IF EMAIL EXISTS
    existing_user = await find_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # HASH PASSWORD
    hashed_pw = hash_password(user.password)

    # CREATE DOCUMENT
    user_doc = user_document(user, hashed_pw)
    new_user = await create_user(user_doc)

    # RETURN SAFE OUTPUT
    return UserOut(
        name=new_user["name"],
        email=new_user["email"],
        gender=new_user["gender"],
        date_of_birth=new_user["date_of_birth"]
    )

# LOGIN
@router.post("/login", response_model=Token)
async def login(credentials: LoginSchema):
    user = await find_user_by_email(credentials.email)

    # GENERIC ERROR (SECURITY BEST PRACTICE)
    generic_error = HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

    # EMAIL NOT FOUND
    if not user:
        raise generic_error

    # PASSWORD INCORRECT
    if not verify_password(credentials.password, user["password"]):
        raise generic_error

    # CREATE JWT
    token = create_access_token({"sub": user["email"]})

    return Token(access_token=token, token_type="bearer")


# GET CURRENT USER FROM TOKEN
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return email

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

@router.get("/me")
async def profile(current_user: str = Depends(get_current_user)):
    return {"current_user": current_user}
