from aiohttp import web
from morven_cube_server.models.cube_pattern import CubePattern
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
        _convert_runthrough_to_dict(searched_run),
        status=200
    )
    return resp


def _convert_runthrough_to_dict(runthrough: dict[str, any]):
    return {
        "id": runthrough.id,
        "instructions": runthrough.instructions,
        "startPattern": runthrough.start_pattern,
        "endPattern": str(CubePattern(runthrough.start_pattern).execute_instructions(runthrough.instructions)),
        "runtime": runthrough.runtime,
        "date": runthrough.date,
        "acc50": runthrough.acc50,
        "acc100": runthrough.acc100,
        "cc50": runthrough.cc50,
        "cc100": runthrough.cc100,
        "isDouble": runthrough.is_double,
        "maxSpeed": runthrough.max_speed,
    }


@routes.get("/runthroughs")
async def handler_pattern_get(request: web.Request) -> web.Response:
    db = consume(request.app, valueType=RubiksDatabaseService)
    runs = db.runthroughs
    data = []
    for run in runs:
        data.append(_convert_runthrough_to_dict(run))
    resp = web.json_response(
        {
            "data": data
        },
        status=200
    )
    return resp
