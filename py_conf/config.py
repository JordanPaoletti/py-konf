from dataclasses import dataclass
from typing import Any


@dataclass
class _Value:
    default: Any


def _handle_args(cls):
    for val in cls.__annotations__.keys():
        if hasattr(cls, val):
            v = getattr(cls, val)
            if type(v) is _Value:
                setattr(cls, val, v.default)
        else:
            setattr(cls, val, None)


class _MetaConfig(type):
    def __init__(cls, name, bases, dct):
        super().__init__(cls)

        # ignore Config class
        if _MetaConfig.__module__ != cls.__module__:
            _handle_args(cls)


class Config(metaclass=_MetaConfig):
    pass


def value(*, default: Any) -> _Value:
    return _Value(default=default)
