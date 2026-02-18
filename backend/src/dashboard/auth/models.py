import enum
import uuid

from pydantic import BaseModel, EmailStr
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from dashboard.database import Base


class Role(str, enum.Enum):
    supervisor = "supervisor"
    general = "general"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(Enum(Role, name="role"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    role: Role
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
