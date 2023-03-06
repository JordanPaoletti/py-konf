from typing import Any, Optional


def or_else(val: Optional[Any], default: Any) -> Any:
    return val if val is not None else default
