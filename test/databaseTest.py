import pandas as pd
from pathlib import Path

dirpath = Path(__file__).cwd().as_posix()
data = pd.read_csv(dirpath + "/db_cube.csv")
print(data.values.tolist())
