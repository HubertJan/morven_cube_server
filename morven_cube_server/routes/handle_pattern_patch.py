import asyncio
import json
from typing import Any
from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.helper.cubeSimulator import CubeSimulator
from morven_cube_server.helper.kociemba_extend import Kociemba
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus
from morven_cube_server.models.program import Program
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState

from morven_cube_server.state_handler.provider import consume


def _update_arduino_constants_by_query(constants: ArduinoConstants, query: Any) -> ArduinoConstants:
    updated_constants = constants.update()
    for key, value in query.items():  # type: ignore
        match key:
            case "cc50":
                updated_constants = constants.update(cc50=int(value))
    return updated_constants


def _extract_pattern(request: web.Request) -> str:
    new_pattern = request.match_info["pattern"]
    match new_pattern:
        case "solve":
            new_pattern = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        case "scramble":
            new_pattern = CubeSimulator.generate_scramble()
        case _:
            if CubeSimulator.validate_pattern(new_pattern) == False:
                raise Exception()
    return new_pattern


@routes.patch("/pattern/{pattern}")
async def handle_pattern_patch(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    arduino_state = consume(request.app, valueType=PrimaryArduinoState)
    if state.cube_pattern is None:
        raise Exception()
    if arduino_state.status != PrimaryArduinoStatus.IDLING:
        raise Exception()
    arduino = consume(request.app, valueType=PrimaryService)
    patched_pattern = _extract_pattern(request=request)
    instructions = Kociemba.solve(state.cube_pattern.pattern, patched_pattern)
    updated_conts = _update_arduino_constants_by_query(
        state.standard_arduino_constants, request.query)
    program = Program(
        arduino_constants=updated_conts,
        start_pattern=state.cube_pattern.pattern,
        id=0,
        instructions=instructions
    )
    await arduino.send_program(program)
    arduino_state.current_program = program
    arduino_state.status = PrimaryArduinoStatus.RUNNING
    return web.json_response(
        data={
            "program_id": program.id
        },
        status=200
    )
