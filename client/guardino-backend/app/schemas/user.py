from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    name: str

    class Config:
        from_attributes = True  # Pydantic v2: erlaubt ORM -> Schema
