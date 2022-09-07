from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.services.camera_service import capture_image

@routes.get("/scanPattern")
async def handle_scan_pattern_get(request: web.Request) -> web.Response():
    state = consume(request.app, valueType=ServerState)
    primaryService = consume(request.app, valueType=PrimaryService)
    secondaryService = consume(request.app, valueType=SecondaryService)

    await secondaryService.open_flap()
    await primaryService.rotate_cube(45)
    await secondaryService.turn_on_white_light()
    cube_sides = []
    for i in range(0, 4):
        img = capture_image(state.camera_port)
        cube_sides[i] = detect_pattern(img)
    await secondaryService.turn_off_white_light()
    await secondaryService.close_flap()
    await primaryService.rotate_cube(-45)

    """ img = capture_image(state.camera_port)
    possible_pattern = detect_pattern(img) """
    return web.json_response(
        {
            "pattern": "FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL" 
        },
        status=200
    )
