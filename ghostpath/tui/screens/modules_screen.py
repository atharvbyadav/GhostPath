"""Modules screen."""

from textual.screen import Screen
from textual.widgets import Static


class ModulesScreen(Screen):
    """Module screen placeholder."""

    def compose(self):
        yield Static("Select a module from the sidebar and press Enter.", id="modules-copy")
