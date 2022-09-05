

import asyncio
from inspect import Parameter
from random import randint
from typing import AsyncIterator, Optional
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.services.secondary_service import SecondaryService
from morven_cube_server.states.server_state import SensorData


class DummySecondaryArduinoService(SecondaryService):

    async def connect(self, port: int, baudrate: int) -> None:
        await asyncio.sleep(3)
        self._port = port
        self._baudrate = baudrate

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def baudrate(self) -> Optional[int]:
        return self._baudrate

    async def handle_received_sensor_data(self) -> AsyncIterator[EndOfProgramReport]:
        while True:
            await asyncio.sleep(5)
            yield SensorData(
                temp1=randint(10, 30),
                temp2=randint(10, 30),
                temp3=randint(10, 30),
                volt1=randint(1, 5),
                volt2=randint(1, 5),
                volt3=randint(1, 5),
            )
