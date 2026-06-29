from PyQt5.QtWidgets import QMenu

from quick_launcher.config import LauncherEntry
from quick_launcher.runner import run_command


def build_menu(launchers: list[LauncherEntry]) -> QMenu:
    menu = QMenu()

    for entry in launchers:
        action = menu.addAction(entry.name)
        action.triggered.connect(lambda checked, e=entry: run_command(e))

    return menu
