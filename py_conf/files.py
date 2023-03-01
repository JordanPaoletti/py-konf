"""
Utility functions for dealing with file input/output
"""

import json
import logging
from os import PathLike

_log = logging.getLogger(__name__)


def fetch_json(file_path: str | PathLike[str]) -> dict:
    _log.info('Loading json file: %s', file_path)
    with open(file_path) as fp:
        return json.load(fp)
