import imp
from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService
from cube_image_scanner import analyze_image_for_cube_face_and_one_row
from cube_image_scanner.models.standard_cube_face import CubeDirections
from cube_image_scanner.models.standard_cube_face import StandardCubeFace
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.state_handler.provider import consume
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.services.camera_service import capture_image
from morven_cube_server.helper.guess_cube_face import calculate_up_cube_face, StandardCubePattern, convert_standard_cube_pattern_to_pattern_string


@routes.get("/scanPattern")
async def handle_scan_pattern_get(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    primaryService = consume(request.app, valueType=PrimaryService)
    secondaryService = consume(request.app, valueType=SecondaryService)


    await secondaryService.open_flap()
    await primaryService.rotate_cube(45)
    await secondaryService.turn_on_white_light()
    cube_faces: list[StandardCubeFace] = []
    bottom_face = StandardCubeFace()
    for i in range(0, 4):
        img = None
        attempts = 0
        is_done = False
        while not is_done:
            try:
                img = capture_image(state.camera_port)
                (cube_faces[i], row) = analyze_image_for_cube_face_and_one_row(
                    img)
                is_done = True
            except:
                attempts += 1
                if attempts >= 10:
                    raise Exception("Unable to scan cube")
        bottom_face.apply_row_to(row, direction=CubeDirections(i))
    up_face = calculate_up_cube_face(
        StandardCubePattern(
            front=cube_faces[0],
            left=cube_faces[1],
            back=cube_faces[2],
            right=cube_faces[3],
            down=bottom_face,
            up=StandardCubeFace()
        )
    )
    pattern = StandardCubePattern(
        front=cube_faces[0],
        left=cube_faces[1],
        back=cube_faces[2],
        right=cube_faces[3],
        down=bottom_face,
        up=up_face
    )

    await secondaryService.turn_off_white_light()
    await secondaryService.close_flap()
    await primaryService.rotate_cube(-45)
    scanned_pattern_string = convert_standard_cube_pattern_to_pattern_string(
        pattern)
    return web.json_response(
        {
            "pattern": scanned_pattern_string
        },
        status=200
    )
