from dataclasses import dataclass
from domain.base.events.base import BaseEvent


@dataclass(frozen=True)
class FullnameUpdated(BaseEvent):
    user_id: str
    first_name: str
    last_name: str
    middle_name: str | None
