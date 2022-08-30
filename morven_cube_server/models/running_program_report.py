from dataclasses import dataclass
from morven_cube_server.models.program import Program

@dataclass(frozen=True)
class RunningProgramReport:
    program: Program
    latest_finished_instruction_id: int
    current_run_time: int