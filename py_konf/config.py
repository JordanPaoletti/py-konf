import logging
from typing import List

from py_konf.sources.base import Source, DefaultsSource, OverrideSource
from py_konf.sources.cli import CliSource
from py_konf.sources.envvars import EnvVarSource
from py_konf.sources.prompt import PromptSource
from py_konf.value import ConfigValue, value, ConfigDetails

_default_sources = [
    EnvVarSource(),
    CliSource()
]

_log = logging.getLogger(__name__)


def _clean_values(cls):
    cvals = {}

    for key, typ in cls.__annotations__.items():
        cval: ConfigValue
        if hasattr(cls, key):
            v = getattr(cls, key)
            if type(v) is ConfigValue:
                cval = v
            else:
                cval = value(default=v)
        else:
            cval = value(default=None)

        if cval.from_str is None:
            if typ is str:
                cval.from_str = str
            if typ is int:
                cval.from_str = int
            elif typ is float:
                cval.from_str = float
            elif typ is bool:
                cval.from_str = lambda v: None if v is None else v.lower() == 'true'

        cval.vtype = typ
        cvals[key] = cval
        setattr(cls, key, None)

    cls._cvals = cvals


class _MetaConfig(type):
    def __init__(cls, name, bases, dct):
        super().__init__(cls)

        # ignore Config class
        if _MetaConfig.__module__ != cls.__module__:
            cls._cvals = {}
            _clean_values(cls)


class Config(metaclass=_MetaConfig):
    _sources: List[Source]
    _cvals: dict[str, ConfigValue]
    _details: ConfigDetails

    def __init__(self, *,
                 name: str = None,
                 load_on_init: bool = False,
                 sources: List[Source] = None
                 ):
        self._sources = [DefaultsSource(),
                         *(sources if sources is not None else _default_sources),
                         OverrideSource()
                         ]
        self._details = ConfigDetails(name=name)

        if load_on_init:
            self.load()

    def load(self):
        vals = {}

        for src in self._sources:
            vals.update(src.fetch_source(self._details, self._cvals))
            _log.debug('%s: %s', src.__class__.__name__, vals)

        # have prompt default to the final state of other config sources
        vals.update(
            PromptSource().fetch_source_with_existing_vals(self._cvals, vals)
        )

        for k, v in vals.items():
            self.__setattr__(k, v)

        return self

    def to_dict(self) -> dict:
        return {k: self.__getattribute__(k) for k in self._cvals.keys()}
