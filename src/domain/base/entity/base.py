from dataclasses import dataclass, field
from typing import Generic, TypeVar, Any
from abc import ABC
from datetime import datetime, UTC
from copy import copy
from domain.base.events.base import BaseEvent

from uuid6 import uuid7


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid7()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )
