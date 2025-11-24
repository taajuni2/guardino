from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..api.deps import get_db_session
from ..models.user import User
from ..schemas.user import LoginRequest, TokenResponse, UserCreate, UserRead
from ..core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    # existiert email schon?
    print(f"Registering user with email: {payload.email}")
    res = await db.execute(select(User).where(User.email == payload.email))
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    # User nach email holen
    res = await db.execute(select(User).where(User.name == payload.name))
    user = res.scalar_one_or_none()

    if not user:
        # gleiche Fehlermeldung wie bei falschem PW -> keine User-Enumeration
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Token bauen, wir nehmen als subject user.id (UUID als string)
    token = create_access_token(str(user.id))

    return TokenResponse(access_token=token)
