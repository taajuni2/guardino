from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .deps import get_db_session
from ..models.user import User
from ..schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    # check if email exists
    res = await db.execute(select(User).where(User.email == payload.email))
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(email=payload.email, name=payload.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get(
    "/{user_id}",
)
def greeting():
    return {"message": "Hello, User!"}
# async def list_users(db: AsyncSession = Depends(get_db_session)):
#     res = await db.execute(select(User).order_by(User.created_at.desc()))
#     return list(res.scalars())
