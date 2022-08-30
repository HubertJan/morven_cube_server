import asyncio
from typing import Awaitable, Callable, Coroutine
from morven_cube_server.state_handler.notifier import Notifier


async def refresh_on_update(
    notifier: Notifier,
    create_coroutine: Callable[[], Coroutine[None, None, None]]
) -> None:
    task = asyncio.create_task(create_coroutine())
    notifier.add_listener(lambda: task.cancel())
    while True:
        try:
            await task
        except asyncio.CancelledError:
            task = asyncio.create_task(create_coroutine())
