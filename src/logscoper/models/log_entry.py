from __future__ import annotations
import re
from datetime import datetime, timezone

LOG_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<ts>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>.*?)(?:\s+HTTP/\d\.\d)?"\s+'
    r'(?P<status>\d{3})\s+(?P<bytes>\S+)'
    r'(?:\s+"[^"]*"\s+"[^"]*")?'
    r'(?:\s+(?P<rt>\d+\.\d+)|\s+rt=(?P<rt_kv>\d+\.\d+))?'
)

RT_KV_RE = re.compile(r'(?:^|\s)rt=(?P<rt>\d+\.\d+)\b')


def parse_timestamp(timestamp: str) -> datetime:
    ts_clean = timestamp.split()[0]
    dt = datetime.strptime(ts_clean, '%d/%b/%Y:%H:%M:%S')
    return dt.replace(tzinfo=timezone.utc)


def parse_iso(iso: str) -> datetime:
    if '+' in iso:
        return datetime.fromisoformat(iso)
    else:
        return datetime.fromisoformat(iso + '+00:00')
