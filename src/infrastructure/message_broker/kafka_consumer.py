from typing import Any, Dict, Optional, List, AsyncGenerator

import orjson

from infrastructure.base.message_broker.consumer import AsyncMessageConsumer
from dataclasses import dataclass
from aiokafka import AIOKafkaConsumer


@dataclass
class AsyncKafkaConsumer(AsyncMessageConsumer):

    async def start(self) -> None:
        """Start the consumer."""
        await self.consumer.start()

    async def close(self) -> None:
        """Close the consumer."""
        await self.consumer.stop()

    async def subscribe(self, topics: List[str]) -> None:
        """Subscribe to one or more topics."""
        self.consumer.subscribe(topics=topics)

    async def start_consuming(self) -> AsyncGenerator[Any, None]:
        """Start consuming messages."""
        async for msg in self.consumer:
            yield orjson.loads(msg.value).decode("utf-8")

    async def stop_consuming(self) -> None:
        """Stop consuming messages."""
        self.consumer.unsubscribe()

    @property
    async def is_connected(self) -> bool:
        if not self.consumer:
            return False

        if getattr(self.consumer, "_closed", True):
            return False

        return True
