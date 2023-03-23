import json
import os
from abc import ABC
from configparser import ConfigParser
from os import PathLike
from typing import Optional

from py_konf.sources.base import Source
from py_konf.value import ConfigValue, ConfigDetails


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


class ConfigSource(FileSource):
    section_name: Optional[str]

    def __init__(self,
                 file_name: str,
                 section_name: Optional[str] = None,
                 path: str | PathLike[str] = '~',
                 env_var: Optional[str] = None
                 ):
        super().__init__(file_name, path, env_var)
        self.section_name = section_name

    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        with open(f'{self.path}/{self.file_name}') as fp:
            parser = ConfigParser()
            parser.read_file(fp)

            sect = None
            if self.section_name is not None:
                sect = parser[self.section_name]
            elif len(parser.sections()) == 1:
                sect = parser[parser.sections()[0]]

            return {key: cval.from_str(sect[key]) for key, cval in cvals.items()}
