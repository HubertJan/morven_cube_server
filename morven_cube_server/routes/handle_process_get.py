    
async def handlerGetProcess(self, request):
    resp = web.json_response(
        {
            "status": self._status,
            "program":  self._currentProgram.instructions if self._currentProgram.instructions != None else "",
            "programId": self._currentProgram.id if self._currentProgram.id != None else "",
            "currentInstructionId": self._currentInstructionId if self._currentInstructionId != None else "",
            "startPattern": self._currentProgram.startPattern,
            "endPattern": self._currentProgram.endPattern,
            "time": self._programRunningTime,
        },
        status=200
    )
    return resp