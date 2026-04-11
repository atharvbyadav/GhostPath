"""Stats widget."""

from textual.widgets import Static


class StatsPanel(Static):
    """Simple stats display."""

    def update_stats(self, target: str, modules: int, findings: int) -> None:
        self.update(f"Target: {target or '-'}\nModules: {modules}\nFindings: {findings}")
