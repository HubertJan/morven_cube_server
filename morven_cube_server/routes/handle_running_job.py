from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState
from morven_cube_server.states.server_state import SensorData, ServerState
from morven_cube_server.state_handler.provider import consume


@routes.get('/runningJob')
async def handler_get_sensor(request: web.Request) -> web.Response:
    arduino_state = consume(request.app, valueType=PrimaryServiceState)
    if arduino_state.current_program is None:
        return web.json_response(
            status=204
        )
    return web.json_response(
        data={
            "instructions":  arduino_state.current_program.instructions,
            "startPattern": arduino_state.current_program.start_pattern,
            "id": arduino_state.current_program.id,
            "settings": arduino_state.current_program.arduino_constants.__dict__,
        },
        status=200
    )
