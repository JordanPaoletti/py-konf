from typing import Any, Optional


def prompt_val(name: str, default: Optional[Any] = None) -> str | Any:
    val = ''

    if default is None:
        prompt = f'{name}: '
        while not val:
            val = input(prompt)
    else:
        val = input(f'{name} [{default}]: ').strip()
        val = val if val else default

    return val
