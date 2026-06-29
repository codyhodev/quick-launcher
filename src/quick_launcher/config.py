from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class LauncherEntry:
    name: str
    command: str


def default_config_path() -> str:
    return str(Path.home() / ".config" / "quick-launcher" / "config.yaml")


def load_config(path: str | None = None) -> list[LauncherEntry]:
    if path is None:
        path = default_config_path()

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    launchers = data.get("launchers", [])
    return [LauncherEntry(**item) for item in launchers]
