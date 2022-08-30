from aiohttp import web

from morven_cube_server.services.secondary_arduino_connection import SecondaryArduinoService
from morven_cube_server.state_handler.provider import consume

async def connect_to_arduinos(app: web.Application):
    service = consume(app, valueType=SecondaryArduinoService)
    await service.connect(baudrate=5,port=5)