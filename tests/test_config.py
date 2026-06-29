import os
import tempfile
from pathlib import Path

import pytest
import yaml

from quick_launcher.config import load_config, LauncherEntry


def test_load_config_flat_launchers():
    data = {
        "launchers": [
            {"name": "Terminal", "command": "alacritty"},
            {"name": "Browser", "command": "firefox"},
            {"name": "Build", "command": "./build.sh"},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        result = load_config(path)
        assert len(result) == 3
        assert result[0] == LauncherEntry(name="Terminal", command="alacritty")
        assert result[1] == LauncherEntry(name="Browser", command="firefox")
        assert result[2] == LauncherEntry(name="Build", command="./build.sh")
    finally:
        os.unlink(path)


def test_load_config_empty_launchers():
    data = {"launchers": []}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        path = f.name

    try:
        result = load_config(path)
        assert result == []
    finally:
        os.unlink(path)


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/path/config.yaml")
