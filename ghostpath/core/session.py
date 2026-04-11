"""Session persistence utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SessionManager:
    """Save and load run sessions."""

    def __init__(self, output_root: Path) -> None:
        self.output_root = output_root
        self.raw_dir = output_root / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def build_payload(
        self,
        target: str,
        results: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return {
            "target": target,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "modules": [result.get("module", "unknown") for result in results],
            "results": results,
        }

    def save(self, payload: dict[str, Any]) -> Path:
        target = payload["target"].replace("/", "_")
        timestamp = payload["timestamp"]
        path = self.raw_dir / f"session_{target}_{timestamp}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        latest = self.raw_dir / f"session_{target}_latest.json"
        with latest.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return path

    def load_latest(self, target: str) -> dict[str, Any]:
        path = self.raw_dir / f"session_{target.replace('/', '_')}_latest.json"
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
