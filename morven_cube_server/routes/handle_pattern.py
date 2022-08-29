
from aiohttp import web
from morven_cube_server.models.server_state import ServerState

from morven_cube_server.provide import consume


async def handler_pattern_get(self, request: web.Request):
    state = consume(request.app, valueType=ServerState)
    if state.cube_pattern is None:
        raise Exception()
    resp = web.json_response(
        {
            "currentPattern": state.cube_pattern
        },
        status=200
    )
    return resp

def getOptionalArguemnts(self, optionalArguments: dict, data):
    for key in optionalArguments.keys():
        if key in data:
            optionalArguments[key] = data[key]
    return optionalArguments
    
async def handlerPatchPattern(self, request):

    if(self._status == "RUN"):
        return web.json_response(
            {
                "msg": "A program is already running."
            },
            status=403)
    optionalArguments = {
        "isDouble": True,
        "acc50": 42000,
        "acc100": 4300,
        "cc50": 19,
        "cc100": 20,
        "maxSp": 4000,
    }
    optionalArguments = self.getOptionalArguemnts(
        optionalArguments, request.rel_url.query)
    command = request.rel_url.name
    if(command == "solve" or command == ""):
        inst = kociemba.solve(self._cubePattern.pattern)
        resp = await self._createAndSendProgramByInstructions(inst, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
    elif(command == "scramble"):
        inst = CubeSimulator.getScramble()
        resp = await self._createAndSendProgramByInstructions(inst, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
    else:
        pattern = command
        resp = await self._createAndSendProgramByPattern(pattern, isDouble=optionalArguments["isDouble"], acc50=optionalArguments["acc50"], acc100=optionalArguments["acc100"], cc50=optionalArguments["cc50"], cc100=optionalArguments["cc100"], maxSp=optionalArguments["maxSp"])
    return resp