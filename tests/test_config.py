import os
import tempfile

import pytest
import yaml

from quick_launcher.config import Config, LauncherEntry, load_config


def test_load_config_flat_launchers():
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
        assert len(config.launchers) == 2
        assert config.launchers[0] == LauncherEntry(name="Terminal", command="alacritty")
        assert config.launchers[1] == LauncherEntry(name="Browser", command="firefox")
    finally:
        os.unlink(path)


def test_load_config_empty_launchers():
    data = {"launchers": []}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        assert config.launchers == []
    finally:
        os.unlink(path)


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/path/config.yaml")


def test_load_config_default_terminal_cmd():
    data = {"launchers": [{"name": "App", "command": "app"}]}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        assert config.terminal_cmd == "gnome-terminal"
    finally:
        os.unlink(path)


def test_load_config_custom_terminal_cmd():
    data = {
        "terminal_cmd": "alacritty",
        "launchers": [{"name": "App", "command": "app"}],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        assert config.terminal_cmd == "alacritty"
    finally:
        os.unlink(path)


def test_load_config_with_submenus():
    data = {
        "launchers": [
            {
                "name": "Dev",
                "items": [
                    {"name": "Editor", "command": "code"},
                    {"name": "Terminal", "command": "alacritty", "terminal": True},
                ],
            },
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        assert len(config.launchers) == 1
        dev = config.launchers[0]
        assert dev.name == "Dev"
        assert dev.command is None
        assert dev.items is not None
        assert len(dev.items) == 2
        assert dev.items[0].name == "Editor"
        assert dev.items[0].command == "code"
        assert dev.items[1].name == "Terminal"
        assert dev.items[1].terminal is True
    finally:
        os.unlink(path)


def test_load_config_with_separator():
    data = {
        "launchers": [
            {"name": "App1", "command": "app1"},
            {"type": "separator"},
            {"name": "App2", "command": "app2"},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        config = load_config(path)
        assert len(config.launchers) == 3
        assert config.launchers[1].type == "separator"
    finally:
        os.unlink(path)
