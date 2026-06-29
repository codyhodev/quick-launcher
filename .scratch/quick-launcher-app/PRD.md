Status: done

# PRD: quick-launcher

## Problem Statement

In Linux X11 desktop environments, users need a lightweight, quick way to launch
frequently-used applications and scripts. Existing launchers (dmenu, rofi)
require keyboard interaction and lack a system-tray permanent presence; desktop
environments' built-in tray tools have complex configuration. Users need a
system-tray-based quick launcher with a statically defined YAML configuration
file.

## Solution

A PyQt5-based Linux X11 system tray application. Users define launcher entries
by editing `~/.config/quick-launcher/config.yaml`. The configuration supports:

- Multi-level nested submenus
- Separator lines
- Run-in-terminal option (configurable terminal emulator)
- Arbitrary commands or external script files

The application is installed via `uv tool install` and accessed through a
self-drawn rocket icon in the system tray.

## User Stories

1. As a user, I want a clickable icon in the system tray, so that I can access
   the launch menu at any time
2. As a user, I want to define the launcher list via a YAML file, so that I can
   freely control which applications appear
3. As a user, I want multi-level submenu support, so that I can organize
   launchers by category
4. As a user, I want separator lines in the menu, so that I can group related
   launcher entries
5. As a user, I want certain commands to run inside a terminal, so that I can
   run programs like htop or pip that produce terminal output
6. As a user, I want to configure the default terminal emulator, so that I can
   use my preferred terminal (e.g. alacritty)
7. As a user, I want to run external script files by path, so that I can reuse
   existing automation scripts
8. As a user, I want to install the application via `uv tool install`, so that
   `quick-launcher` is available globally
9. As a user, I want the program to read the config file automatically on
   startup, so that I can see my menu configuration without extra steps
10. As a user, I want the program to fully exit when I quit the tray, so that
    no background processes remain

## Implementation Decisions

- **Tray icon**: PyQt5 `QSystemTrayIcon` with a rocket shape drawn via
  `QPainter`
- **Config format**: YAML; file path hardcoded to
  `~/.config/quick-launcher/config.yaml`; no `--config` flag
- **Terminal emulator**: config field `terminal_cmd`, default `gnome-terminal`.
  When `terminal: true`, the executed command becomes
  `{terminal_cmd} -- {original_command}`
- **Command execution**: `QProcess` for non-blocking external process launch
- **Entry point**: `[project.scripts]` in `pyproject.toml` defines
  `quick-launcher`; also supports `python -m quick_launcher`
- **Menu construction**: recursive walk of the parsed config tree — leaf nodes
  become `QAction`, interior nodes become child `QMenu`, `type: separator`
  becomes `addSeparator()`
- **Module split**: `config.py` (YAML read/validate), `menu.py` (config → QMenu
  tree), `runner.py` (command execution via QProcess), `app.py`
  (QApplication lifecycle + tray icon management)

## Testing Decisions

- **Strategy**: test external behaviour only (menu structure, command
  construction), not implementation details
- **Scope**: one integration test module covering the full pipeline
  YAML → menu construction → command execution
- **Runtime**: `Qt.QPA.platform=offscreen` under `xvfb-run`
- **What is tested**:
  - Submenu config produces correct `QMenu` nesting
  - Separator positions in the menu are correct
  - `terminal: true/false` produces correct command strings
  - Missing optional fields (e.g. `terminal`) use defaults
- **Not tested**:
  - `QPainter` icon output (visual verification)
  - `QSystemTrayIcon` OS-level interaction (cannot mock)

## Out of Scope

- Config hot-reload (requires restart after editing YAML)
- Auto-start on login
- GUI config editor
- Themed or custom icons
- Native Wayland support (XWayland only)
- Windows/macOS cross-platform support
- Search/filter functionality
- Keyboard shortcut bindings

## Further Notes

- X11 tray requires a running X server; tests need `xvfb-run`
- On pure Wayland sessions the X11 tray may not work; recommend X11 or XWayland
- The program does not gracefully handle YAML syntax errors — it will error and
  exit on startup
