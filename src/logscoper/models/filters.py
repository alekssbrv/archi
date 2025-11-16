from __future__ import annotations
from typing import Any
import re
from .log_entry import parse_timestamp, parse_iso


def try_filters(get: dict[str, str | Any], args: Any) -> bool:
    # Checking the status
    if args.status:
        status = get['status']
        stats_pars = args.status.strip()

        if ',' in stats_pars:
            status_check = [s.strip() for s in args.status.split(',')]
            matched = False
            for check in status_check:
                if check.endswith('xx'):
                    if int(status) // 100 == int(check[0]):
                        matched = True
                        break
                else:
                    try:
                        if int(status) == int(check):
                            matched = True
                            break
                    except Exception:
                        raise SystemExit
            if not matched:
                return False
        elif str(stats_pars).endswith('xx'):
            if int(status) // 100 != int(stats_pars[0]):
                return False
        else:
            try:
                if int(status) != int(stats_pars):
                    return False
            except Exception:
                raise SystemExit

    # Time-check
    if args.since or args.until:
        try:
            log_ts = parse_timestamp(get['ts'])

            if args.since:
                since_ts = parse_iso(args.since)
                if log_ts < since_ts:
                    return False

            if args.until:
                until_ts = parse_iso(args.until)
                if log_ts >= until_ts:
                    return False
        except Exception:
            raise SystemExit

    # Grep
    if args.grep:
        try:
            if not re.search(args.grep, get['path']):
                return False
        except re.error:
            raise re.error("Invalid regular pattern")

    return True
