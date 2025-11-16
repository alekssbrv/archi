from __future__ import annotations
from typing import List, Dict, Any, Tuple
import statistics
from ..models.statistics import percentile


class LogFormatter:
    """Класс для форматирования статистики и гистограмм в требуемые форматы"""

    NO_DATA_ALLERT = "No data"
    NO_RT_VALUE = "n/a"

    # Класс для преобразования статистики в json-формат
    @classmethod
    def format_stats_for_json(cls, cnt: int, status_counter: Dict[int, int],
                              top_paths: List[Tuple[str, int]], times: List[float]) -> Dict[
        str, str | float | None | Any]:
        statistic = {
            'total': cnt,
            'status': {str(k): v for k, v in sorted(status_counter.items())},
            'top_paths': [[path, count] for path, count in top_paths],
        }

        if times:
            statistic['rt_avg_ms'] = round(sum(times) / len(times) * 1000, 2)
            statistic['rt_p95_ms'] = round(percentile(times, 95) * 1000, 2)
            statistic['rt_p99_ms'] = round(percentile(times, 99) * 1000, 2)
        else:
            statistic['rt_avg_ms'] = None
            statistic['rt_p95_ms'] = None
            statistic['rt_p99_ms'] = None

        return statistic

    # Класс для преобразования статистики в текстовый формат
    @classmethod
    def format_stats_for_text(cls, cnt: int, status_counter: Dict[int, int],
                              top_paths: List[Tuple[str, int]], times: List[float]) -> List[str]:
        lines = [f'Total: {cnt}', 'By status:']
        for status in sorted(status_counter.keys()):
            lines.append(f'  {status}: {status_counter[status]}')

        if times:
            lines.append(f'Avg RT (ms): {round(statistics.mean(times) * 1000, 2):.2f}')
            lines.append(f'P95 RT (ms): {round(percentile(times, 95) * 1000, 2):.2f}')
            lines.append(f'P99 RT (ms): {round(percentile(times, 99) * 1000, 2):.2f}')
        else:
            lines.append(f'Avg RT (ms): {cls.NO_RT_VALUE}')
            lines.append(f'P95 RT (ms): {cls.NO_RT_VALUE}')
            lines.append(f'P99 RT (ms): {cls.NO_RT_VALUE}')

        lines.append('Top paths:')
        for path, count in top_paths:
            lines.append(f'  {path}: {count}')

        return lines

    # Класс для преобразования гистограмм в json-формат
    @classmethod
    def format_hist_for_json(cls, histogram: Dict[str, int]) -> Dict[str, int]:
        return histogram

    # Класс для преобразования гистограмм в текстовый формат
    @classmethod
    def format_hist_for_text(cls, histogram: Dict[str, int]) -> List[str]:
        if not histogram:
            return [cls.NO_DATA_ALLERT]

        lines = []
        for bucket, count in sorted(histogram.items()):
            lines.append(f"{bucket} : {'#' * count} {count}")

        return lines

    # Класс для преобразования пустых гистограмм в json-формат
    @classmethod
    def format_empty_hist_for_json(cls) -> Dict[str, Any]:
        return {"buckets": []}

    # Класс для преобразования пустых гистограмм в текстовый формат
    @classmethod
    def format_empty_hist_for_text(cls) -> List[str]:
        return [cls.NO_DATA_ALLERT]
