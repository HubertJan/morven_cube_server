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


@routes.get("/runthroughs/{id}")
async def handler_pattern_get(request: web.Request) -> web.Response:
    db = consume(request.app, valueType=RubiksDatabaseService)
    id = request.match_info["id"]

    runs = db.runthroughs
    searched_run = None
    for run in runs:
        if run.id == id:
            searched_run = run
            break
    if searched_run == None:
        raise Exception("Could not find runthrough with id")
    resp = web.json_response(
        {
            "id": searched_run.id,
            "instructions": searched_run.instructions,
            "startPattern": searched_run.start_pattern,
            "runtime": searched_run.runtime,
            "date": searched_run.date,
            "acc50": searched_run.acc50,
            "acc100": searched_run.acc100,
            "cc50": searched_run.cc50,
            "cc100": searched_run.cc100,
            "isDouble": searched_run.is_double,
            "maxSpeed": searched_run.max_speed,
        },
        status=200
    )
    return resp
