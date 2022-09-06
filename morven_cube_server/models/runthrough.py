from __future__ import annotations

from dataclasses import dataclass
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program_settings import ArduinoConstants


@dataclass(frozen=True)
class Runthrough:
    id: str
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
    def of_report(cls, report: EndOfProgramReport, arduino_constants: ArduinoConstants, start_pattern: str, date: str) -> Runthrough:
        consts = arduino_constants
        return Runthrough(
            id=report.program_id,
            instructions=report.instructions,
            start_pattern=start_pattern,
            runtime=report.runtime,
            date=date,
            acc50=consts.acc50,
            acc100=consts.acc100,
            cc50=consts.cc50,
            cc100=consts.cc100,
            is_double=consts.is_double,
            max_speed=consts.max_speed,
        )
