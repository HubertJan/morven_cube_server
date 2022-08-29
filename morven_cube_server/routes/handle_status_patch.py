async def handlerPatchStatus(self, request):
    command = request.rel_url.name
    if command != "RUN" or command != "PAUSE":
        return web.json_response(
            status=403
        )
    await self._mainArduinoConnection.sendStatus(command)
    resp = web.json_response(
        {
            "status": self._status,
        },
        status=200
    )
    return resp