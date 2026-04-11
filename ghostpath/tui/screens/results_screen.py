"""Results screen."""

from textual.screen import Screen

from ghostpath.tui.widgets.results_table import ResultsTable


class ResultsScreen(Screen):
    """Results screen."""

    def compose(self):
        yield ResultsTable(id="results-view")
