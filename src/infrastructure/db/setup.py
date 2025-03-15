from typing import AsyncGenerator
from dishka import provide, Scope, Provider

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from settings.config import Config


async def build_engine(config: Config) -> AsyncEngine:
    # don't forget to dispose connection pools at app shutdown
    return create_async_engine(
        config.postgres.db_url,
        echo=True,
        pool_size=50,
    )


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
