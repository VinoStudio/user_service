from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar


@dataclass(eq=False, frozen=True)
class AppException(ABC, Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Application Error"
