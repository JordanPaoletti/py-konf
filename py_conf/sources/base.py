from abc import ABC, abstractmethod

from py_conf.value import ConfigValue, ConfigDetails


class Source(ABC):
    @abstractmethod
    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        pass


class DefaultsSource(Source):
    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        return {k: v.default for k, v in cvals.items()}


class OverrideSource(Source):
    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        return {k: v.override for k, v in cvals.items() if v.override is not None}
