from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.hash import argon2

from dashboard.config import settings


def hash_password(password: str) -> str:
    return argon2.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return argon2.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> str:
    payload = jwt.decode(
        token=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
    )
    return payload["sub"]
