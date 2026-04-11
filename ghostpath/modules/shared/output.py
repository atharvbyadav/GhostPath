"""Legacy output adapter."""

from __future__ import annotations

from pathlib import Path

from ghostpath.core.exporter import export_csv, export_html, export_json


def save_results(data, output_path: str, fmt: str = "txt") -> None:
    payload = {
        "target": "legacy",
        "timestamp": "legacy",
        "modules": ["legacy"],
        "results": [{"module": "legacy", "results": list(data), "metadata": {}}],
    }
    path = Path(output_path)
    if fmt == "json":
        export_json(payload, path)
        return
    if fmt == "csv":
        export_csv(payload, path)
        return
    if fmt == "html":
        export_html(payload, path)
        return
    with path.open("w", encoding="utf-8") as handle:
        for item in data:
            handle.write(f"{item}\n")
