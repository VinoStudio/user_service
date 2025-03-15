from dishka import Scope, provide, Provider, decorate

from application.base.event_publisher.event_publisher import EventPublisher
from application.event_bus.event_bus import EventBus
from application.mediator.mediator import Mediator
from application.user.commands import CreateUserCommandHandler, CreateUserCommand
from application.user.events import (
    UserCreatedEventHandler,
    UserRestoredEventHandler,
    UserDeletedEventHandler,
)
from domain.user.events import (
    UsernameUpdated,
    FullnameUpdated,
    UserDeleted,
    UserRestored,
    UserCreated,
)


from application.user.queries import (
    GetUserByIdHandler,
    GetUserById,
    GetUserByUsernameHandler,
    GetUserByUsername,
)

from infrastructure.base.message_broker.producer import AsyncMessageProducer


class MediatorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_mediator(self) -> Mediator:
        return Mediator()

    @provide(scope=Scope.APP)
    async def get_event_bus(
        self, message_broker: AsyncMessageProducer
    ) -> EventPublisher:
        return EventBus(_message_broker=message_broker)


class MediatorConfigProvider(Provider):
    @decorate
    async def register_commands(
        self,
        mediator: Mediator,
        create_user: CreateUserCommandHandler,
    ) -> Mediator:

        mediator.register_command(CreateUserCommand, [create_user])

        return mediator

    @decorate
    async def register_query(
        self,
        mediator: Mediator,
        get_user_by_id: GetUserByIdHandler,
        get_user_by_username: GetUserByUsernameHandler,
    ) -> Mediator:

        mediator.register_query(GetUserById, get_user_by_id)
        mediator.register_query(GetUserByUsername, get_user_by_username)

        return mediator

    @decorate
    async def register_events(
        self,
        event_bus: EventPublisher,
        user_created: UserCreatedEventHandler,
        user_restored: UserRestoredEventHandler,
        user_deleted: UserDeletedEventHandler,
    ) -> EventPublisher:

        event_bus.register_event(UserCreated, [user_created])
        event_bus.register_event(UserRestored, [user_restored])
        event_bus.register_event(UserDeleted, [user_deleted])

        return event_bus
