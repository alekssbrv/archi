from __future__ import annotations
import argparse
import json
import sys
from typing import Optional, List
from ..commands.filter import cmd_filter as filter
from ..commands.stats import cmd_stats as stats
from ..commands.hist import cmd_hist as hist
from ..adapters.formatters import LogFormatter
from ..models.exeptions import FileReadError, FileWriteError


def log_processor(path: str) -> List[str] | None:
    try:
        with open(path, 'r', encoding='utf8') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        # raise FileNotFoundError(f"File not found: {path}")
        return None
    except FileReadError:
        # raise FileReadError(f"Error reading file")
        return None


def cmd_stats(args: argparse.Namespace) -> int:
    lines = log_processor(args.path)
    if not lines:
        return 2

    result = stats(lines, args)

    if 'error' in result and result['error'] != 0:
        return result['error']

    if args.json:
        json_data = LogFormatter.format_stats_for_json(
            result['total'],
            result['status'],
            result['top_paths'],
            result['times']
        )
        json.dump(json_data, sys.stdout)
        print()
    else:
        text_lines = LogFormatter.format_stats_for_text(
            result['total'],
            result['status'],
            result['top_paths'],
            result['times']
        )
        for output_line in text_lines:
            print(output_line)

    return 0


def cmd_filter(args: argparse.Namespace) -> int:
    lines = log_processor(args.path)
    if not lines:
        return 2

    out = sys.stdout
    if args.out:
        try:
            out = open(args.out, 'w', encoding='utf8')
        except FileWriteError:
            # raise FileWriteError(f"Error writing file {args.path}")
            return 2

    try:
        for output_line in filter(lines, args):
            print(output_line, file=out)
    except FileWriteError:
        # raise FileWriteError(f"Error writing file {args.path}")
        return 2
    finally:
        if args.out and out != sys.stdout:
            out.close()

    return 0


def cmd_hist(args: argparse.Namespace) -> int:
    lines = log_processor(args.path)
    if not lines:
        return 2

    result = hist(lines, args)

    if 'error' in result and result['error'] != 0:
        return result['error']

    if result.get('empty'):
        if args.json:
            json_data = LogFormatter.format_empty_hist_for_json()
            json.dump(json_data, sys.stdout)
            print()
        else:
            text_lines = LogFormatter.format_empty_hist_for_text()
            for line in text_lines:
                print(line)
        return 0

    if args.json:
        json_data = LogFormatter.format_hist_for_json(result['histogram'])
        json.dump(json_data, sys.stdout)
        print()
    else:
        text_lines = LogFormatter.format_hist_for_text(result['histogram'])
        for line in text_lines:
            print(line)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logscoper",
        description="Simple access log analyzer",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # stats
    ps = sub.add_parser("stats", help="Show aggregated stats")
    ps.add_argument("--path", required=True)
    ps.add_argument("--top", type=int, default=10)
    ps.add_argument("--since")
    ps.add_argument("--until")
    ps.add_argument("--status")
    ps.add_argument("--grep")
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(func=cmd_stats)

    # filter
    pf = sub.add_parser("filter", help="Filter and print normalized lines")
    pf.add_argument("--path", required=True)
    pf.add_argument("--since")
    pf.add_argument("--until")
    pf.add_argument("--status")
    pf.add_argument("--grep")
    pf.add_argument("--out")
    pf.set_defaults(func=cmd_filter)

    # hist
    ph = sub.add_parser("hist", help="Request time histogram")
    ph.add_argument("--path", required=True)
    ph.add_argument("--bucket-ms", type=int, default=100, dest="bucket_ms")
    ph.add_argument("--since")
    ph.add_argument("--until")
    ph.add_argument("--status")
    ph.add_argument("--grep")
    ph.add_argument("--json", action="store_true")
    ph.add_argument("--strict", action="store_true")
    ph.set_defaults(func=cmd_hist)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
