import asyncio
from typing import Awaitable, Callable, Coroutine, Optional
from aiohttp import web


def start_background_task(app: web.Application, task_func: Callable[[], Coroutine], on_stop: Optional[Callable[[asyncio.Task], Awaitable[None]]]):
    async def run_background(app: web.Application):
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