from dataclasses import dataclass
from typing import Any, Type, Optional, Callable


@dataclass(kw_only=True)
class ConfigDetails:
    name: Optional[str] = None


@dataclass(kw_only=True)
class ConfigValue:
    default: Optional[Any]
    vtype: Optional[Type]
    override: Optional[Any]
    env_var: bool | str
    from_str: Optional[Callable[[str], Any]]


def value(*,
          default: Any = None,
          override: Any = None,
          env_var: bool | str = True,
          from_str: Optional[Callable[[str], Any]] = None
          ) -> ConfigValue:
    return ConfigValue(
        default=default,
        vtype=None,
        override=override,
        env_var=env_var,
        from_str=from_str
    )
