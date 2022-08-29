async def handlerGetRecords(self, request):
    resp = web.json_response(
        {
            "records": self._db.records,
        },
        status=200
    )
    return resp