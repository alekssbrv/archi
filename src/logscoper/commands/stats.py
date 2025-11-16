from __future__ import annotations
from collections import defaultdict
from typing import Any, Dict, List
from ..models.log_entry import LOG_RE
from ..models.filters import try_filters
from .parser import parse_status
from ..models.exeptions import RTParseError


def cmd_stats(lines: List[str], args: Any) -> Dict[str, Any]:
    cnt = 0
    status_counter: dict[int | Any, int] = defaultdict(int)
    times: list[float] = []
    path_counter: dict[str, int] = defaultdict(int)
    path_order: dict[str, int] = {}

    for i, line in enumerate(lines):
        match = LOG_RE.match(line)
        if not match:
            continue

        get = match.groupdict()

        get['status'] = parse_status(get['status'])

        if not try_filters(get, args):
            continue

        cnt += 1
        status_counter[get['status']] += 1
        path_counter[get['path']] += 1

        if get['path'] not in path_order:
            path_order[get['path']] = i

        rt_value = get['rt'] or get['rt_kv']
        if rt_value is not None:
            try:
                times.append(float(rt_value))
            except RTParseError:
                raise SystemExit

    top_paths = sorted(path_counter.items(), key=lambda x: (-x[1], path_order[x[0]]))[:args.top]

    return {
        'total': cnt,
        'status': dict(status_counter),
        'top_paths': top_paths,
        'paths': path_counter,
        'times': times,
    }
