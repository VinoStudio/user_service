from infrastructure.base.repository.base import SQLAlchemyRepository
from infrastructure.base.repository import BaseUserWriter
import domain.user.entities as entity
from typing import Iterable
from dataclasses import dataclass

from infrastructure.exceptions.repository import (
    UserDoesNotExistException,
    UserWithUsernameDoesNotExistException,
)
from infrastructure.repositories.pagination import Pagination
import infrastructure.repositories.converters as c
from sqlalchemy import text


@dataclass
class UserWriter(SQLAlchemyRepository, BaseUserWriter):
    async def create_user(self, user: entity.User) -> None:
        db_user = c.convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        await self._session.flush()

    async def update_user(self, user: entity.User) -> None:
        await self._session.execute(
            text(
                """
                UPDATE "user"
                SET username = :username, 
                first_name = :first_name, 
                last_name = :last_name, 
                middle_name = :middle_name, 
                deleted_at = :deleted_at, 
                version = :version
                WHERE id = :id
                """
            ),
            c.convert_user_entity_to_db_dict(user),
        )

    async def delete_user(self, user: entity.User) -> None:
        await self.update_user(user)

    async def restore_user(self, user: entity.User) -> None:
        await self.update_user(user)

    async def get_user_by_id(self, user_id: str) -> entity.User:
        user: entity.User | None = await self._session.get(entity.User, user_id)

        if user is None:
            raise UserDoesNotExistException(user_id)

        return c.convert_db_model_to_user_entity(user)

    async def check_if_username_exists(self, username: str) -> bool:
        result = await self._session.execute(
            text(
                """
                    SELECT EXISTS (
                        SELECT 1
                        FROM "user"
                        WHERE username = :username
                    )
                """
            ),
            dict(username=username),
        )
        # Extract the actual boolean value from the result
        return result.scalar()
