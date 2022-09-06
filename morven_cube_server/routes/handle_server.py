from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState
from morven_cube_server.states.server_state import SensorData, ServerState
from morven_cube_server.state_handler.provider import consume


@routes.get('/server')
async def handler_get_sensor(request: web.Request) -> web.Response:
    return web.json_response(
        status=200
    )
