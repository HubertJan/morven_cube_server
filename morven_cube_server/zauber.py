from xmlrpc.client import Server
from aiohttp import web
from morven_cube_server.models.server_state import ServerState
from morven_cube_server.state_handler.background_task import start_background_task
from morven_cube_server.state_handler.provider import provide

from morven_cube_server.services.arduino_connection import connect_to_arduino
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.secondary_arduino_connection import SecondaryArduinoService

def run_server():
    app = web.Application()
    secondaryService = SecondaryArduinoService()
    provide(app=app, value=PrimaryArduinoService(), valueType=PrimaryArduinoService)
    provide(app=app, value=secondaryService, 
    valueType=SecondaryArduinoService)
    provide(app=app, value=ServerState(), valueType=ServerState)

    start_background_task(app=app, task_func=connect_to_arduino)
    web.run_app(app, host='localhost', port=9000)