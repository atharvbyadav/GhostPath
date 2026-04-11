"""Live log display."""

from textual.widgets import RichLog


class LogPanel(RichLog):
    """Streaming logs."""

    def push(self, level: str, message: str) -> None:
        colors = {
            "DEBUG": "cyan",
            "INFO": "white",
            "WARN": "yellow",
            "ERROR": "red",
            "SUCCESS": "green",
        }
        self.write(f"[{colors.get(level, 'white')}][{level}][/]: {message}")
