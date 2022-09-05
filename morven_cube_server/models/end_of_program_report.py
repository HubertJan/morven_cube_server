from dataclasses import dataclass
from morven_cube_server.models.program import Program


@dataclass(frozen=True)
class EndOfProgramReport:
    instructions: str
    program_id: str
    runtime: int
