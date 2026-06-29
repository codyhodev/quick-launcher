# quick-launcher

Linux X11 托盘应用程序, 用于快速启动应用程序或脚本.

## Stack

- **Language:** Python (>=3.12)
- **Package manager:** `uv` — use `uv add`, `uv sync`, `uv run`, `uv build`
- **Tray library:** PyQt5
- **Test runner:** pytest (`QT_QPA_PLATFORM=offscreen` for headless)

## Project structure

```
/pyproject.toml
/src/quick_launcher/
    __init__.py
    __main__.py          # python -m quick_launcher
    app.py               # QApplication, QSystemTrayIcon, QPainter icon, main()
    config.py            # YAML config → LauncherEntry
    menu.py              # LauncherEntry list → QMenu
    runner.py            # QProcess command execution
/tests/
    test_config.py
    test_menu.py
    test_integration.py
```

## Developer commands

TBD — will follow `uv` conventions.

Run tests: `QT_QPA_PLATFORM=offscreen uv run pytest`
Run a single test: `QT_QPA_PLATFORM=offscreen uv run pytest tests/test_menu.py::test_build_menu_flat_launchers -v`
Run the app: `uv run quick-launcher` (needs a running X server and `~/.config/quick-launcher/config.yaml`)

## Known quirks

- X11 tray requires a running X server; tests may need `xvfb-run`.
- On Wayland-only sessions, X11 tray apps may not work without XWayland.

## Agent skills

### Issue tracker

Issues are tracked as local markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

All five canonical roles use their default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
