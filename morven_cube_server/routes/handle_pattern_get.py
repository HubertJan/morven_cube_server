from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.states.server_state import ServerState

from morven_cube_server.state_handler.provider import consume


@routes.get("/pattern")
async def handler_pattern_get(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    if state.cube_pattern is None:
        raise Exception()
    resp = web.json_response(
        {
            "pattern": str(state.cube_pattern)
        },
        status=200
    )
    return resp
