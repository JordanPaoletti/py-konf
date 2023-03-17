import json
import os
from abc import ABC
from os import PathLike
from typing import Optional

from py_conf.sources.base import Source
from py_conf.value import ConfigValue, ConfigDetails


class FileSource(Source, ABC):
    file_name: str
    path: str | PathLike[str]

    def __init__(self,
                 file_name: str,
                 path: str | PathLike[str] = '~',
                 env_var: Optional[str] = None
                 ):
        self.file_name = file_name

        env = os.environ.get(env_var) if env_var is not None else None
        self.path = env if env is not None else path


class JsonSource(FileSource):

    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        keys = cvals.keys()
        with open(f'{self.path}/{self.file_name}') as fp:
            vals = json.load(fp)
            return {k: v for k, v in vals.items() if k in keys}
