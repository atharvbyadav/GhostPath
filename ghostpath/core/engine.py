"""Async orchestration engine."""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ghostpath.core.config import GhostPathConfig
from ghostpath.core.logging import logger
from ghostpath.core.plugin_loader import load_plugins
from ghostpath.core.session import SessionManager


ProgressCallback = Callable[[str, str], None]


class ReconEngine:
    """Central module execution engine."""

    def __init__(self, config: GhostPathConfig) -> None:
        self.config = config
        self.plugins = load_plugins()
        self.session_manager = SessionManager(Path(config.output_dir))

    def discover_modules(self) -> dict[str, Any]:
        return self.plugins

    async def run_module(
        self,
        module_name: str,
        target: str,
        overrides: dict[str, Any] | None = None,
        progress: ProgressCallback | None = None,
    ) -> dict[str, Any]:
        if module_name not in self.plugins:
            raise KeyError(f"Unknown module: {module_name}")

        module = self.plugins[module_name]
        config = self.config.to_dict()
        if overrides:
            config.update(overrides)

        if progress:
            progress(module_name, "running")
        logger.info(f"Running module against {target}", module_name)

        if inspect.iscoroutinefunction(module.run):
            result = await module.run(target, config)
        else:
            result = await asyncio.to_thread(module.run, target, config)

        if progress:
            progress(module_name, "complete")
        logger.success("Module completed", module_name)
        return result

    async def run_modules(
        self,
        module_names: list[str],
        target: str,
        overrides: dict[str, Any] | None = None,
        progress: ProgressCallback | None = None,
    ) -> list[dict[str, Any]]:
        tasks = [
            self.run_module(module_name, target, overrides=overrides, progress=progress)
            for module_name in module_names
        ]
        return await asyncio.gather(*tasks)

    def save_session(
        self,
        target: str,
        results: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        payload = self.session_manager.build_payload(target, results, metadata)
        return self.session_manager.save(payload)
