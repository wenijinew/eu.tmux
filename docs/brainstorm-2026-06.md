# Eu.tmux Brainstorm — June 2026

## Theme Intelligence
- **Auto-dark/light** — Detect terminal background (OSC 11 query), auto-switch
- **Time-of-day themes** — Warm tones at night, cool tones during work hours
- **Git-branch-aware** — Hash branch name → unique accent color
- **CI status in bar** — Green/red dot for last pipeline status

## Automation
- **Project profiles** — Detect `pwd` → auto-apply theme (`.eutmux.project` file)
- **SSH host themes** — Auto-change theme when SSH session detected
- **Focus mode** — Maximized pane → minimal status bar; restore on unzoom
- **Pomodoro integration** — Timer widget, color shift work vs break

## Plugin Architecture
- **Widget system** — YAML-defined status widgets (composable modules)
- **Theme marketplace** — `eutmux install-theme <name>` from community registry
- **Export to alacritty/kitty** — Sync terminal colors from eu.tmux theme
- **Import from terminal** — Read terminal theme → generate eu.tmux theme

## Status Bar Modules
- **Kubernetes context** — Active k8s context/namespace
- **LaaS env indicator** — Environment name with color coding
- **Spotify/media** — Now playing in right status
- **Battery + network** — YAML-configurable system widgets

## Developer Experience
- **Live reload** — Watch config file, auto-apply on save (inotify/fswatch)
- **Theme preview** — 3-second preview then revert
- **Color picker TUI** — Interactive HSL sliders in tmux popup
- **Theme diff** — Side-by-side color comparison

---

## Top 3 Priorities

### 1. Project-Aware Auto-Theming
Drop a `.eutmux.project` file in any repo root. When you `cd` into it (via
session-window-changed hook), eu.tmux auto-applies the specified theme.
Fallback: hash the directory path to a deterministic color if no file exists.

### 2. Live Reload on Config Change
Background watcher (fswatch/inotifywait) monitors `eutmux.yaml` and theme files.
On change → `tmux refresh-client` with new theme applied. Zero manual steps.

### 3. Widget System (Composable Status Bar)
Define status-right as a list of widget modules in YAML:
```yaml
status_right:
  widgets:
    - name: git_branch
    - name: k8s_context
    - name: cpu
    - name: clock
```
Each widget = a script that outputs formatted text. Separator configurable.
Community can contribute widgets as standalone repos.
