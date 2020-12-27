import pandas as pd
from pathlib import Path


class RubiksDatabase:
    def __init__(self, databaseFileName):
        self._data = None
        dirpath = Path(__file__).cwd().as_posix()
        self.dbFileURL = dirpath + databaseFileName
        self._readFile()

    def addRecord(self, id, start_pattern, end_pattern, instructions, time, date):
        new_row = {'id': id,
                   'start_pattern': start_pattern,
                   'end_pattern': end_pattern,
                   'instructions': instructions,
                   'time': time,
                   "date": date
                   }
        self._data = self._data.append(new_row, ignore_index=True)
        self._saveFile()

    @property
    def records(self):
        records = []
        for record in self._data.values:
            recordMap = {
                "id": record[0],
                "start_pattern": record[1],
                "end_pattern": record[2],
                "instructions": record[3],
                "time": record[4],
                "date": record[5],
            }
            records.append(recordMap)
        return records
    
    def _saveFile(self):
        try:
            self._data.to_csv(self.dbFileURL, encoding='utf-8', index=False)
        except:
            print("database.py: Error writing to the db file: " + self.dbFileURL)


    def _readFile(self):
        try:
            self._data: pd.DataFrame = pd.read_csv(self.dbFileURL)

        except:
            print("database.py: Error reading the db file: " + self.dbFileURL)

