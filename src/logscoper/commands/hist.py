from __future__ import annotations
from typing import Any, List, Dict
from ..models.log_entry import LOG_RE
from ..models.filters import try_filters
from ..models.exeptions import ValuesParseError
from .parser import parse_status


def cmd_hist(lines: List[str], args: Any) -> Dict[str, Any]:
    values: list[float] = []

    for line in lines:
        match = LOG_RE.match(line)
        if not match:
            continue

        get = match.groupdict()

        get['status'] = parse_status(get['status'])

        if not try_filters(get, args):
            continue

        rt_value = get['rt'] or get['rt_kv']
        if rt_value is not None:
            try:
                values.append(float(rt_value) * 1000)
            except ValuesParseError:
                raise SystemExit

    if args.strict and len(values) == 0:
        return {'error': 1}

    if not values:
        return {'error': 0, 'histogram': False}

    bucket_ms = args.bucket_ms
    if bucket_ms <= 0:
        return {'error': 2}

    num = int(max(values) // bucket_ms)
    buckets = [0] * (num + 1)

    for value in values:
        index = int(value // bucket_ms)
        if index >= (num + 1):
            index = num
        buckets[index] += 1

    hist_data = {}
    for i, bucket in enumerate(buckets):
        if bucket > 0:
            hist_data[f"{i * bucket_ms}-{(i + 1) * bucket_ms}"] = bucket

    return {'error': 0, 'histogram': hist_data}
