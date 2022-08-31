import re
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.runthrough import Runthrough
from morven_cube_server.services.database import LocalFileDatabase


class RubiksDatabaseService:

    def __init__(self, database_file_name: str):
        self._database = LocalFileDatabase(
            database_file_name=database_file_name)

    def add_finished_runthrough(self, report: EndOfProgramReport, date: str) -> None:
        runthrough = Runthrough.of_report(report, date)
        runthrough_dict = runthrough.__dict__
        data = {}
        for key, value in runthrough_dict.items():
            data[key] = str(value)
        self._database.add_record(data)

    @property
    def runthroughs(self) -> list[dict[str, str]]:
        records = self._database.records
        return records
