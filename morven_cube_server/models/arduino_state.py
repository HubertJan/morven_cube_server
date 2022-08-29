from enum import Enum

from morven_cube_server.models.program import Program


class EndOfProgramReport:
    program: Program
    run_time: int

class RunningProgramReport:
    program: Program
    latest_finished_instruction_id: int
    current_run_time: int

class PrimaryArduinoStatus(Enum):
    IDLE=0
    RUN=1
    PAUSE=2