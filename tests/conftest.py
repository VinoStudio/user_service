import pytest
import pytest_asyncio
import asyncio

from domain.user.entities.user import User
from domain.user.values.fullname import FullName
from domain.user.values.user_id import UserId
from domain.user.values.username import Username
from infrastructure.base.repository.user_writer import BaseUserWriter
from infrastructure.db.uow import SQLAlchemyUoW
from tests.fixtures import init_test_di_container
from infrastructure.db.models import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine


@pytest.fixture(scope="session")
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    container = init_test_di_container()

    engine = await container.get(AsyncEngine)

    # Create tables inside this context
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    # Drop tables inside this context
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="session")
async def create_test_user():
    container = init_test_di_container()

    async with container() as c:
        user_writer = await c.get(BaseUserWriter)
        uow = await c.get(SQLAlchemyUoW)

        await user_writer.create_user(
            User.create(
                UserId("user_id"),
                Username("username"),
                FullName("first_name", "last_name", "middle_name"),
            )
        )
        await uow.commit()


@pytest.fixture(scope="session")
async def di_container():
    return init_test_di_container()
