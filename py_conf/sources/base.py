from abc import ABC, abstractmethod

from py_conf.value import ConfigValue


class Source(ABC):
    @abstractmethod
    def fetch_source(self, vals: dict[str, ConfigValue]) -> dict:
        pass


class DefaultsSource(Source):
    def fetch_source(self, vals: dict[str, ConfigValue]) -> dict:
        return {k: v.default for k, v in vals.items()}


class OverrideSource(Source):
    def fetch_source(self, vals: dict[str, ConfigValue]) -> dict:
        return {k: v.override for k, v in vals.items() if v.override is not None}
