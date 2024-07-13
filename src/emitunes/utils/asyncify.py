import asyncio
from collections.abc import AsyncIterable, Iterable
from typing import TypeVar

T = TypeVar("T")


async def iterable(it: Iterable[T]) -> AsyncIterable[T]:
    """Convert an iterable to an async iterable."""

    iterator = await asyncio.to_thread(iter, it)
    sentinel = object()

    while True:
        item = await asyncio.to_thread(next, iterator, sentinel)

        if item is sentinel:
            break

        yield item
