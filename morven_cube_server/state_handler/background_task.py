import asyncio
from typing import AsyncIterator, Awaitable, Callable, Coroutine, Optional
from aiohttp import web


def add_background_task(
    app: web.Application,
    task_func: Callable[[web.Application], Coroutine[None, None, None]],
    on_stop: Optional[Callable[[asyncio.Task[None]],
                               Awaitable[None]]] = None
) -> None:
    async def run_background(app: web.Application) -> None:
        app[f'task-{task_func.__name__}'] = asyncio.create_task(task_func(app))

    async def stop_and_cleanup_background(app: web.Application) -> None:
        task: asyncio.Task[None] = app[f'task-{task_func.__name__}']
        if on_stop is None:
            task.cancel()
            return
        await on_stop(task)
    app.on_startup.append(run_background)
    app.on_cleanup.append(stop_and_cleanup_background)
