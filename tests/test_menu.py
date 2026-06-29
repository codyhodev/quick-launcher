import pytest
from PyQt5.QtWidgets import QApplication, QMenu

from quick_launcher.config import LauncherEntry
from quick_launcher.menu import build_menu


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_build_menu_flat_launchers(qapp):
    launchers = [
        LauncherEntry(name="Terminal", command="alacritty"),
        LauncherEntry(name="Browser", command="firefox"),
    ]

    menu = build_menu(launchers)
    actions = menu.actions()

    assert len(actions) == 2
    assert actions[0].text() == "Terminal"
    assert actions[1].text() == "Browser"


def test_build_menu_empty(qapp):
    menu = build_menu([])
    assert menu.actions() == []


def test_build_menu_single_launcher(qapp):
    launchers = [LauncherEntry(name="Only App", command="app")]

    menu = build_menu(launchers)
    actions = menu.actions()

    assert len(actions) == 1
    assert actions[0].text() == "Only App"
