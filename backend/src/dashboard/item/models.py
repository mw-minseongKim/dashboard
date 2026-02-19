import uuid

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from dashboard.database import Base


class Item(Base):
    __tablename__ = "items"

    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)


class ItemRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ItemDelete(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
