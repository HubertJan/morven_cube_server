import asyncio
import serial_asyncio

isRunning = True

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print(repr(data)[2:len(repr(data))-5])

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')


async def main():
    coro = serial_asyncio.create_serial_connection(loop, Output, 'COM6', baudrate=9600)
    serial_asyncio.
    await asyncio.wait([
        coro,
        sendInputs()
    ])

async def sendInputs():
    global isRunning
    while isRunning:
        print("\nInputs are sent")
        await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
