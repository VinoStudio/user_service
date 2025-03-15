from dishka import provide, Scope, Provider, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.base.repository.base import SQLAlchemyRepository
from infrastructure.base.repository.user_reader import BaseUserReader
from infrastructure.base.repository.user_writer import BaseUserWriter
from infrastructure.db.uow import SQLAlchemyUoW
from infrastructure.repositories.user.user_reader import UserReader
from infrastructure.repositories.user.user_writer import UserWriter


class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_sqlalchemy_provider(
        self, session: AsyncSession
    ) -> SQLAlchemyRepository:
        return SQLAlchemyRepository(_session=session)

    user_reader = provide(UserReader, scope=Scope.REQUEST, provides=BaseUserReader)

    user_writer = provide(UserWriter, scope=Scope.REQUEST, provides=BaseUserWriter)


class UnitOfWorkProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_sqlalchemy_uow_provider(self, session: AsyncSession) -> SQLAlchemyUoW:
        return SQLAlchemyUoW(_session=session)
