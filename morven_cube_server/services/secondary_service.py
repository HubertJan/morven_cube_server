from abc import ABC, abstractmethod
from typing import AsyncIterator, Generator, Protocol
from morven_cube_server.state_handler.notifier import Notifier

from morven_cube_server.states.server_state import SensorData
from morven_cube_server.state_handler.notifier import SupportsAddListener


class _SecondaryService(SupportsAddListener, Protocol):
    async def connect(self, port: int, baudrate: int) -> None:
        pass

    @property
    def port(self) -> int:
        pass

    @property
    def port(self) -> int:
        pass

    def handle_received_sensor_data(self) -> AsyncIterator[SensorData]:
        pass


class SecondaryService(_SecondaryService):
    pass
