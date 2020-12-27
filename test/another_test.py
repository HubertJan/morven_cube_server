import asyncio
import serial_asyncio
from aiohttp import web


async def main():

    reader, writer = await serial_asyncio.open_serial_connection(url='/COM6', baudrate=9600)
    print('Reader created')
    messages = [b'program\n', b'status\n', ]
    sent = send(writer, messages)
    received = recv(reader)
    await reader.readuntil(b'\n')
    await reader.readuntil(b'\n')

    server = web.Application()
    routes = [
            web.get("/test", handlerTest),
    ]
    server.router.add_routes(routes)

    await asyncio.gather(
        web._run_app(server,  host='localhost', port=9000),
        received,
        sent
    )

def handlerTest(request):
    print("Yeah")
    resp = web.json_response(
        {
            "value": "fuck america",
        }
    )
    return resp


async def send(w, msgs):
    for msg in msgs:
        w.write(msg)
        print(f'sent: {msg.decode().rstrip()}')
        await asyncio.sleep(0.5)
    print('Done sending')


async def recv(r):
    while True:
        msg = await r.readuntil(b'\n')
        print(msg)

asyncio.run(main())