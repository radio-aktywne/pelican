import asyncio
from collections.abc import AsyncIterator, Generator, Iterator
from typing import TypeVar

T = TypeVar("T")


def iterator(
    it: AsyncIterator[T], loop: asyncio.AbstractEventLoop | None = None
) -> Iterator[T]:
    """Convert an async iterator to an iterator."""

    def _iterate(
        it: AsyncIterator[T], loop: asyncio.AbstractEventLoop
    ) -> Generator[T, None, None]:
        sentinel = object()

        while True:
            coroutine = anext(it, sentinel)
            future = asyncio.run_coroutine_threadsafe(coroutine, loop)
            item = future.result()

            if item is sentinel:
                break

            yield item

    loop = loop if loop is not None else asyncio.get_running_loop()
    return _iterate(it, loop)
