from __future__ import annotations
from typing import Iterator, List, Any
from ..models.log_entry import LOG_RE, parse_timestamp
from ..models.filters import try_filters
from ..models.exeptions import TimeParseError
from .parser import parse_status


def cmd_filter(lines: List[str], args: Any) -> Iterator[str]:
    for line in lines:
        match = LOG_RE.match(line)
        if not match:
            continue

        get = match.groupdict()

        get['status'] = parse_status(get['status'])

        if not try_filters(get, args):
            continue

        try:
            log_ts = parse_timestamp(get['ts'])
            iso_ts = log_ts.isoformat()
        except TimeParseError:
            return

        rt_value = get['rt'] or get['rt_kv']
        rt_str = f" rt={rt_value}" if rt_value else ""
        bytes_str = get['bytes']

        normalized = f"{iso_ts} {get['ip']} {get['method']} {get['path']} {get['status']} {bytes_str}{rt_str}"
        yield normalized
