from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, date

ALLOWED_GENDERS = ["male", "female", "other"]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    date_of_birth: datetime
    gender: str 

    # NAME VALIDATION
    @field_validator("name")
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if not all(x.isalpha() or x.isspace() for x in v):
            raise ValueError("Name must contain only letters and spaces")
        return v

    # PASSWORD VALIDATION
    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

    # GENDER VALIDATION
    @field_validator("gender")
    def validate_gender(cls, v:str):
        sex = v.lower()
        if sex not in ALLOWED_GENDERS:
            raise ValueError(f"Gender must be one of: {ALLOWED_GENDERS}")
        return sex

    # AGE VALIDATION
    @field_validator("date_of_birth")
    def validate_age(cls, v: datetime):
        today = date.today()
        dob = v.date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        return v


class UserOut(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: datetime
    gender: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
