from dataclasses import dataclass
from domain.base.exceptions.domain import DomainException, ValidationException


@dataclass(frozen=True)
class NameIsTooLongException(ValidationException):
    name: str

    @property
    def message(self) -> str:
        return f"Name {self.name} is too long"


@dataclass(frozen=True)
class NameIsTooShortException(ValidationException):
    name: str

    @property
    def message(self) -> str:
        return f"Name {self.name} is too short"


@dataclass(frozen=True)
class WrongNameFormatException(ValidationException):
    name: str

    @property
    def message(self) -> str:
        return f"Name {self.name} has wrong format"
