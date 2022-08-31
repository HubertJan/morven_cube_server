from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.models.cube_pattern import CubePattern
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.helper.cubeSimulator import CubeSimulator


@routes.patch("/verifiedPattern/{pattern}")
async def handle_possible_pattern_get(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    verified_pattern = request.match_info["pattern"]
    if CubeSimulator.validate_pattern(verified_pattern) == False:
        raise Exception()
    state.cube_pattern = CubePattern(verified_pattern)
    return web.json_response(
        data={
            "pattern": state.cube_pattern.pattern
        },
        status=200
    )
