from enum import Enum

from morven_cube_server.models.program import Program


class PrimaryArduinoStatus(Enum):
    IDLING = 0
    RUNNING = 1
    PAUSING = 2
