"""Structured logging with live subscribers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


LOG_LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40, "SUCCESS": 50}


@dataclass(slots=True)
class LogEvent:
    level: str
    message: str
    timestamp: str
    module: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
            "module": self.module,
        }


class GhostLogger:
    """Shared logger that can stream to CLI and TUI listeners."""

    def __init__(self) -> None:
        self.level = "INFO"
        self._listeners: list[Callable[[LogEvent], None]] = []

    def set_level(self, level: str) -> None:
        self.level = level.upper()

    def add_listener(self, listener: Callable[[LogEvent], None]) -> None:
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[LogEvent], None]) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def emit(self, level: str, message: str, module: str | None = None) -> None:
        if LOG_LEVELS[level] < LOG_LEVELS.get(self.level, 20):
            return
        event = LogEvent(
            level=level,
            message=message,
            module=module,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        )
        for listener in list(self._listeners):
            listener(event)

    def debug(self, message: str, module: str | None = None) -> None:
        self.emit("DEBUG", message, module)

    def info(self, message: str, module: str | None = None) -> None:
        self.emit("INFO", message, module)

    def warn(self, message: str, module: str | None = None) -> None:
        self.emit("WARN", message, module)

    def error(self, message: str, module: str | None = None) -> None:
        self.emit("ERROR", message, module)

    def success(self, message: str, module: str | None = None) -> None:
        self.emit("SUCCESS", message, module)


logger = GhostLogger()
