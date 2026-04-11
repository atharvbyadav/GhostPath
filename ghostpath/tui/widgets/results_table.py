"""Results table widget."""

from textual.widgets import DataTable


class ResultsTable(DataTable):
    """Sortable results table."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Module", "Result")

    def load_results(self, payloads: list[dict]) -> None:
        self.clear(columns=False)
        for payload in payloads:
            module = payload.get("module", "unknown")
            for value in payload.get("results", []):
                self.add_row(module, str(value))
