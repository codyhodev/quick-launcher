from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QMenu

from quick_launcher.config import LauncherEntry


def _run_command(entry: LauncherEntry, terminal_cmd: str) -> None:
    if entry.command is None:
        return
    if entry.terminal:
        parts = [terminal_cmd, "--"] + entry.command.split()
    else:
        parts = entry.command.split()
    QProcess.startDetached(parts[0], parts[1:])


def _build_submenu(parent: QMenu, entry: LauncherEntry, terminal_cmd: str) -> None:
    if entry.type == "separator":
        parent.addSeparator()
        return

    if entry.items:
        submenu = parent.addMenu(entry.name)
        for child in entry.items:
            _build_submenu(submenu, child, terminal_cmd)
        return

    action = parent.addAction(entry.name)
    action.triggered.connect(lambda checked, e=entry: _run_command(e, terminal_cmd))


def build_menu(launchers: list[LauncherEntry], terminal_cmd: str = "gnome-terminal") -> QMenu:
    menu = QMenu()

    for entry in launchers:
        if entry.type == "separator":
            menu.addSeparator()
        elif entry.items:
            submenu = menu.addMenu(entry.name)
            for child in entry.items:
                _build_submenu(submenu, child, terminal_cmd)
        else:
            action = menu.addAction(entry.name)
            action.triggered.connect(lambda checked, e=entry: _run_command(e, terminal_cmd))

    return menu
