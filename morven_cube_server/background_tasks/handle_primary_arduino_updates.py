import asyncio
from typing import Awaitable, Callable
from aiohttp import web
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.state_handler.refresh_on_update import refresh_on_update
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState
from morven_cube_server.models.running_program_report import RunningProgramReport
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.state_handler.notifier import Notifier

from morven_cube_server.state_handler.provider import consume

async def handle_primary_arduino_updates(app: web.Application):
    service = consume(app, valueType=PrimaryArduinoService)
    arduino_state = consume(app, valueType=PrimaryArduinoState)
    
    async def create_task():
        async for update in service.handle_received_updates():
            if update is EndOfProgramReport:
                arduino_state.current_program = None
                arduino_state.status = PrimaryArduinoStatus.IDLE
            elif update is RunningProgramReport:
                arduino_state.last_instruction_id = update.latest_finished_instruction_id
                arduino_state.runtime = update.run_time
    await refresh_on_update(
        notifier=service, 
        task_func= create_task
    )