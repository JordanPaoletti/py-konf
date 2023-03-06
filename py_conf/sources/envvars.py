from py_conf.sources.base import Source
from py_conf.value import ConfigValue


class EnvVarSource(Source):
    def fetch_source(self, vals: dict[str, ConfigValue]) -> dict:
        return {}
