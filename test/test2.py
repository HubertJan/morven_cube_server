import asyncio
import aioconsole

isRunning = True


async def main():
    print("Test")
    await asyncio.wait([
        receiveOutputs(),
        sendInputs()
    ])

async def receiveOutputs():
    global isRunning
    while isRunning:
        await aioconsole.ainput('Enter something: ') 
        print("Received Input")
        

async def sendInputs():
    global isRunning
    while isRunning:
        print("\nInputs are sent")
        await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())