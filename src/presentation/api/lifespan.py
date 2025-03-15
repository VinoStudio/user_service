from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from application.dependency_injector.di import get_container
from fastapi import FastAPI
from infrastructure.db.models.base import BaseModel


async def create_tables():
    container = get_container()
    engine = await container.get(AsyncEngine)
    async with engine.begin() as e:
        await e.run_sync(BaseModel.metadata.create_all)


async def dispose_engine():
    container = get_container()
    engine = await container.get(AsyncEngine)
    async with engine.begin() as e:
        await e.run_sync(BaseModel.metadata.drop_all)
    await engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    # container: Container = init_container()
    # scheduler: Scheduler = container.resolve(Scheduler)
    # job = await scheduler.spawn(consume_in_background())

    yield
    # await job.close()
    await dispose_engine()
