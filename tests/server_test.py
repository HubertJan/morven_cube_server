
import asyncio
import json
from aiohttp import web
import pytest

from morven_cube_server.all_routes import routes
from morven_cube_server.helper.cube_simulator import CubeSimulator
from morven_cube_server.models.cube_pattern import CubePattern

from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.services.rubiks_database_service import RubiksDatabaseService
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.state_handler.provider import provide
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.state_handler.background_task import add_background_task
from morven_cube_server.background_tasks.connect_to_arduinos import connect_to_arduinos
from morven_cube_server.background_tasks.update_state_with_current_sensor_data import update_state_with_current_sensor_data
from morven_cube_server.background_tasks.handle_primary_updates import handle_primary_updates

from morven_cube_server.dummies.dummy_primary_arduino_service import DummyPrimaryArduinoService
from morven_cube_server.dummies.dummy_secondary_arduino_service import DummySecondaryArduinoService


def create_app():
    app = web.Application()
    app.add_routes(routes)
    provide(app=app, value=ServerState(
        camera_port=0,
        cube_pattern=CubePattern(
            patttern=CubeSimulator.to_format("DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD")),
        standard_arduino_constants=ArduinoConstants(
            acc100=50,
            acc50=50,
            cc100=3,
            cc50=3,
            is_double=True,
            max_speed=30
        ),
    ), valueType=ServerState)
    provide(app=app,
            value=DummyPrimaryArduinoService(),
            valueType=PrimaryService)
    provide(app=app,
            value=PrimaryServiceState(),
            valueType=PrimaryServiceState)
    provide(app=app,
            value=DummySecondaryArduinoService(),
            valueType=SecondaryService)
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

    return app


@pytest.mark.asyncio
async def test_sensor_update(aiohttp_client):
    client = await aiohttp_client(create_app())
    await asyncio.sleep(5)
    resp = await client.get('/sensor')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["temp2"] >= 0


@pytest.mark.asyncio
async def test_pattern_patch(aiohttp_client):
    client = await aiohttp_client(create_app())
    await asyncio.sleep(10)
    resp = await client.patch('/pattern/solve')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["program_id"] == 0
    await asyncio.sleep(5)
    resp = await client.get('/pattern')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["pattern"] == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"


@pytest.mark.asyncio
async def test_runthrough_latest_get(aiohttp_client):
    client = await aiohttp_client(create_app())
    await asyncio.sleep(10)
    resp = await client.patch('/pattern/solve')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["program_id"] == 0
    await asyncio.sleep(5)
    resp = await client.get('/runthroughs/latest')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["id"] == 0


@pytest.mark.asyncio
async def test_pattern_get(aiohttp_client):
    client = await aiohttp_client(create_app())
    await asyncio.sleep(10)
    resp = await client.get('/pattern')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["pattern"] == "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"


@pytest.mark.asyncio
async def test_verified_pattern_patch(aiohttp_client):
    client = await aiohttp_client(create_app())
    await asyncio.sleep(10)
    resp = await client.patch('/verifiedPattern/FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL')
    assert resp.status == 200
    text = await resp.text()
    data = json.loads(text)
    assert data["pattern"] == "FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL"
