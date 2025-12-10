from datetime import datetime
from app.schemas.auth_schema import UserCreate

def user_document(user: UserCreate, hashed_password: str):
    return {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "created_at": datetime.utcnow()
    }
