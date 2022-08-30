from aiohttp import web
from morven_cube_server import routes
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.models.server_state import ServerState
from morven_cube_server.services.camera_service import capture_frame, capture_image


@routes.get('/verifiedPattern')
async def handle_possible_pattern_get(request: web.Request) -> web.Response:
    camera = consume(request.app, valueType=CameraService)
    img = await capture_image()
    possible_pattern = detect_pattern(img)
    return convert_pattern_to_response(possible_pattern)