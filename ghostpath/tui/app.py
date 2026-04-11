"""Textual application for GhostPath."""

from __future__ import annotations

import asyncio
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Input, Static, TabbedContent, TabPane

from ghostpath.banner import BANNER
from ghostpath.core.config import GhostPathConfig
from ghostpath.core.engine import ReconEngine
from ghostpath.core.logging import LogEvent, logger
from ghostpath.tui.widgets.footer import GhostFooter
from ghostpath.tui.widgets.header import GhostHeader
from ghostpath.tui.widgets.log_panel import LogPanel
from ghostpath.tui.widgets.results_table import ResultsTable
from ghostpath.tui.widgets.sidebar import Sidebar
from ghostpath.tui.widgets.stats_panel import StatsPanel


class GhostPathApp(App):
    """Interactive dashboard."""

    CSS_PATH = str(Path(__file__).resolve().parent / "themes" / "ghostpath.css")
    BINDINGS = [
        Binding("tab", "focus_next", "Switch Panel"),
        Binding("enter", "run_selected", "Run Module"),
        Binding("s", "save_results", "Save Results"),
        Binding("e", "export_results", "Export"),
        Binding("r", "rerun_module", "Rerun"),
        Binding("q", "quit", "Quit"),
        Binding("/", "focus_target", "Search/Target"),
    ]

    def __init__(self, config: GhostPathConfig | None = None) -> None:
        super().__init__()
        self.config = config or GhostPathConfig()
        self.engine = ReconEngine(self.config)
        self.selected_target = ""
        self.last_results: list[dict] = []

    def compose(self) -> ComposeResult:
        yield GhostHeader(show_clock=True)
        with Container(id="layout"):
            yield Sidebar(id="sidebar")
            with Container(id="main-panel"):
                yield Static(BANNER, id="banner")
                yield Input(placeholder="Enter target domain or URL", id="target-input")
                with TabbedContent(id="tabs"):
                    with TabPane("Results"):
                        yield ResultsTable(id="results-table")
                    with TabPane("Status"):
                        yield Static("Idle", id="status-copy")
                yield StatsPanel(id="stats")
            yield LogPanel(id="log-panel")
        yield GhostFooter()

    def on_mount(self) -> None:
        sidebar = self.query_one("#sidebar", Sidebar)
        sidebar.set_modules(sorted(self.engine.discover_modules().keys()))
        logger.add_listener(self._handle_log)
        self.query_one("#stats", StatsPanel).update_stats("", len(self.engine.discover_modules()), 0)

    def on_unmount(self) -> None:
        logger.remove_listener(self._handle_log)

    def _handle_log(self, event: LogEvent) -> None:
        self.call_from_thread(self.query_one("#log-panel", LogPanel).push, event.level, f"{event.module or 'core'}: {event.message}")

    @on(Sidebar.Selected)
    def _on_sidebar_selected(self, event) -> None:
        self.query_one("#status-copy", Static).update(f"Selected module: {event.item.children[0].renderable}")

    async def action_run_selected(self) -> None:
        sidebar = self.query_one("#sidebar", Sidebar)
        if sidebar.index is None:
            return
        selected_item = sidebar.children[sidebar.index]
        module_name = str(selected_item.children[0].renderable)
        target_input = self.query_one("#target-input", Input)
        target = target_input.value.strip()
        if not target:
            self.notify("Target is required", severity="warning")
            return
        self.selected_target = target
        self.query_one("#status-copy", Static).update(f"Running {module_name}...")
        result = await self.engine.run_module(module_name, target)
        self.last_results = [result]
        self.query_one("#results-table", ResultsTable).load_results(self.last_results)
        self.query_one("#status-copy", Static).update(f"Completed {module_name}")
        self.query_one("#stats", StatsPanel).update_stats(target, 1, len(result.get("results", [])))

    async def action_rerun_module(self) -> None:
        await self.action_run_selected()

    async def action_save_results(self) -> None:
        if not self.last_results or not self.selected_target:
            self.notify("No results to save", severity="warning")
            return
        path = self.engine.save_session(self.selected_target, self.last_results, {"source": "tui"})
        self.notify(f"Saved session to {path}")

    async def action_export_results(self) -> None:
        await self.action_save_results()

    def action_focus_target(self) -> None:
        self.query_one("#target-input", Input).focus()


def run_tui(config: GhostPathConfig | None = None) -> None:
    app = GhostPathApp(config=config)
    app.run()
