from application.base.event_publisher.event_publisher import EventPublisher
from application.exceptions.user import UsernameAlreadyExistsException
from domain.user.entities.user import User
from domain.user.values.user_id import UserId
from domain.user.values.username import Username
from domain.user.values.fullname import FullName

from infrastructure.base.repository.base import SQLAlchemyRepository
from infrastructure.base.repository.user_writer import BaseUserWriter
from infrastructure.db.uow import SQLAlchemyUoW

from application.base.commands.command_handler import CommandHandler
from application.base.commands.base import BaseCommand

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    user_id: str
    username: str
    first_name: str | None
    last_name: str | None
    middle_name: str | None


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    _event_handler: EventPublisher
    _user_writer: BaseUserWriter
    _uow: SQLAlchemyUoW

    async def handle(self, command: CreateUserCommand) -> User:

        if await self._user_writer.check_if_username_exists(command.username):
            raise UsernameAlreadyExistsException(command.username)

        user_id = UserId(command.user_id)
        username = Username(command.username)
        full_name = FullName(
            first_name=command.first_name,
            last_name=command.last_name,
            middle_name=command.middle_name,
        )

        user = User.create(user_id, username, full_name)

        await self._user_writer.create_user(user)
        # await self._event_handler.handle_event(user.pull_events())
        await self._uow.commit()

        return user
