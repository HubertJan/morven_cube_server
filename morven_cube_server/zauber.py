from aiohttp import web
from morven_cube_server.all_routes import routes
from morven_cube_server.background_tasks.update_state_with_current_sensor_data import update_state_with_current_sensor_data
from morven_cube_server.background_tasks.connect_to_arduinos import connect_to_arduinos
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.state_handler.background_task import add_background_task
from morven_cube_server.state_handler.provider import provide
from morven_cube_server.background_tasks.handle_primary_updates import handle_primary_updates

from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.rubiks_database_service import RubiksDatabaseService

from morven_cube_server.routes import *

from morven_cube_server.dummies.dummy_primary_arduino_service import DummyPrimaryArduinoService
from morven_cube_server.dummies.dummy_secondary_arduino_service import DummySecondaryArduinoService


def run_server() -> None:
    app = web.Application()
    app.add_routes(routes=routes)

    provide(app=app, value=PrimaryArduinoService(),
            valueType=PrimaryService)
    provide(app=app, value="",
            valueType=SecondaryService)

    provide(app=app, value=ServerState(
        camera_port=6,
        standard_arduino_constants=ArduinoConstants(
            acc100=30,
            acc50=50,
            cc100=100,
            cc50=50,
            is_double=True,
            max_speed=50,
        )
    ), valueType=ServerState)
    provide(app=app, value=PrimaryServiceState(),
            valueType=PrimaryServiceState)

    add_background_task(
        app=app,
        task_func=connect_to_arduinos
    )
    add_background_task(
        app=app,
        task_func=update_state_with_current_sensor_data,
    )

    web.run_app(app, host='localhost', port=9000)


def run_test_server() -> None:
    app = web.Application()
    app.add_routes(routes=routes)

    provide(app=app,
            value=DummyPrimaryArduinoService(),
            valueType=PrimaryService)
    provide(app=app,
            value=DummySecondaryArduinoService(),
            valueType=SecondaryService)

    provide(app=app, value=ServerState(
        camera_port=6,
        standard_arduino_constants=ArduinoConstants(
            acc100=30,
            acc50=50,
            cc100=100,
            cc50=50,
            is_double=True,
            max_speed=50,
        )
    ), valueType=ServerState)
    provide(app=app,
            value=PrimaryServiceState(),
            valueType=PrimaryServiceState)
    provide(app=app,
            value=RubiksDatabaseService(database_file_name="db_cube.csv"),
            valueType=RubiksDatabaseService
            )

    add_background_task(
        app=app,
        task_func=connect_to_arduinos
    )
    add_background_task(
        app=app,
        task_func=update_state_with_current_sensor_data,
    )
    add_background_task(
        app=app,
        task_func=handle_primary_updates
    )

    web.run_app(app, host='192.168.0.42', port=9000)
