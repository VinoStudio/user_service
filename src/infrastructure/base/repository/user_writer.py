from dataclasses import dataclass
from typing import Protocol
from domain.user.entities.user import User
from abc import abstractmethod, ABC


@dataclass
class BaseUserWriter(ABC):
    # get methods implemented too because we need to get user to deal with
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def restore_user(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_if_username_exists(self, username: str) -> bool:
        raise NotImplementedError
