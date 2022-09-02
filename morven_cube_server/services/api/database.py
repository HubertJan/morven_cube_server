from typing import Optional
import pandas as pd
from pathlib import Path


class LocalFileDatabase:
    _data: Optional[pd.DataFrame]

    def __init__(self, database_file_name: str):
        self._data = None
        dirpath = Path(__file__).cwd().as_posix()
        self.dbFileURL = f'{dirpath}/{database_file_name}'
        self._read_file()

    def add_record(self, record: dict[str, str]) -> None:
        if self._data is None:
            raise Exception()
        self._data = self._data.append(record, ignore_index=True)
        self._save_file()

    @property
    def records(self) -> list[dict[str, str]]:
        records = []
        if self._data is None:
            raise Exception()
        self._read_file()
        record_map = {}
        for record in self._data.values:
            index = 0
            for key in self._data.keys():
                record_map[key] = record[index]
                index += 1
            records.append(record_map)
        return records

    def _save_file(self) -> None:
        try:
            if self._data is None:
                raise Exception()
            self._data.to_csv(self.dbFileURL, encoding='utf-8', index=False)
        except:
            print("database.py: Error writing to the db file: " + self.dbFileURL)

    def _read_file(self) -> None:
        try:
            self._data = pd.read_csv(self.dbFileURL)

        except:
            print("database.py: Error reading the db file: " + self.dbFileURL)
