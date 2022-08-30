from abc import ABC, abstractmethod
from typing import AsyncGenerator, Awaitable, Generator
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.running_program_report import RunningProgramReport

from morven_cube_server.states.server_state import SensorData


class IPrimaryArduinoService(ABC):

    @abstractmethod
    async def connect(self, port: int, baudrate: int):
        pass

    @property # type: ignore[misc]
    @abstractmethod
    def port(self) -> int:
        pass

    @property # type: ignore[misc]
    @abstractmethod
    def port(self) -> int:
        pass

    @abstractmethod
    async def handle_received_updates(self) -> AsyncGenerator[EndOfProgramReport | RunningProgramReport, None]:
        pass

    @abstractmethod
    async def send_program(self, program: Program) -> Awaitable[None]:
        pass