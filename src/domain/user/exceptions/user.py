from dataclasses import dataclass
from domain.base.exceptions.domain import DomainException


@dataclass(frozen=True)
class UserIsDeletedException(DomainException):
    user_id: str

    @property
    def message(self):
        return (
            f"User with id {self.user_id} is deleted. You can reactivate your account."
        )


@dataclass(frozen=True)
class UsernameAlreadyExistsException(DomainException):
    username: str

    @property
    def message(self):
        return f"Username {self.username} already exists"
