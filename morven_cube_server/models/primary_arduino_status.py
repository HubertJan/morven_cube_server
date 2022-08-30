from enum import Enum

from morven_cube_server.models.program import Program


class PrimaryArduinoStatus(Enum):
    IDLE=0
    RUNNING=1
    PAUSED=2