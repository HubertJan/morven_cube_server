from dataclasses import dataclass
from enum import Enum
from typing import AsyncGenerator, Optional
from __future__ import annotations
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus

from morven_cube_server.models.cube_pattern import CubePattern
from morven_cube_server.models.program import Program
from aiohttp import web

from morven_cube_server.models.program_settings import ArduinoConstants

class ServerStatus(Enum):
    NOTFETCHED = 0
    READY = 1

@dataclass
class SensorData:
    temp1: Optional[int]
    temp2: Optional[int]
    temp3: Optional[int]
    volt1: Optional[int]
    volt2: Optional[int]
    volt3: Optional[int]

@dataclass
class ServerState:
    status: ServerStatus
    cube_pattern: Optional[CubePattern]
    sensor_data: SensorData
    camera_port: int
    standard_arduino_constants: ArduinoConstants

    async def update_sensor_data_by_receiving_data(self, receiving_data: AsyncGenerator[SensorData, None]):
        async for data in receiving_data:
            self.sensor_data = data