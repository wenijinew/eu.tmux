#!/usr/bin/env bash
# Focus mode for eu.tmux — minimal status bar when pane is zoomed or window is IDE
#
# Zoomed or IDE window → eutmux.tmux -b (minimal bar)
# Unzoomed non-IDE     → eutmux.tmux -B (restore full bar)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"

is_zoomed=$(tmux display-message -p '#{window_zoomed_flag}')
current_window=$(tmux display-message -p '#W')

if [ "$is_zoomed" = "1" ] || [ "$current_window" = "IDE" ]; then
    "${EUTMUX_SCRIPT}" -b
else
    "${EUTMUX_SCRIPT}" -B
fi
