from aiohttp import web
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus

from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState


async def connect_to_arduinos(app: web.Application) -> None:
    service1 = consume(app, valueType=PrimaryService)
    service2 = consume(app, valueType=SecondaryService)
    state1 = consume(app, valueType=PrimaryArduinoState)
    await service1.connect(baudrate=5000, port=5)
    await service2.connect(baudrate=5000, port=5)
    state1.status = PrimaryArduinoStatus.IDLING
