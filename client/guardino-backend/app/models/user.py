
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    user_id: int
    username: str
    email: EmailStr
    is_admin: bool
    last_activity: str
