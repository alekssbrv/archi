from __future__ import annotations
from ..models.exeptions import ValuesParseError


def parse_status(status_value: str) -> int:
    try:
        return int(status_value)
    except ValuesParseError:
        # raise StatusParseError(f'Invalid status value: {status_value}')
        return 2
