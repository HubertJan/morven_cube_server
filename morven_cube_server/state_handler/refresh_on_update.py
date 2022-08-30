import asyncio
from morven_cube_server.state_handler.notifier import Notifier

async def refresh_on_update(notifier: Notifier, task_func):
    task = asyncio.create_task(task_func())
    notifier.add_listener(lambda: task.cancel())
    while True:
        try:
            await task
        except asyncio.CancelledError:
            task = asyncio.create_task(task_func)