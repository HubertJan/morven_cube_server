import asyncio
from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService


async def test_connect():
    service = SecondaryArduinoService()
    await service.connect("/dev/cu.usbmodem73283201", 115200)


async def test_open_close_flap():
    service = SecondaryArduinoService()
    await service.connect("/dev/cu.usbmodem73283201", 115200)
    await service.open_flap()
    asyncio.sleep(5)
    await service.close_flap()


async def test_white_light():
    service = SecondaryArduinoService()
    await service.connect("/dev/cu.usbmodem73283201", 115200)
    await service.turn_on_white_light()
    asyncio.sleep(5)
    await service.turn_off_white_light()


async def test_clamp_unclamp_cube():
    service = SecondaryArduinoService()
    await service.connect("/dev/cu.usbmodem73283201", 115200)
    await service.clamp_cube()
    asyncio.sleep(5)
    await service.unclamp_cube()
