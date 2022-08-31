import asyncio
from typing import Any, Awaitable, Callable, Coroutine
from morven_cube_server.state_handler.notifier import SupportsAddListener, do


async def refresh_on_update(
    notifier: SupportsAddListener,
    create_coroutine: Callable[[], Coroutine[None, None, Any]]
) -> None:
    task = asyncio.create_task(create_coroutine())
    notifier.add_listener(lambda: do(task.cancel()))
    while True:
        try:
            await task
        except asyncio.CancelledError:
            task = asyncio.create_task(create_coroutine())
