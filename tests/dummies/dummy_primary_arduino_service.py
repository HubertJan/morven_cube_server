

from morven_cube_server.services.interface_primary_arduino_service import IPrimaryArduinoService


class DummyPrimaryArduinoService(IPrimaryArduinoService):
    async def connect(self) -> None:
        pass
