import asyncio
from collections.abc import AsyncIterable, Iterable
from threading import Thread
from typing import TypeVar

T = TypeVar("T")


class LoopThread(Thread):
    """Thread with an event loop."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:

        def _run(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        super().__init__(target=_run, args=(loop,))


class LoopContext:
    """Context manager for an event loop."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def __enter__(self) -> None:
        return None

    def __exit__(self, *args, **kwargs) -> None:
        self._loop.call_soon_threadsafe(self._loop.stop)


class ThreadContext:
    """Context manager for a thread."""

    def __init__(self, thread: Thread) -> None:
        self._thread = thread

    def __enter__(self) -> None:
        self._thread.start()

    def __exit__(self, *args, **kwargs) -> None:
        self._thread.join()


class LoopThreadContext:
    """Context manager for an event loop running in a thread."""

    def __init__(self) -> None:
        self._loop_context = None
        self._thread_context = None

    def __enter__(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.new_event_loop()
        thread = LoopThread(loop)

        self._thread_context = ThreadContext(thread)
        self._loop_context = LoopContext(loop)

        self._thread_context.__enter__()
        self._loop_context.__enter__()

        return loop

    def __exit__(self, *args, **kwargs) -> None:
        self._loop_context.__exit__()
        self._thread_context.__exit__()


def iterable(it: AsyncIterable[T]) -> Iterable[T]:
    """Convert an async iterable to an iterable."""

    iterator = aiter(it)
    sentinel = object()

    with LoopThreadContext() as loop:
        while True:
            coroutine = anext(iterator, sentinel)
            future = asyncio.run_coroutine_threadsafe(coroutine, loop)
            item = future.result()

            if item is sentinel:
                break

            yield item
