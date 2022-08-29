from aiohttp import web
from morven_cube_server import routes
from morven_cube_server.models.server_state import ServerState
from morven_cube_server.provide import consume

@routes.get('/program')
async def handlerGetSensor(self, request: web.Request):
    state = consume(request.app, valueType=ServerState)
    resp = web.json_response(
        {
            "temp":  state.sensor_data["temp1"],
            "temp2": state.sensor_data["temp2"],
            "temp3": state.sensor_data["temp3"],
            "volt1": state.sensor_data["volt1"],
            "volt2": state.sensor_data["volt2"],
            "volt3": state.sensor_data["volt3"],
            "c2": 4
        },
        status=200
    )
    return resp