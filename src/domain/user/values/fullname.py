from dataclasses import dataclass
from domain.base.values.base import BaseValueObject
from domain.user.exceptions.fullname import (
    NameIsTooLongException,
    NameIsTooShortException,
    WrongNameFormatException,
)
import re

NAME_PATTERN_REGEX = re.compile(r"[A-Za-zа-яА-Я]+")
RU_PATTERN_REGEX = re.compile(r"[а-яА-Я]+")


@dataclass(frozen=True)
class FullName(BaseValueObject):
    first_name: str
    last_name: str
    middle_name: str | None = None

    def _validate(self) -> None:
        if len(self.first_name) > 24:
            raise NameIsTooLongException(self.first_name)
        if len(self.first_name) == 0:
            raise NameIsTooShortException(self.first_name)
        if not NAME_PATTERN_REGEX.match(self.first_name):
            raise WrongNameFormatException(self.first_name)

        if len(self.last_name) > 24:
            raise NameIsTooLongException(self.last_name)
        if len(self.last_name) == 0:
            raise NameIsTooShortException(self.last_name)
        if not NAME_PATTERN_REGEX.match(self.last_name):
            raise WrongNameFormatException(self.last_name)

        if self.middle_name:
            if len(self.middle_name) > 24:
                raise NameIsTooLongException(self.middle_name)
            if len(self.middle_name) == 0:
                raise NameIsTooShortException(self.middle_name)
            if not NAME_PATTERN_REGEX.match(self.middle_name):
                raise WrongNameFormatException(self.middle_name)

    def __str__(self):
        if self.middle_name is None:
            return f"{self.first_name} {self.last_name}"
        if RU_PATTERN_REGEX.match(self.middle_name):
            return f"{self.first_name} {self.last_name} {self.middle_name}"
        return f"{self.first_name} {self.middle_name} {self.last_name}"
