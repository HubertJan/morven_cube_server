from xmlrpc.client import Server
import pytest
from aiohttp import web

from morven_cube_server.all_routes import routes
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.interface_primary_arduino_service import IPrimaryArduinoService
from morven_cube_server.state_handler.provider import provide
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState
from morven_cube_server.states.server_state import SensorData, ServerState, ServerStatus
from tests.dummies.dummy_primary_arduino_service import DummyPrimaryArduinoService


@pytest.fixture  # type: ignore
def cli(loop, aiohttp_client):  # type: ignore
    app = web.Application()
    app.add_routes(routes)
    provide(app=app, value=ServerState(
        camera_port=0,
        standard_arduino_constants=ArduinoConstants(
            acc100=50,
            acc50=50,
            cc100=3,
            cc50=3,
            is_double=True,
            max_speed=30
        ),
    ), valueType=ServerState)
    provide(app=app, value="yo",
            valueType=IPrimaryArduinoService)
    provide(app=app,
            value=PrimaryArduinoState(),
            valueType=PrimaryArduinoState
            )

    return loop.run_until_complete(aiohttp_client(app))  # type: ignore


async def test_get_sensor(cli) -> None:  # type: ignore
    resp = await cli.get('/sensor')  # type: ignore
    assert resp.status == 200  # type: ignore
