import os
import tempfile

import pytest
import yaml
from PyQt5.QtWidgets import QApplication

from quick_launcher.config import load_config
from quick_launcher.menu import build_menu


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_config_to_menu_pipeline(qapp):
    data = {
        "launchers": [
            {"name": "Terminal", "command": "alacritty"},
            {"name": "Browser", "command": "firefox"},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        menu = build_menu(config.launchers)
        actions = menu.actions()

        assert len(actions) == 2
        assert actions[0].text() == "Terminal"
        assert actions[1].text() == "Browser"
    finally:
        os.unlink(path)


def test_config_to_menu_with_quit_action(qapp):
    data = {
        "launchers": [
            {"name": "App1", "command": "app1"},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        menu = build_menu(config.launchers)
        menu.addAction("Quit")
        actions = menu.actions()

        assert len(actions) == 2
        assert actions[0].text() == "App1"
        assert actions[1].text() == "Quit"
    finally:
        os.unlink(path)


def test_tray_app_menu_structure(qapp):
    from quick_launcher.app import TrayApp
    from quick_launcher.config import Config, LauncherEntry

    cfg = Config(
        launchers=[
            LauncherEntry(name="Terminal", command="alacritty"),
            LauncherEntry(name="Browser", command="firefox"),
        ]
    )
    tray = TrayApp(cfg)
    actions = tray.contextMenu().actions()

    assert len(actions) == 3  # 2 launchers + Quit
    assert actions[0].text() == "Terminal"
    assert actions[1].text() == "Browser"
    assert actions[2].text() == "Quit"


def test_tray_app_with_advanced_config(qapp):
    from quick_launcher.app import TrayApp
    from quick_launcher.config import Config, LauncherEntry

    cfg = Config(
        terminal_cmd="alacritty",
        launchers=[
            LauncherEntry(
                name="Dev",
                items=[
                    LauncherEntry(name="Editor", command="code", terminal=True),
                ],
            ),
            LauncherEntry(type="separator"),
            LauncherEntry(name="Browser", command="firefox"),
        ],
    )
    tray = TrayApp(cfg)
    actions = tray.contextMenu().actions()

    assert len(actions) == 4  # Dev submenu + separator + Browser + Quit
    assert actions[0].text() == "Dev"
    assert actions[0].menu() is not None
    assert actions[1].isSeparator()
    assert actions[2].text() == "Browser"
    assert actions[3].text() == "Quit"


def test_config_to_menu_with_font_size(qapp):
    data = {
        "font_size": 16,
        "launchers": [{"name": "App", "command": "app"}],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        menu = build_menu(config.launchers, font_size=config.font_size)
        assert config.font_size == 16
        assert menu.font().pointSize() == 16
    finally:
        os.unlink(path)


def test_config_to_menu_with_submenu(qapp):
    data = {
        "launchers": [
            {
                "name": "Dev",
                "items": [
                    {"name": "Editor", "command": "code"},
                    {"name": "Terminal", "command": "alacritty"},
                ],
            },
            {"type": "separator"},
            {"name": "Browser", "command": "firefox"},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        menu = build_menu(config.launchers)
        actions = menu.actions()

        assert len(actions) == 3
        assert actions[0].text() == "Dev"
        sub_actions = actions[0].menu().actions()
        assert len(sub_actions) == 2
        assert sub_actions[0].text() == "Editor"
        assert sub_actions[1].text() == "Terminal"
        assert actions[1].isSeparator()
        assert actions[2].text() == "Browser"
    finally:
        os.unlink(path)
