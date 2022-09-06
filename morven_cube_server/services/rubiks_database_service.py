from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.runthrough import Runthrough
from morven_cube_server.services.api.database import LocalFileDatabase


class RubiksDatabaseService:

    def __init__(self, database_file_name: str):
        self._database = LocalFileDatabase(
            database_file_name=database_file_name)

    def add_finished_runthrough(self, report: EndOfProgramReport, date: str, start_pattern: str, arduino_constants: ArduinoConstants) -> None:
        runthrough = Runthrough.of_report(report, date=date,arduino_constants=arduino_constants, start_pattern=start_pattern)
        runthrough_dict = runthrough.__dict__
        data = {}
        for key, value in runthrough_dict.items():
            data[key] = str(value)
        self._database.add_record(data)

    @property
    def runthroughs(self) -> list[Runthrough]:
        records = self._database.records
        runs = []
        for record in records:
            runs.append(Runthrough(
                id=record["id"],
                instructions=record["instructions"],
                start_pattern=record["start_pattern"],
                runtime=int(record["runtime"]),
                date=record["date"],
                acc50=int(record["acc50"]),
                acc100=int(record["acc100"]),
                cc50=int(record["cc50"]),
                cc100=int(record["cc100"]),
                is_double=bool(record["is_double"]),
                max_speed=int(record["max_speed"])
            ))
        return runs
