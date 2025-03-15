from dishka import provide, Provider, Scope

from infrastructure.base.message_broker.producer import AsyncMessageProducer
from infrastructure.base.message_broker.consumer import AsyncMessageConsumer
from settings.config import Config
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from infrastructure.message_broker.kafka_producer import AsyncKafkaProducer
from infrastructure.message_broker.kafka_consumer import AsyncKafkaConsumer


class MessageBrokerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_message_producer(self, config: Config) -> AsyncMessageProducer:
        return AsyncKafkaProducer(
            producer=AIOKafkaProducer(
                bootstrap_servers=config.kafka.kafka_url,
            ),
        )

    @provide(scope=Scope.APP)
    async def get_message_consumer(self, config: Config) -> AsyncMessageConsumer:
        return AsyncKafkaConsumer(
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka.kafka_url,
                group_id="user-service-group",
                metadata_max_age_ms=40000,
            )
        )
