from infrastructure.db.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func, cast
from sqlalchemy.sql.elements import Null
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7
from datetime import datetime
import sqlalchemy as sa


class User(BaseModel):
    id: Mapped[str] = mapped_column(primary_key=True, unique=True, default=str(uuid7()))
    username: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    middle_name: Mapped[str | None]
    deleted_at: Mapped[datetime | None] = mapped_column(
        default=None,
        server_default=Null(),
        type_=TIMESTAMP(timezone=True),
        nullable=True,
    )
    version: Mapped[int]
