from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    offset: int = 0
    limit: int = 10
    order: str = "asc"
