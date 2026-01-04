from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import select

from .config import APP_NAME, JWT_SECRET
from .database import get_session
from .models import User
from .schemas import UserRead


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

JWT_ALGO = "HS256"
JWT_EXPIRE_HOURS = 12


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "app": APP_NAME,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> UserRead:
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido")

    with get_session() as session:
        user = session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Utilizador inválido")
        return UserRead.model_validate(user)


def require_roles(*roles: str):
    def dependency(user: UserRead = Depends(get_current_user)) -> UserRead:
        if roles and user.role not in roles:
            raise HTTPException(status_code=403, detail="Sem permissões")
        return user

    return dependency
