"""Small JSON-backed cache."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CacheStore:
    """Simple file cache for low-risk reusable data."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Any | None:
        path = self.cache_dir / f"{key}.json"
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def set(self, key: str, value: Any) -> Path:
        path = self.cache_dir / f"{key}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2)
        return path
