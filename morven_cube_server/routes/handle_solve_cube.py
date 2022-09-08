from typing import Any
import uuid
from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.helper.cube_simulator import CubeSimulator
from morven_cube_server.helper.kociemba_extend import Kociemba
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.program import Program
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState

from morven_cube_server.state_handler.provider import consume


async def _update_arduino_constants_by_body(constants: ArduinoConstants, request: web.Request) -> ArduinoConstants:
    if not request.has_body:
        return constants
    data = await request.json()
    updated_constants = constants.update()
    for key, value in data.items():  # type: ignore
        match key:
            case "cc50":
                updated_constants = constants.update(cc50=int(value))
            case "cc100":
                updated_constants = constants.update(cc100=int(value))
            case "acc50":
                updated_constants = constants.update(acc50=int(value))
            case "acc100":
                updated_constants = constants.update(acc100=int(value))
            case "maxSp":
                updated_constants = constants.update(max_speed=int(value))
            case "isDouble":
                updated_constants = constants.update(is_double=bool(value))
    return updated_constants


def _extract_pattern(request: web.Request) -> str:
    pattern = request.match_info["pattern"]
    match pattern:
        case "solve":
            pattern = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        case "scramble":
            pattern = CubeSimulator.generate_scramble()
        case _:
            if CubeSimulator.validate_pattern(pattern) == False:
                raise Exception()
    return pattern


@routes.post("/solveCube/{pattern}")
async def handle_pattern_patch(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    arduino_state = consume(request.app, valueType=PrimaryServiceState)
    if state.cube_pattern is None:
        raise Exception()
    if arduino_state.status != PrimaryArduinoStatus.IDLING:
        raise Exception()
    arduino = consume(request.app, valueType=PrimaryService)
    patched_pattern = _extract_pattern(request=request)
    instructions = Kociemba.solve(str(state.cube_pattern), patched_pattern)

    updated_conts = await _update_arduino_constants_by_body(
        state.standard_arduino_constants, request)
    program = Program(
        arduino_constants=updated_conts,
        start_pattern=str(state.cube_pattern),
        id=str(uuid.uuid4()),
        instructions=instructions
    )

    await arduino.send_program(program)
    arduino_state.current_program = program
    arduino_state.status = PrimaryArduinoStatus.RUNNING
    return web.json_response(
        data={
            "id": program.id
        },
        status=200
    )
