import hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..core.config import settings

# Passwort-Hasher (bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Secret + Token Settings
JWT_SECRET = getattr(settings, "JWT_SECRET", "CHANGE_ME_SUPER_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # kannst du in settings legen, wenn du willst


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    sub = subject, z.B. user_id oder email
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": sub,
        "exp": expire,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """
    Rückgabe: Payload dict oder None wenn invalid/expired
    """
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return data
    except JWTError:
        return None
