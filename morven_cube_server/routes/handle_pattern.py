
from audioop import mul
from email.policy import default
import typing
from xmlrpc.client import Server
from aiohttp import web, multipart
from morven_cube_server import routes
from morven_cube_server.helper.cubeSimulator import CubeSimulator
from morven_cube_server.helper.kociemba_extend import Kociemba
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.program import Program
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService

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


def _update_arduino_constants_by_query(constants: ArduinoConstants, query) -> ArduinoConstants:
    updated_constants = constants.update()
    for key, value in query.items():
        match key:
            case "cc50":
                updated_constants = constants.update(cc50=int(value))
    return updated_constants

def _extract_pattern(request: web.Request) -> str:
    new_pattern = request.match_info["pattern"]
    match new_pattern:
        case "solve":
            new_pattern = ""
        case "scramble":
            new_pattern = CubeSimulator.generate_scramble()
        case _:
            if CubeSimulator.validate_pattern(new_pattern) == False:
                raise Exception()
    return new_pattern
            
@routes.patch("/pattern/{pattern}")    
async def handlerPatchPattern(self, request: web.Request):
    state = consume(request.app, valueType=ServerState)
    if state.cube_pattern is None:
        raise Exception()
    if state.primary_arduino_status != PrimaryArduinoStatus.IDLE:
        raise Exception()
    arduino = consume(request.app, valueType=PrimaryArduinoService)
    patched_pattern = _extract_pattern(request=request)
    instructions = Kociemba.solve(state.cube_pattern, patched_pattern)
    updated_conts = _update_arduino_constants_by_query(state.standard_arduino_constants, request.query)
    program = Program(
        arduino_constants=updated_conts,
        start_pattern=state.cube_pattern,
        id=0,
        instructions=instructions
    )
    await arduino.send_program(program)
    