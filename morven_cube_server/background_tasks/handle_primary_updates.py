from datetime import datetime
from re import I
from xmlrpc.client import Server
from aiohttp import web
from morven_cube_server.models.cube_pattern import CubePattern

from morven_cube_server.state_handler.provider import consume
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.state_handler.refresh_on_update import refresh_on_update
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState:
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.services.rubiks_database_service import RubiksDatabaseService


async def _handle_updates(state: ServerState,
                          service: PrimaryService,
                          arduino_state: PrimaryServiceState:,
                          database: RubiksDatabaseService,
                          ) -> None:
    async for report in service.handle_received_updates():
        state.cube_pattern = CubePattern(report.program.end_pattern)
        now = datetime.now()
        now_string = now.strftime("%d/%m/%Y %H:%M:%S")
        database.add_finished_runthrough(
            date=now_string,
            report=report,
        )
        arduino_state.current_program = None
        arduino_state.status = PrimaryArduinoStatus.IDLING


async def handle_primary_updates(app: web.Application) -> None:
    service = consume(app, valueType=PrimaryService)
    state = consume(app, valueType=ServerState)
    arduino_state = consume(app, valueType=PrimaryServiceState:)
    database = consume(app, valueType=RubiksDatabaseService)
    await refresh_on_update(
        notifier=service,
        create_coroutine=lambda: _handle_updates(
            state=state, service=service,
            arduino_state=arduino_state,
            database=database)
    )
