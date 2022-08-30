import asyncio
from typing import AsyncGenerator
from xmlrpc.client import Server
from aiohttp import web
from morven_cube_server.models.server_state import SensorData, ServerState

from morven_cube_server.state_handler.provider import consume
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.secondary_arduino_connection import SecondaryArduinoService

async def connect_to_arduinos(app: web.Application):
    service = consume(app, valueType=SecondaryArduinoService)
    await service.connect(baudrate=5,port=5)

async def update_state_with_current_sensor_data(app: web.Application):
    service = consume(app, valueType=SecondaryArduinoService)
    state = consume(app, valueType=ServerState)
    updating_state = asyncio.create_task(state.update_sensor_data_by_receiving_data(service.handle_received_sensor_data))
    service.add_listener(lambda: updating_state.cancel())
    while True:
        try:
            await updating_state
        except asyncio.CancelledError:
            receiving_data = service.handle_received_sensor_data()
            updating_state = asyncio.create_task(
                state.update_sensor_data_by_receiving_data(receiving_data)
                )