from dataclasses import dataclass
from domain.base.events.base import BaseEvent


@dataclass(frozen=True)
class UserRestored(BaseEvent):
    user_id: str
