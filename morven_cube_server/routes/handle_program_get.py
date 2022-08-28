from aiohttp import web
from routes import routes
from morven_cube_server.models.server_state import ServerState


@routes.get('/program')
async def handle_program_get(request: web.Request) -> web.Response:
    server_state = ServerState.of(request)
    if server_state.current_program == None:
        resp = web.json_response(
            {
                "currentProgram": None,
            },
            status=200
        )
    else:
        program = server_state.current_program
        resp = web.json_response(
            {
                "currentProgram": program.instructions,
                "currentProgramId": program.id,
                "currentInstructionId": program,
            },
            status=200
        )
    return resp