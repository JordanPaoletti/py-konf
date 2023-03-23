from functools import reduce
from typing import Any

from py_konf.cli import prompt_val
from py_konf.sources.base import Source
from py_konf.value import ConfigDetails, ConfigValue


def pretty_name(name: str) -> str:
    return reduce(lambda x, y: x + y, [s.capitalize() for s in name.split("_")])


class PromptSource(Source):
    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        return self.fetch_source_with_existing_vals(cvals, {})

    def fetch_source_with_existing_vals(self,
                                        cvals: dict[str, ConfigValue],
                                        curr: dict[str, Any]
                                        ) -> dict:
        to_prompt = {k: v for k, v in cvals.items() if v.prompt}
        if len(to_prompt) == 0:
            return {}

        print('Specify run parameters')
        vals = {}
        for key, cval in to_prompt.items():
            default = curr[key] if key in curr else cval.default
            v = prompt_val(pretty_name(key), default)
            vals[key] = cval.from_str(v) if type(v) is str else v
        return vals
