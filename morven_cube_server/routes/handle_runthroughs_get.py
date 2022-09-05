from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.services.rubiks_database_service import RubiksDatabaseService
from morven_cube_server.state_handler.provider import consume


def _is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except:
        return False


@routes.get("/runthroughs/{specific}")
async def handler_pattern_get(request: web.Request) -> web.Response:
    db = consume(request.app, valueType=RubiksDatabaseService)
    specific = request.match_info["specific"]
    run_index = None
    if specific == "latest":
        run_index = -1
    if run_index is None:
        if not _is_int(specific):
            raise Exception()
        run_index = int(specific)

    runs = db.runthroughs
    if len(runs) <= run_index:
        raise Exception()

    run = runs[run_index]
    resp = web.json_response(
        {
            "id": run.id,
            "instructions": run.instructions,
            "startPattern": run.start_pattern,
            "runtime": run.runtime,
            "date": run.date,
            "acc50": run.acc50,
            "acc100": run.acc100,
            "cc50": run.cc50,
            "cc100": run.cc100,
            "isDouble": run.is_double,
            "maxSpeed": run.max_speed,
        },
        status=200
    )
    return resp
