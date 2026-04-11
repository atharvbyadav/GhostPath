"""Shared helpers for runnable modules."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from ghostpath.core.config import GhostPathConfig
from ghostpath.core.exporter import export_payload
from ghostpath.core.logging import logger


def normalize_target(value: str | None, fallback: str | None = None) -> str:
    target = value or fallback
    if not target:
        raise ValueError("A target is required")
    return target.strip()


def default_result(module: str, results: list[Any], metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"module": module, "results": results, "metadata": metadata or {}}


def build_standard_parser(name: str, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=name, description=description)
    parser.add_argument("target", nargs="?", help="Target domain or URL")
    parser.add_argument("--target", dest="target_flag", help="Target domain or URL")
    parser.add_argument("--output", help="Output path to save structured results")
    parser.add_argument("--format", choices=["json", "csv", "html", "txt"], default="json", help="Output format")
    parser.add_argument("--threads", type=int, default=20, help="Concurrency level")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser


def cli_entry(module_name: str, run_callable: Any, args: argparse.Namespace) -> dict[str, Any]:
    target = normalize_target(args.target_flag, args.target)
    base_config = GhostPathConfig(
        threads=args.threads,
        timeout=args.timeout,
        debug=args.debug,
        log_level="DEBUG" if args.debug else "INFO",
    ).to_dict()
    config = {
        key: value
        for key, value in vars(args).items()
        if key not in {"command", "_modules", "target", "target_flag", "output", "format"}
        and value is not None
    }
    config = {**base_config, **config}
    if args.debug:
        logger.set_level("DEBUG")

    result = run_callable(target, config)
    if asyncio.iscoroutine(result):
        result = asyncio.run(result)

    if args.output:
        payload = {"target": target, "timestamp": "cli", "modules": [module_name], "results": [result]}
        export_payload(payload, Path(args.output), args.format)

    return result
