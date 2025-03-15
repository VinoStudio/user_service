from dataclasses import dataclass
from domain.base.values.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value:
            raise ValueError
