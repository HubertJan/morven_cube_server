from aiohttp import web
from morven_cube_server.provide import consume
from morven_cube_server.models.server_state import ServerState



@routes.get('/possiblePattern')
async def handle_possible_pattern_get(request: web.Request) -> web.Response():
    camera = consume(request.app, valueType=CameraService)
    img = await camera.shootImage()
    possible_pattern = detect_pattern(img)
    return convert_pattern_to_response(possible_pattern)