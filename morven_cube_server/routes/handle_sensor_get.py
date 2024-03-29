from aiohttp import web
from morven_cube_server.routes.routes_object import routes
from morven_cube_server.services.primary_service import PrimaryService
from morven_cube_server.states.primary_arduino_state import PrimaryServiceState
from morven_cube_server.states.server_state import SensorData, ServerState
from morven_cube_server.state_handler.provider import consume


@routes.get('/sensor')
async def handler_get_sensor(request: web.Request) -> web.Response:
    state = consume(request.app, valueType=ServerState)
    resp = _create_json_response_of_current_sensor_data(
        sensor_data=state.sensor_data
    )
    return resp


def _create_json_response_of_current_sensor_data(sensor_data: SensorData) -> web.Response:
    return web.json_response(
        data={
            "temp":  sensor_data.temp1,
            "temp2": sensor_data.temp2,
            "temp3": sensor_data.temp3,
            "volt1": sensor_data.volt1,
            "volt2": sensor_data.volt2,
            "volt3": sensor_data.volt3,
        },
        status=200
    )
