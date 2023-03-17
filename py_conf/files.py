
import json
from os import PathLike



def fetch_json(file_path: str | PathLike[str]) -> dict:
    with open(file_path) as fp:
        return json.load(fp)
