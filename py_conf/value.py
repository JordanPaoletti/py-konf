from dataclasses import dataclass
from typing import Any, Type, Optional


@dataclass
class ConfigValue:
    default: Optional[Any]
    vtype: Optional[Type]
    override: Optional[Any]


def value(*, default: Any = None, override: Any = None) -> ConfigValue:
    return ConfigValue(default=default, vtype=None, override=override)
