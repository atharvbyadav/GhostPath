"""Auto-discovery for GhostPath modules."""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterator
from types import ModuleType

import ghostpath.modules
from ghostpath.core.logging import logger


def iter_module_names() -> Iterator[str]:
    """Yield import paths for runnable module plugins."""

    prefix = f"{ghostpath.modules.__name__}."
    for module_info in pkgutil.walk_packages(ghostpath.modules.__path__, prefix):
        if module_info.ispkg:
            continue
        if ".shared." in module_info.name:
            continue
        yield module_info.name


def load_plugins() -> dict[str, ModuleType]:
    """Load all discovered plugins that expose a run function."""

    loaded: dict[str, ModuleType] = {}
    for import_name in iter_module_names():
        try:
            module = importlib.import_module(import_name)
        except ModuleNotFoundError as exc:
            logger.warn(f"Skipping plugin {import_name}: missing dependency {exc.name}")
            continue
        name = import_name.rsplit(".", maxsplit=1)[-1]
        if hasattr(module, "run"):
            loaded[name] = module
    return loaded
