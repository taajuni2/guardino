# core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from ..core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    settings.DB_URL,
    echo=(settings.ENV == "dev"),
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency-Funktion für FastAPI, aber kann genauso in anderen Kontexten verwendet werden
async def get_db():
    async with SessionLocal() as session:
        yield session
