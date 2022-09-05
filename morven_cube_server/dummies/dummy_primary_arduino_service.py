

import asyncio
from inspect import Parameter
from optparse import Option
from typing import AsyncIterator, Optional
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.services.primary_service import PrimaryService


class DummyPrimaryArduinoService(PrimaryService):
    _current_program: Optional[Program] = None

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

    async def handle_received_updates(self) -> AsyncIterator[EndOfProgramReport]:
        while True:
            await asyncio.sleep(0.1)
            if self._current_program is None:
                continue
            yield EndOfProgramReport(
                program=self._current_program,
                runtime=5
            )
            self._current_program = None

    async def send_program(self, program: Program) -> None:
        await asyncio.sleep(0.1)
        self._current_program: Optional[Program] = program
