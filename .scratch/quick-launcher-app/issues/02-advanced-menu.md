Status: ready-for-agent

Parent: `.scratch/quick-launcher-app/PRD.md`

# Slice 2: Advanced menu — submenus, separators, terminal support

## What to build

Extends the flat launcher from Slice 1 with three features:

1. **Submenus** — entries with an `items` field become nested `QMenu` children
2. **Separators** — entries with `type: separator` render as `addSeparator()`
3. **Terminal wrapping** — the `terminal_cmd` config field sets the default
   terminal emulator; entries with `terminal: true` wrap the command as
   `{terminal_cmd} -- {original_command}`

`terminal_cmd` defaults to `gnome-terminal` when omitted.

## Acceptance criteria

- [ ] Entries with `items` produce nested `QMenu` submenus at arbitrary depth
- [ ] Entries with `type: separator` produce menu divider lines
- [ ] `terminal_cmd` is read from config, defaulting to `gnome-terminal`
- [ ] Entries with `terminal: true` execute via `{terminal_cmd} -- {command}`
- [ ] Entries with `terminal: false` (or omitted) execute directly
- [ ] Integration test verifies: submenu nesting depth, separator positions,
      command wrapping for terminal: true / false / omitted

## Blocked by

- `01-core-tray-app.md`
