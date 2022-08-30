import pytest
from aiohttp import web

from morven_cube_server.all_routes import routes
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.state_handler.provider import provide
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState
from morven_cube_server.states.server_state import SensorData, ServerState, ServerStatus


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.add_routes(routes)
    provide(app=app, value=ServerState(
        camera_port=0,
        cube_pattern=None,
        sensor_data=SensorData(
            temp1=None,
            temp2=None,
            temp3=None,
            volt1=None,
            volt2=None,
            volt3=None,
        ),
        standard_arduino_constants=ArduinoConstants(
            acc100=50,
            acc50=50,
            cc100=3,
            cc50=3,
            is_double=True,
            max_speed=30
        ),
        status=ServerStatus.NOTFETCHED,
    ), valueType=ServerState)
    provide(app=app, value=PrimaryArduinoState(
        current_program=None,
        last_instruction_id=None,
        status=PrimaryArduinoStatus.IDLE
    ),
        valueType=PrimaryArduinoState
    )

    return loop.run_until_complete(aiohttp_client(app))


async def test_get_sensor(cli):
    resp = await cli.get('/sensor')
    assert resp.status == 200
