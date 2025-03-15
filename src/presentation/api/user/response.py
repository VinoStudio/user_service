from pydantic import BaseModel
from datetime import datetime

from domain.user.entities.user import User


class CreateUserResponseSchema(BaseModel):
    user_id: str
    username: str
    created_at: datetime
    is_deleted: bool

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            user_id=user.id.to_raw(),
            username=user.username.to_raw(),
            created_at=user.created_at,
            is_deleted=user.deleted_at.is_deleted(),
        )
