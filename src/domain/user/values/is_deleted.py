from dataclasses import dataclass
from domain.base.values.base import ValueObject
from datetime import datetime, UTC
from typing import Self


@dataclass(frozen=True)
class DeletedAt(ValueObject[datetime | None]):
    value: datetime | None

    def _validate(self) -> None: ...

    @classmethod
    def deleted_at(cls) -> Self:
        return cls(datetime.now(UTC))

    @classmethod
    def not_deleted(cls) -> Self:
        return cls(None)

    def is_deleted(self) -> bool:
        return self.value is not None
