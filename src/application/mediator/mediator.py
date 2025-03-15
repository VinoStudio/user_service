from dataclasses import dataclass, field
from typing import Iterable

from black.trans import defaultdict

from application.base.commands import CommandHandler, CT, CR, BaseCommand
from application.base.mediator.command import CommandMediator
from application.base.mediator.query import QueryMediator
from application.base.queries import BaseQueryHandler, QT, QR, BaseQuery

from application.exceptions.mediator import CommandIsNotRegisteredException


@dataclass(eq=False)
class Mediator(CommandMediator, QueryMediator):
    command_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    query_map: dict[QT, BaseQueryHandler] = field(default_factory=dict, kw_only=True)

    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]
    ) -> None:
        self.command_map[command].extend(command_handlers)

    def register_query(
        self, query: QT, query_handler: BaseQueryHandler[QT, QR]
    ) -> None:
        self.query_map[query] = query_handler

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type: type(BaseCommand) = command.__class__

        command_handlers: Iterable[CommandHandler] = self.command_map.get(command_type)

        if not command_handlers:
            raise CommandIsNotRegisteredException(command_type)

        return [await c.handle(command) for c in command_handlers]

    async def handle_query(self, query: QT) -> QR:
        return await self.query_map[query.__class__].handle(query)
