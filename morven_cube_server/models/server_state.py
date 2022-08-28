from dataclasses import dataclass
from enum import Enum
from typing import Optional
from __future__ import annotations

from morven_cube_server.models.cube_pattern import CubePattern
from morven_cube_server.models.program import Program
from aiohttp import web

class ServerStatus(Enum):
    NOTFETCHED = 0
    IDLE = 1
    RUN = 2
    DONE = 3


@dataclass
class SensorData:
    _temp1: int
    _temp2: int
    _temp3: int
    _volt1: int
    _volt2: int
    _volt3: int
    
@dataclass
class ServerState:
    status: ServerStatus
    cube_pattern: CubePattern
    current_program: Optional[Program]

    @classmethod
    def of(cls, request: web.Request) -> ServerState:
        state = request.app["serverState"]
        if state == None or type(state) is not ServerState:
            raise Exception("No ServerState stored.")
        return state