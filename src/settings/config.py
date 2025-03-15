from pydantic_settings import BaseSettings
from dataclasses import dataclass
from pydantic import Field
from dishka import provide, Scope, Provider


class PostgresDB(BaseSettings):
    db_name: str = Field(default="postgres", alias="POSTGRES_DB")
    db_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    db_port: str = Field(default="5432", alias="POSTGRES_PORT")
    db_user: str = Field(default="postgres", alias="POSTGRES_USER")
    db_password: str = Field(default="postgres", alias="POSTGRES_PASSWORD")

    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class TestPostgresDB(BaseSettings):
    db_name: str = Field(default="postgres_test", alias="POSTGRES_TEST_DB")
    db_host: str = Field(default="localhost", alias="POSTGRES_TEST_HOST")
    db_port: str = Field(default="5433", alias="POSTGRES_TEST_PORT")
    db_user: str = Field(default="postgres_test", alias="POSTGRES_TEST_USER")
    db_password: str = Field(default="postgres_test", alias="POSTGRES_PASSWORD")

    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class KafkaConfig(BaseSettings):
    kafka_url: str = Field(default="kafka:29092", alias="KAFKA_URL")
    user_service_topic: str = Field(default="user_service_topic")

    class Config:
        env_prefix = "KAFKA_"
        case_sensitive = False


@dataclass(frozen=True)
class Config:
    postgres = PostgresDB()
    test_db = TestPostgresDB()
    kafka = KafkaConfig()


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        return Config()
