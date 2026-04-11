"""Result export helpers."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any


def flatten_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for module_result in payload.get("results", []):
        module_name = module_result.get("module", "unknown")
        metadata = module_result.get("metadata", {})
        for item in module_result.get("results", []):
            row = {"module": module_name, "value": item}
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    row[key] = value
            rows.append(row)
    return rows


def export_json(payload: dict[str, Any], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return destination


def export_csv(payload: dict[str, Any], destination: Path) -> Path:
    rows = flatten_results(payload)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()} or {"module", "value"})
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return destination


def export_html(payload: dict[str, Any], destination: Path) -> Path:
    rows = flatten_results(payload)
    destination.parent.mkdir(parents=True, exist_ok=True)
    module_list = ", ".join(payload.get("modules", []))
    row_html = "\n".join(
        f"<tr><td>{escape(str(row.get('module', '')))}</td><td>{escape(str(row.get('value', '')))}</td></tr>"
        for row in rows
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GhostPath Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #0b1020; color: #d7f8f5; margin: 2rem; }}
    h1, h2 {{ color: #7ef9ff; }}
    .card {{ background: #131c35; border: 1px solid #2c3d68; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #2c3d68; padding: 0.6rem; text-align: left; }}
    th {{ background: #182447; }}
  </style>
</head>
<body>
  <h1>GhostPath Report</h1>
  <div class="card">
    <p><strong>Target:</strong> {escape(str(payload.get("target", "")))}</p>
    <p><strong>Timestamp:</strong> {escape(str(payload.get("timestamp", datetime.now(timezone.utc).isoformat())))}</p>
    <p><strong>Modules:</strong> {escape(module_list)}</p>
    <p><strong>Total Findings:</strong> {len(rows)}</p>
  </div>
  <div class="card">
    <h2>Results</h2>
    <table>
      <thead><tr><th>Module</th><th>Value</th></tr></thead>
      <tbody>{row_html}</tbody>
    </table>
  </div>
</body>
</html>
"""
    with destination.open("w", encoding="utf-8") as handle:
        handle.write(html)
    return destination


def export_payload(payload: dict[str, Any], destination: Path, fmt: str) -> Path:
    fmt = fmt.lower()
    if fmt == "json":
        return export_json(payload, destination)
    if fmt == "csv":
        return export_csv(payload, destination)
    if fmt == "html":
        return export_html(payload, destination)
    if fmt == "txt":
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8") as handle:
            for row in flatten_results(payload):
                handle.write(f"{row.get('module')}: {row.get('value')}\n")
        return destination
    raise ValueError(f"Unsupported export format: {fmt}")
