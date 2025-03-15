from dataclasses import dataclass
from domain.base.events.base import BaseEvent


@dataclass(frozen=True)
class UserDeleted(BaseEvent):
    user_id: str
