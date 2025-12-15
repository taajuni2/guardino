# api/user_router.py
from fastapi import APIRouter, Depends

from ..api.deps import get_db_session, get_current_user
from ..models.user import User
from ..schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
