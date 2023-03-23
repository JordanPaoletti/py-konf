import os

from py_konf.sources.base import Source
from py_konf.value import ConfigValue, ConfigDetails


class EnvVarSource(Source):
    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        vals = {}
        for key, cval in cvals.items():
            use_env_vars = False
            env_var = None

            if type(cval.env_var) is str:
                env_var = cval.env_var
                use_env_vars = True
            elif cval.env_var:
                use_env_vars = True
                env_var = key.upper()
                if details.name is not None:
                    env_var = f'{details.name.upper()}_{env_var}'

            if not use_env_vars:
                continue

            v = os.environ.get(env_var)
            if v is not None:
                vals[key] = cval.from_str(v)
        return vals
