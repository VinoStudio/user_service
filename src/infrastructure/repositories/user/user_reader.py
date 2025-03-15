from infrastructure.base.repository.base import SQLAlchemyRepository
from infrastructure.base.repository import BaseUserReader
import infrastructure.db.models as models
import domain.user.entities as entity
from typing import Iterable

from infrastructure.exceptions.repository import (
    UserDoesNotExistException,
    UserWithUsernameDoesNotExistException,
)
from infrastructure.repositories.pagination import Pagination
import infrastructure.repositories.converters as c
from sqlalchemy import text


class UserReader(SQLAlchemyRepository, BaseUserReader):
    async def get_user_by_id(self, user_id: str) -> entity.User:
        result = await self._session.execute(
            text(
                """
                SELECT u.*
                FROM "user" as u
                WHERE id = :id
                """
            ),
            dict(id=user_id),
        )

        user: entity.User | None = result.fetchone()

        if user is None:
            raise UserDoesNotExistException(user_id)

        return c.convert_db_model_to_user_entity(user)

    async def get_user_by_username(self, username: str) -> entity.User:
        result = await self._session.execute(
            text(
                """
                SELECT u.*
                FROM "user" as u
                WHERE username = :username
                """
            ),
            dict(username=username),
        )
        user: entity.User | None = result.fetchone()

        if user is None:
            raise UserWithUsernameDoesNotExistException(username)

        return c.convert_db_model_to_active_user_entity(user)

    async def get_all_users(self, pagination: Pagination) -> Iterable[entity.User]:
        result = await self._session.execute(
            text(
                """
            SELECT u.*
            FROM "user" as u
            ORDER BY id
            OFFSET :offset
            LIMIT :limit
            """
            ),
            dict(offset=pagination.offset, limit=pagination.limit),
        )

        return [c.convert_db_model_to_user_entity(user) for user in result.fetchall()]

    async def get_all_usernames(self) -> Iterable[str]: ...
