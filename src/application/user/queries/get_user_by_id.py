from dataclasses import dataclass
from typing import Any

from application.base.queries import BaseQuery, BaseQueryHandler
from domain.user.entities.user import User
from infrastructure.base.repository.user_reader import BaseUserReader


@dataclass(frozen=True)
class GetUserById(BaseQuery):
    user_id: str


@dataclass(frozen=True)
class GetUserByIdHandler(BaseQueryHandler[GetUserById, Any]):
    user_reader: BaseUserReader

    async def handle(self, query: GetUserById) -> User:
        return await self.user_reader.get_user_by_id(user_id=query.user_id)
