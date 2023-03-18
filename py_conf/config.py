from typing import List

from py_conf.sources.base import Source, DefaultsSource, OverrideSource
from py_conf.sources.cli import CliSource
from py_conf.sources.envvars import EnvVarSource
from py_conf.sources.prompt import PromptSource
from py_conf.utils import or_else
from py_conf.value import ConfigValue, value, ConfigDetails

_default_sources = [
    EnvVarSource(),
    CliSource()
]


def _handle_args(cls):
    cls._values = cls.__annotations__

    for key in cls.__annotations__.keys():
        if hasattr(cls, key):
            v = getattr(cls, key)
            if type(v) is ConfigValue:
                setattr(cls, key, v.default)
        else:
            setattr(cls, key, None)


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
                         *or_else(sources, _default_sources),
                         OverrideSource()
                         ]
        self._details = ConfigDetails(name=name)

        if load_on_init:
            self.load()

    def load(self):
        vals = {}

        for src in self._sources:
            vals.update(src.fetch_source(self._details, self._cvals))

        # have prompt default to the final state of other config sources
        vals.update(
            PromptSource().fetch_source_with_existing_vals(self._cvals, vals)
        )

        for k, v in vals.items():
            self.__setattr__(k, v)

        return self
