"""Dashboard screen."""

from textual.screen import Screen
from textual.widgets import Static


class DashboardScreen(Screen):
    """Default landing screen."""

    def compose(self):
        yield Static("GhostPath v3.0\nModular Recon Intelligence Framework", id="dashboard-copy")
