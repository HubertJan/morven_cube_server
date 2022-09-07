from abc import ABC, abstractmethod
from typing import AsyncGenerator, AsyncIterator, Awaitable, Generator, Protocol
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.running_program_report import RunningProgramReport

from morven_cube_server.states.server_state import SensorData
from morven_cube_server.state_handler.notifier import Notifier, SupportsAddListener


class _PrimaryService(SupportsAddListener, Protocol):
    async def connect(self, port: int, baudrate: int) -> None:
        pass

    @property
    def port(self) -> int:
        pass

    @property
    def port(self) -> int:
        pass

    def handle_received_updates(self) -> AsyncIterator[EndOfProgramReport]:
        pass

    async def send_program(self, program: Program) -> None:
        pass

    async def rotate_cube(self, rotationInDegree: int) -> None:
        pass
    


class PrimaryService(_PrimaryService):
    pass
