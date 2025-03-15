from dataclasses import dataclass
from domain.user.entities.user import User
from abc import ABC, abstractmethod
from typing import Iterable


class BaseUserReader(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(self) -> Iterable[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_usernames(self) -> Iterable[str]:
        raise NotImplementedError
