import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dashboard.auth.models import Role, User, UserCreate
from dashboard.auth.utils import hash_password


async def get_user_by_email(*, email: str, session: AsyncSession) -> User | None:
    return await session.scalar(select(User).where(User.email == email))


async def get_user_by_id(*, user_id: uuid.UUID, session: AsyncSession) -> User | None:
    return await session.scalar(select(User).where(User.id == user_id))


async def create_user(*, user_in: UserCreate, session: AsyncSession) -> User:
    hashed_password = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        role=Role.general,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
