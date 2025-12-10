# from fastapi import APIRouter, Depends, HTTPException
# from jose import JWTError, jwt
# from app.core.config import settings

# router = APIRouter()

# def get_current_user(token: str):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload["sub"]
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

# @router.get("/me")
# async def profile(token: str):
#     return {"current_user": get_current_user(token)}
