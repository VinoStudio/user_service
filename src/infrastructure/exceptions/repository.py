from infrastructure.base.exception import InfrastructureException
from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryException(InfrastructureException):
    pass


@dataclass(frozen=True)
class UserIdAlreadyExistsErrorException(RepositoryException):
    value: str

    @property
    def message(self) -> str:
        return f'A user with the "{self.value}" user_id already exists'


@dataclass(frozen=True)
class UserDoesNotExistException(RepositoryException):
    value: str

    @property
    def message(self) -> str:
        return f'A user with "{self.value}" user_id does not exist'


@dataclass(frozen=True)
class UserWithUsernameDoesNotExistException(RepositoryException):
    value: str

    @property
    def message(self) -> str:
        return f'A user with "{self.value}" username does not exist'


@dataclass(frozen=True)
class UserIsDeletedException(RepositoryException):
    value: str

    @property
    def message(self) -> str:
        return f'A user with "{self.value}" user_id is deleted'
