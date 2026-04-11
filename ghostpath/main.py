#!/usr/bin/env python3
"""GhostPath v3 entrypoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghostpath.banner import BANNER
from ghostpath.core.config import ensure_default_config, load_config
from ghostpath.core.engine import ReconEngine
from ghostpath.core.exporter import export_payload
from ghostpath.version import __version__

try:
    from rich.console import Console
    from rich.table import Table
except ModuleNotFoundError:  # pragma: no cover - compatibility fallback
    Console = None
    Table = None


console = Console() if Console else None


def _root_parser(engine: ReconEngine) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ghostpath", description="GhostPath v3.0 Modular Recon Intelligence Framework")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    subparsers = parser.add_subparsers(dest="command")

    module_commands = {}
    for module_name, module in sorted(engine.discover_modules().items()):
        subparsers.add_parser(
            module_name,
            help=(module.__doc__ or module_name).splitlines()[0],
            parents=[module.arg_parser()],
            add_help=False,
        )
        module_commands[module_name] = module

    export_parser = subparsers.add_parser("export", help="Export results JSON/session into another format")
    export_parser.add_argument("input_path", help="Path to input JSON file")
    export_parser.add_argument("--format", choices=["json", "csv", "html"], default="html")
    export_parser.add_argument("--output", help="Destination output file")

    session_parser = subparsers.add_parser("session", help="Session management")
    session_subparsers = session_parser.add_subparsers(dest="session_command")
    save_parser = session_subparsers.add_parser("save", help="Save latest session for a target")
    save_parser.add_argument("target", help="Target name")
    load_parser = session_subparsers.add_parser("load", help="Load latest session for a target")
    load_parser.add_argument("target", help="Target name")

    parser.set_defaults(_modules=module_commands)
    return parser


def _print_results(payload: dict) -> None:
    if not console or not Table:
        print(f"\n[{payload['module']}]")
        for result in payload.get("results", []):
            print(result)
        return
    table = Table(title=f"{payload['module']} Results")
    table.add_column("Result")
    for result in payload.get("results", []):
        table.add_row(str(result))
    console.print(table)


def _handle_export(args) -> None:
    input_path = Path(args.input_path)
    with input_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    output = Path(args.output) if args.output else input_path.with_suffix(f".{args.format}")
    export_payload(payload, output, args.format)
    if console:
        console.print(f"Exported to {output}")
    else:
        print(f"Exported to {output}")


def _handle_session(args, engine: ReconEngine) -> None:
    try:
        if args.session_command == "load":
            payload = engine.session_manager.load_latest(args.target)
            if console:
                console.print_json(json.dumps(payload))
            else:
                print(json.dumps(payload, indent=2))
            return
        if args.session_command == "save":
            latest = engine.session_manager.load_latest(args.target)
            path = engine.session_manager.save(latest)
            if console:
                console.print(f"Saved session to {path}")
            else:
                print(f"Saved session to {path}")
            return
    except FileNotFoundError:
        print(f"No saved session found for {args.target}")
        return
    raise ValueError("Invalid session command")


def main() -> None:
    config = load_config()
    ensure_default_config()
    engine = ReconEngine(config)
    parser = _root_parser(engine)
    args = parser.parse_args()

    if args.version:
        if console:
            console.print(f"GhostPath {__version__}")
        else:
            print(f"GhostPath {__version__}")
        return

    if not args.command:
        if console:
            console.print(f"[cyan]{BANNER}[/cyan]")
        else:
            print(BANNER)
        try:
            from ghostpath.tui.app import run_tui
        except ModuleNotFoundError as exc:
            missing = exc.name or "required dependency"
            print(f"TUI dependencies are missing ({missing}). Install requirements.txt to launch the dashboard.")
            return
        run_tui(config)
        return

    if args.command == "export":
        _handle_export(args)
        return

    if args.command == "session":
        _handle_session(args, engine)
        return

    module = args._modules[args.command]
    result = module.cli(args)
    _print_results(result)


if __name__ == "__main__":
    main()
