from abc import ABC, abstractmethod
from typing import Generator

from morven_cube_server.states.server_state import SensorData


class ISecondaryArduinoService(ABC):

    @abstractmethod
    async def connect(self, port: int, baudrate: int) -> None:
        pass

    @property  # type: ignore[misc]
    @abstractmethod
    def port(self) -> int:
        pass

    @property  # type: ignore[misc]
    @abstractmethod
    def port(self) -> int:
        pass

    @abstractmethod
    async def handle_received_sensor_data(self) -> Generator[SensorData, None, None]:
        pass
