import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import TypeVar

T = TypeVar("T")


async def iterator(it: Iterator[T]) -> AsyncIterator[T]:
    """Convert an iterator to an async iterator."""

    sentinel = object()

    while True:
        item = await asyncio.to_thread(next, it, sentinel)

        if item is sentinel:
            break

        yield item
