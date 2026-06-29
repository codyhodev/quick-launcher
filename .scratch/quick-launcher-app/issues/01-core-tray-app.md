Status: done

Parent: `.scratch/quick-launcher-app/PRD.md`

# Slice 1: Core tray app with flat launcher list

## What to build

A minimal but complete end-to-end tray app that:

1. Reads a flat list of launchers from `~/.config/quick-launcher/config.yaml`
2. Builds a flat `QMenu` (no submenus, no separators)
3. Shows a self-drawn rocket icon via `QSystemTrayIcon`
4. Launches commands via `QProcess` when clicked
5. Supports `quit` action to exit
6. Supports `python -m quick_launcher` and a `quick-launcher` CLI entrypoint

This slice includes scaffolding: `pyproject.toml`, package layout, and all four
modules at their initial shape.

## Acceptance criteria

- [ ] `pyproject.toml` is configured with PyQt5 dependency and entrypoint
- [ ] `src/quick_launcher/__main__.py` enables `python -m quick_launcher`
- [ ] `config.py` reads YAML from `~/.config/quick-launcher/config.yaml` and
      returns a list of launcher dicts (with `name` and `command`)
- [ ] `runner.py` launches a command string via `QProcess` when called
- [ ] `menu.py` builds a flat `QMenu` from the launcher list, with each item
      triggering `runner.py`
- [ ] `app.py` creates a `QApplication`, builds the menu, sets a
      `QSystemTrayIcon` with a `QPainter`-drawn rocket icon, and enters the
      event loop
- [ ] The tray icon displays and the menu is clickable on X11
- [ ] Quit action stops the event loop and exits cleanly
- [ ] Integration test verifies: config → menu actions match input

## Blocked by

None — can start immediately
