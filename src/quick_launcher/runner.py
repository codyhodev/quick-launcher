from PyQt5.QtCore import QProcess

from quick_launcher.config import LauncherEntry


def run_command(entry: LauncherEntry, terminal_cmd: str = "gnome-terminal") -> None:
    if entry.terminal:
        parts = [terminal_cmd, "--"] + entry.command.split()
    else:
        parts = entry.command.split()
    QProcess.startDetached(parts[0], parts[1:])
