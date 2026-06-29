from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class LauncherEntry:
    name: str = ""
    command: str | None = None
    terminal: bool = False
    type: str | None = None
    items: list[LauncherEntry] | None = None


@dataclass
class Config:
    terminal_cmd: str = "gnome-terminal"
    font_size: int = 14
    launchers: list[LauncherEntry] = field(default_factory=list)


def default_config_path() -> str:
    return str(Path.home() / ".config" / "quick-launcher" / "config.yaml")


def _parse_entry(item: dict) -> LauncherEntry:
    if item.get("type") == "separator":
        return LauncherEntry(type="separator")
    kw = dict(item)
    if "items" in kw:
        kw["items"] = [_parse_entry(child) for child in kw["items"]]
    return LauncherEntry(**kw)


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = default_config_path()

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Config(
        terminal_cmd=data.get("terminal_cmd", "gnome-terminal"),
        font_size=data.get("font_size", 14),
        launchers=[_parse_entry(item) for item in data.get("launchers", [])],
    )
