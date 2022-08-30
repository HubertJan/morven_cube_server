from aiohttp import web
from . import routes_object
from morven_cube_server.states.server_state import ServerState


async def handle_status_get(request: web.Request) -> web.Response:
    server_state = ServerState.of(request)
    resp = web.json_response(
        {
            "status": server_state.status,
        },
        status=200
    )
    return resp
