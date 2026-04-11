"""Sidebar widget."""

from textual.widgets import ListItem, ListView, Static


class Sidebar(ListView):
    """Module selection list."""

    def set_modules(self, modules: list[str]) -> None:
        self.clear()
        for module in modules:
            self.append(ListItem(Static(module)))
