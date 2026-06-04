#!/usr/bin/env bash
# Live reload for eu.tmux — watches config/theme files and auto-applies changes.
#
# Usage:
#   eutmux-live-reload start   — start background watcher
#   eutmux-live-reload stop    — stop background watcher
#   eutmux-live-reload status  — check if running
#
# Requires: inotifywait (inotify-tools) or fswatch

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"
PID_FILE="/tmp/eutmux-live-reload.pid"

WATCH_PATHS=(
    "${XDG_CONFIG_HOME:-$HOME/.config}/eutmux"
    "${SCRIPT_DIR}/../themes"
    "$HOME/.tmux/plugins/eu.tmux/themes"
)

watch_with_inotifywait() {
    local watch_dirs=()
    for watch_path in "${WATCH_PATHS[@]}"; do
        [ -d "$watch_path" ] && watch_dirs+=("$watch_path")
    done

    [ ${#watch_dirs[@]} -eq 0 ] && {
        echo "No watch directories found"
        exit 1
    }

    inotifywait -m -r -e modify,create --include '\.yaml$' "${watch_dirs[@]}" |
    while read -r _directory _events _filename; do
        # Debounce: wait 500ms for rapid saves
        sleep 0.5
        "${EUTMUX_SCRIPT}" -R
        tmux display-message "eu.tmux: theme reloaded (${_filename})"
    done
}

watch_with_fswatch() {
    local watch_dirs=()
    for watch_path in "${WATCH_PATHS[@]}"; do
        [ -d "$watch_path" ] && watch_dirs+=("$watch_path")
    done

    fswatch -r --include='\.yaml$' --exclude='.*' "${watch_dirs[@]}" |
    while read -r changed_file; do
        sleep 0.5
        "${EUTMUX_SCRIPT}" -R
        tmux display-message "eu.tmux: theme reloaded ($(basename "$changed_file"))"
    done
}

start_watcher() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Live reload already running (PID $(cat "$PID_FILE"))"
        return 0
    fi

    if command -v inotifywait &>/dev/null; then
        watch_with_inotifywait &
    elif command -v fswatch &>/dev/null; then
        watch_with_fswatch &
    else
        echo "Error: install inotify-tools or fswatch for live reload"
        exit 1
    fi

    echo $! > "$PID_FILE"
    echo "Live reload started (PID $!)"
}

stop_watcher() {
    if [ -f "$PID_FILE" ]; then
        local watcher_pid
        watcher_pid="$(cat "$PID_FILE")"
        kill "$watcher_pid" 2>/dev/null && echo "Stopped (PID $watcher_pid)"
        rm -f "$PID_FILE"
    else
        echo "Not running"
    fi
}

show_status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Running (PID $(cat "$PID_FILE"))"
    else
        echo "Not running"
        rm -f "$PID_FILE" 2>/dev/null
    fi
}

case "${1:-status}" in
    start)  start_watcher ;;
    stop)   stop_watcher ;;
    status) show_status ;;
    *)      echo "Usage: $0 {start|stop|status}" ;;
esac
