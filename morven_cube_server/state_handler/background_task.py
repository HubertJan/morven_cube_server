import asyncio
from typing import AsyncIterator, Awaitable, Callable, Coroutine, Optional
from aiohttp import web


def add_background_task(
    app: web.Application,
    task_func: Callable[[], Coroutine[None, None, None]],
    on_stop: Optional[Callable[[asyncio.Task[None]],
                               Awaitable[None]]] = None
) -> None:
    async def run_background(app: web.Application) -> AsyncIterator[None]:
        task = asyncio.create_task(task_func())
        yield
        if on_stop is None:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            finally:
                return
        await on_stop(task)
    app.cleanup_ctx.append(run_background)
