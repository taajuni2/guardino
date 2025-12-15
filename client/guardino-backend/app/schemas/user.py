# schemas/user.py
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    # neu: Plaintext PW kommt nur hier rein

class UserRead(BaseModel):
    email: str
    name: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    name: str
    password: str
