from PyQt5.QtWidgets import QMenu

from quick_launcher.config import LauncherEntry
from quick_launcher.runner import run_command


def _build_submenu(parent: QMenu, entry: LauncherEntry) -> None:
    if entry.type == "separator":
        parent.addSeparator()
        return

    if entry.items:
        submenu = parent.addMenu(entry.name)
        for child in entry.items:
            _build_submenu(submenu, child)
        return

    action = parent.addAction(entry.name)
    action.triggered.connect(lambda checked, e=entry: run_command(e))


def build_menu(launchers: list[LauncherEntry], terminal_cmd: str = "gnome-terminal") -> QMenu:
    menu = QMenu()

    for entry in launchers:
        if entry.type == "separator":
            menu.addSeparator()
        elif entry.items:
            submenu = menu.addMenu(entry.name)
            for child in entry.items:
                _build_submenu(submenu, child)
        else:
            action = menu.addAction(entry.name)
            action.triggered.connect(lambda checked, e=entry: run_command(e, terminal_cmd))

    return menu
