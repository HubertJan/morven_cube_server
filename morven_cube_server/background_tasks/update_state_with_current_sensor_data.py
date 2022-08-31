import imp
from typing import Protocol
from aiohttp import web

from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.state_handler.notifier import SupportsAddListener
from morven_cube_server.state_handler.refresh_on_update import refresh_on_update
from morven_cube_server.states.server_state import SensorData, ServerState
from morven_cube_server.state_handler.provider import consume

from morven_cube_server.services.secondary_service import SecondaryService


async def update_state_with_current_sensor_data(app: web.Application) -> None:
    service = consume(app, valueType=SecondaryService)
    state = consume(app, valueType=ServerState)
    await refresh_on_update(
        notifier=service,
        create_coroutine=lambda: state.update_sensor_data_by_receiving_data(
            service.handle_received_sensor_data()
        )
    )
