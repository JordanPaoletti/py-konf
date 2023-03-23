from argparse import ArgumentParser
from typing import List, Optional

from py_konf.sources.base import Source
from py_konf.value import ConfigValue, ConfigDetails


class CliSource(Source):
    args: Optional[List[str]]

    def __init__(self, args: Optional[List[str]] = None):
        self.args = args

    def fetch_source(self, details: ConfigDetails, cvals: dict[str, ConfigValue]) -> dict:
        cli_vals = {k: v for k, v in cvals.items() if v.cli_arg is not None}
        parser = ArgumentParser()
        for cval in cli_vals.values():
            kwargs = {'action': 'store_const', 'const': 'true'} if cval.vtype is bool else {'action': 'store'}
            if type(cval.cli_arg) is str:
                parser.add_argument(cval.cli_arg, **kwargs)
            else:
                short, long = cval.cli_arg
                parser.add_argument(short, long, **kwargs)

        args_parsed = vars(
            parser.parse_known_args(args=self.args)[0] if self.args is not None else parser.parse_known_args()[0])
        print(args_parsed)

        vals = {}
        for key, cval in cli_vals.items():
            cli_arg = cval.cli_arg if type(cval.cli_arg) is str else cval.cli_arg[1]
            cli_arg = cli_arg.strip('-')
            v = args_parsed[cli_arg]
            if v is not None:
                vals[key] = cval.from_str(v)

        return vals
