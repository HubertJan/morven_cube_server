from aiohttp import web
from morven_cube_server import routes
from morven_cube_server.states.server_state import ServerState

from morven_cube_server.state_handler.provider import consume


@routes.get("pattern")
async def handler_pattern_get(self, request: web.Request):
    state = consume(request.app, valueType=ServerState)
    if state.cube_pattern is None:
        raise Exception()
    resp = web.json_response(
        {
            "pattern": state.cube_pattern.pattern
        },
        status=200
    )
    return resp

