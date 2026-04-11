"""Legacy logger adapter."""

from __future__ import annotations

import sys

from ghostpath.core.logging import logger as core_logger


def enable_debug() -> None:
    core_logger.set_level("DEBUG")


def debug(message: str) -> None:
    core_logger.debug(message)
    if core_logger.level == "DEBUG":
        print(f"[DEBUG] {message}", file=sys.stderr)


def info(message: str) -> None:
    core_logger.info(message)
    print(f"[INFO] {message}")


def warn(message: str) -> None:
    core_logger.warn(message)
    print(f"[WARN] {message}")


def error(message: str) -> None:
    core_logger.error(message)
    print(f"[ERROR] {message}")


def success(message: str) -> None:
    core_logger.success(message)
    print(f"[SUCCESS] {message}")
