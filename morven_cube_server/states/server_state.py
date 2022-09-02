from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import AsyncGenerator, AsyncIterator, Optional

from morven_cube_server.models.cube_pattern import CubePattern

from morven_cube_server.models.program_settings import ArduinoConstants


@dataclass(frozen=True)
class SensorData:
    temp1: Optional[int] = None
    temp2: Optional[int] = None
    temp3: Optional[int] = None
    volt1: Optional[int] = None
    volt2: Optional[int] = None
    volt3: Optional[int] = None

    def update(self,  temp1: Optional[int] = None,
               temp2: Optional[int] = None,
               temp3: Optional[int] = None,
               volt1: Optional[int] = None,
               volt2: Optional[int] = None,
               volt3: Optional[int] = None,
               ) -> SensorData:
        return SensorData(
            temp1=temp1 if temp1 is not None else self.temp1,
            temp2=temp2 if temp2 is not None else self.temp2,
            temp3=temp3 if temp3 is not None else self.temp1,
            volt1=volt1 if volt1 is not None else self.volt1,
            volt2=volt2 if volt2 is not None else self.volt2,
            volt3=volt3 if volt3 is not None else self.volt3
        )


@dataclass
class ServerState:
    camera_port: int
    standard_arduino_constants: ArduinoConstants
    cube_pattern: Optional[CubePattern] = None
    sensor_data: SensorData = SensorData()

    async def update_sensor_data_by_receiving_data(self, receiving_data: AsyncIterator[SensorData]) -> None:
        async for data in receiving_data:
            self.sensor_data = data
