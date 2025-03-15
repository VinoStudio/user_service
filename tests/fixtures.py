from dishka import AsyncContainer, make_async_container

from application.di_setup import MediatorProvider, MediatorConfigProvider
from application.user.di_setup import (
    CommandRegisterProvider,
    EventRegisterProvider,
    QueryRegisterProvider,
)
from infrastructure.db.di_setup import TestDatabaseProvider, SessionProvider
from infrastructure.message_broker.di_setup import MessageBrokerProvider
from infrastructure.repositories.di_setup import RepositoryProvider, UnitOfWorkProvider
from settings.config import ConfigProvider
from application.dependency_injector.di import get_container


def init_test_di_container() -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        TestDatabaseProvider(),
        SessionProvider(),
        RepositoryProvider(),
        UnitOfWorkProvider(),
        MessageBrokerProvider(),
        MediatorProvider(),
        CommandRegisterProvider(),
        EventRegisterProvider(),
        QueryRegisterProvider(),
        MediatorConfigProvider(),
    )


#
# def init_test_di_container() -> AsyncContainer:
#     return get_container()
