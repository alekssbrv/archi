from __future__ import annotations


class LogScoperError(Exception):
    pass


class FileReadError(LogScoperError):
    pass


class FileWriteError(LogScoperError):
    pass


class StatusParseError(LogScoperError):
    pass


class TimeParseError(LogScoperError):
    pass


class FileError(LogScoperError):
    pass


class ValuesParseError(LogScoperError):
    pass


class RTParseError(LogScoperError):
    pass
