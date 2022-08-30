from dataclasses import dataclass
from typing import Optional

from morven_cube_server.models.program import Program
from morven_cube_server.models.primary_arduino_status import PrimaryArduinoStatus


@dataclass
class PrimaryArduinoState:
    status: Optional[PrimaryArduinoStatus] = None
    current_program: Optional[Program] = None
    last_instruction_id: Optional[int] = None
