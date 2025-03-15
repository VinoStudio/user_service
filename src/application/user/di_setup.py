from dishka import Scope, provide, Provider
from application.user.commands import CreateUserCommand, CreateUserCommandHandler

from application.user.events import (
    UserCreatedEventHandler,
    UserRestoredEventHandler,
    UserDeletedEventHandler,
)

from application.user.queries import GetUserByIdHandler, GetUserByUsernameHandler

from settings.config import Config


class CommandRegisterProvider(Provider):
    # Command handlers
    create_user = provide(CreateUserCommandHandler, scope=Scope.REQUEST)


class EventRegisterProvider(Provider):
    # Event handlers
    @provide(scope=Scope.APP)
    async def user_created(self, config: Config) -> UserCreatedEventHandler:
        return UserCreatedEventHandler(broker_topic=config.kafka.user_service_topic)

    @provide(scope=Scope.APP)
    async def user_restored(self, config: Config) -> UserRestoredEventHandler:
        return UserRestoredEventHandler(broker_topic=config.kafka.user_service_topic)

    @provide(scope=Scope.APP)
    async def user_deleted(self, config: Config) -> UserDeletedEventHandler:
        return UserDeletedEventHandler(broker_topic=config.kafka.user_service_topic)


class QueryRegisterProvider(Provider):
    # Query handlers
    get_user_by_id = provide(GetUserByIdHandler, scope=Scope.REQUEST)
    get_user_by_username = provide(GetUserByUsernameHandler, scope=Scope.REQUEST)
