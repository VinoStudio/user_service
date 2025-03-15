from dataclasses import dataclass
from typing import Any

from domain.user.events.user_restored import UserRestored
from domain.user.events.user_created import UserCreated
from domain.user.events.user_deleted import UserDeleted
from domain.user.events.fullname_updated import FullnameUpdated
from domain.user.events.username_updated import UsernameUpdated
from domain.base.events.base import BaseEvent

from application.base.events.event_handler import EventHandler
from infrastructure.message_broker.converters import convert_event_to_broker_message


@dataclass
class UserCreatedEventHandler(EventHandler[UserCreated, Any]):
    async def handle(self, event: UserCreated) -> dict:
        return dict(
            key=str(event.id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event),
        )


@dataclass
class UserRestoredEventHandler(EventHandler[UserRestored, Any]):
    async def handle(self, event: UserRestored):
        return dict(
            key=str(event.id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event),
        )


@dataclass
class UserDeletedEventHandler(EventHandler[UserDeleted, Any]):
    async def handle(self, event: UserDeleted):
        return dict(
            key=str(event.id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event),
        )
