from dataclasses import dataclass, field
from typing import Iterable, Any

from black.trans import defaultdict

from application.base.event_publisher.event_publisher import EventPublisher
from application.base.events.event_handler import EventHandler, ET, ER
from domain.base.events.base import BaseEvent


@dataclass(eq=False)
class EventBus(EventPublisher):
    event_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    def register_event(
        self, event: BaseEvent, event_handlers: Iterable[EventHandler[BaseEvent, Any]]
    ) -> None:
        self.event_map[event].extend(event_handlers)

    async def handle_event(self, events: Iterable[BaseEvent]) -> None:
        for event in events:
            event_handlers: Iterable[EventHandler] = self.event_map.get(event.__class__)
            for handler in event_handlers:
                message = await handler.handle(event)
                await self._message_broker.publish(**message)
