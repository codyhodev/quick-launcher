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


def test_build_menu_with_separator(qapp):
    launchers = [
        LauncherEntry(name="App1", command="app1"),
        LauncherEntry(name="", type="separator"),
        LauncherEntry(name="App2", command="app2"),
    ]

    menu = build_menu(launchers)
    actions = menu.actions()

    assert len(actions) == 3
    assert actions[0].text() == "App1"
    assert actions[1].isSeparator()
    assert actions[2].text() == "App2"


def test_build_menu_with_submenu(qapp):
    launchers = [
        LauncherEntry(
            name="Dev",
            items=[
                LauncherEntry(name="Editor", command="code"),
                LauncherEntry(name="Terminal", command="alacritty"),
            ],
        ),
    ]

    menu = build_menu(launchers)
    actions = menu.actions()

    assert len(actions) == 1
    assert actions[0].text() == "Dev"
    assert actions[0].menu() is not None
    sub_actions = actions[0].menu().actions()
    assert len(sub_actions) == 2
    assert sub_actions[0].text() == "Editor"
    assert sub_actions[1].text() == "Terminal"


def test_build_menu_with_custom_font_size(qapp):
    launchers = [LauncherEntry(name="App", command="app")]
    menu = build_menu(launchers, font_size=20)
    assert menu.font().pointSize() == 20


def test_build_menu_nested_submenus(qapp):
    launchers = [
        LauncherEntry(
            name="Outer",
            items=[
                LauncherEntry(
                    name="Inner",
                    items=[
                        LauncherEntry(name="Leaf", command="leaf"),
                    ],
                ),
            ],
        ),
    ]

    menu = build_menu(launchers)
    outer_action = menu.actions()[0]
    inner_menu = outer_action.menu()
    assert inner_menu is not None
    inner_action = inner_menu.actions()[0]
    assert inner_action.text() == "Inner"
    leaf_menu = inner_action.menu()
    assert leaf_menu is not None
    assert leaf_menu.actions()[0].text() == "Leaf"
