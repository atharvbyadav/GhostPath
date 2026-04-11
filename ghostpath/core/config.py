"""Configuration loading for GhostPath."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG_PATH = Path.home() / ".ghostpath" / "config.yaml"
FALLBACK_CONFIG_PATH = Path.cwd() / ".ghostpath" / "config.yaml"


@dataclass(slots=True)
class GhostPathConfig:
    """Runtime configuration."""

    threads: int = 20
    timeout: int = 10
    user_agent: str = "GhostPath/3.0"
    output_dir: Path = field(default_factory=lambda: Path.cwd() / "outputs")
    concurrency_limit: int = 20
    debug: bool = False
    log_level: str = "INFO"

    def to_dict(self) -> dict[str, Any]:
        return {
            "threads": self.threads,
            "timeout": self.timeout,
            "user_agent": self.user_agent,
            "output_dir": str(self.output_dir),
            "concurrency_limit": self.concurrency_limit,
            "debug": self.debug,
            "log_level": self.log_level,
        }


def _coerce_config(data: dict[str, Any]) -> GhostPathConfig:
    config = GhostPathConfig()
    for key, value in data.items():
        if hasattr(config, key):
            setattr(config, key, value)
    config.output_dir = Path(config.output_dir)
    return config


def load_config(path: Path | None = None) -> GhostPathConfig:
    """Load config from the user's home directory or use defaults."""

    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        config_path = ensure_default_config(config_path)
        if not config_path.exists():
            return GhostPathConfig()
        return _coerce_config(_load_yaml(config_path))

    return _coerce_config(_load_yaml(config_path))


def ensure_default_config(path: Path | None = None) -> Path:
    """Create a default config file if needed."""

    config_path = path or DEFAULT_CONFIG_PATH
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        config_path = FALLBACK_CONFIG_PATH
        config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        with config_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(GhostPathConfig().to_dict(), handle, sort_keys=False)
    return config_path


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
