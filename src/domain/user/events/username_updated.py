from dataclasses import dataclass, field
from domain.base.events.base import BaseEvent


@dataclass(frozen=True)
class UsernameUpdated(BaseEvent):
    user_id: str
    username: str
