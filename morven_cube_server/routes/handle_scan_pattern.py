from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.states.server_state import ServerState

@routes.get("/scanPattern")
async def handle_scan_pattern_get(request: web.Request) -> web.Response():
    state = consume(request.app, valueType=ServerState)
    """ img = capture_image(state.camera_port)
    possible_pattern = detect_pattern(img) """
    return web.json_response(
        {
            "pattern": "FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL" 
        },
        status=200
    )
