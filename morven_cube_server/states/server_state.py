from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import AsyncGenerator, Optional

from morven_cube_server.models.cube_pattern import CubePattern

from morven_cube_server.models.program_settings import ArduinoConstants


class ServerStatus(Enum):
    NOTFETCHED = 0
    READY = 1


@dataclass(frozen=True)
class SensorData:
    temp1: Optional[int] = None
    temp2: Optional[int] = None
    temp3: Optional[int] = None
    volt1: Optional[int] = None
    volt2: Optional[int] = None
    volt3: Optional[int] = None


@dataclass
class ServerState:
    camera_port: int
    standard_arduino_constants: ArduinoConstants
    status: ServerStatus = ServerStatus.NOTFETCHED
    cube_pattern: Optional[CubePattern] = None
    sensor_data: SensorData = SensorData()

    async def update_sensor_data_by_receiving_data(self, receiving_data: AsyncGenerator[SensorData, None]):
        async for data in receiving_data:
            self.sensor_data = data
