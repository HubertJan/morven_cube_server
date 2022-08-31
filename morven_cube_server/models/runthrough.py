from __future__ import annotations

from dataclasses import dataclass
from morven_cube_server.models.end_of_program_report import EndOfProgramReport


@dataclass(frozen=True)
class Runthrough:
    id: int
    instructions: str
    start_pattern: str
    runtime: int
    date: str
    acc50: int
    acc100: int
    cc50: int
    cc100: int
    max_speed: int
    is_double: bool

    @classmethod
    def of_report(cls, report: EndOfProgramReport, date: str) -> Runthrough:
        program = report.program
        consts = program.arduino_constants
        return Runthrough(
            id=program.id,
            instructions=program.instructions,
            start_pattern=program.start_pattern,
            runtime=report.runtime,
            date=date,
            acc50=consts.acc50,
            acc100=consts.acc100,
            cc50=consts.cc50,
            cc100=consts.cc100,
            is_double=consts.is_double,
            max_speed=consts.max_speed,
        )
