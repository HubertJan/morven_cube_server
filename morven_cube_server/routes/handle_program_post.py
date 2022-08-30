from aiohttp import web
from routes import routes
from morven_cube_server.states.server_state import ServerState


async def handlerPostProgram(request: web.Request) -> web.Response:
    server_state = ServerState.of(request)
    if(server_state._status == "RUN"):
        return web.json_response(
            {
                "msg": "A program is already running."
            },
            status=403)
    inst = request.rel_url.name
    return await self._createAndSendProgramByInstructions(inst)