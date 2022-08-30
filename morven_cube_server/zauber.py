from aiohttp import web
from morven_cube_server.background_tasks.update_state_with_current_sensor_data import update_state_with_current_sensor_data
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.state_handler.background_task import add_background_task
from morven_cube_server.state_handler.provider import provide

from morven_cube_server.services.arduino_connection import connect_to_arduino
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService

def run_server():
    app = web.Application()
    provide(app=app, value=PrimaryArduinoService(), valueType=PrimaryArduinoService)
    provide(app=app, value=SecondaryArduinoService(), 
    valueType=SecondaryArduinoService)
    provide(app=app, value=ServerState(), valueType=ServerState)
    provide(app=app, value=PrimaryArduinoState(), valueType=PrimaryArduinoState)

    add_background_task(
        app=app, 
        task_func=connect_to_arduino
    )
    add_background_task(
        app=app, 
        task_func=update_state_with_current_sensor_data,
    )
    web.run_app(app, host='localhost', port=9000)