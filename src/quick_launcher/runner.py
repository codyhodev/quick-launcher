from PyQt5.QtCore import QProcess

from quick_launcher.config import LauncherEntry


def run_command(entry: LauncherEntry) -> None:
    parts = entry.command.split()
    program, args = parts[0], parts[1:]
    QProcess.startDetached(program, args)
