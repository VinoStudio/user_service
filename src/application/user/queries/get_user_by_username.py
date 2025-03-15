from dataclasses import dataclass
from typing import Any

from application.base.queries import BaseQuery, BaseQueryHandler
from domain.user.entities.user import User
from infrastructure.base.repository.user_reader import BaseUserReader


@dataclass(frozen=True)
class GetUserByUsername(BaseQuery):
    username: str


@dataclass(frozen=True)
class GetUserByUsernameHandler(BaseQueryHandler[GetUserByUsername, Any]):
    user_reader: BaseUserReader

    async def handle(self, query: GetUserByUsername) -> User:
        return await self.user_reader.get_user_by_username(query.username)
