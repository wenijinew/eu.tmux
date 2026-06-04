#!/usr/bin/env bash
# Widget: Pomodoro timer
# State stored in /tmp/eutmux_pomodoro
# Usage: widgets/pomodoro.sh [start|stop|status]

STATE_FILE="/tmp/eutmux_pomodoro"
WORK_MINUTES=25
BREAK_MINUTES=5

start_pomodoro() {
    echo "$(date +%s) work" > "$STATE_FILE"
}

stop_pomodoro() {
    rm -f "$STATE_FILE"
}

show_status() {
    [ ! -f "$STATE_FILE" ] && exit 0

    read -r start_epoch mode < "$STATE_FILE"

    # Validate state file contents
    if ! [[ "$start_epoch" =~ ^[0-9]+$ ]]; then
        rm -f "$STATE_FILE"
        exit 0
    fi
    [ -z "$mode" ] && mode="work"

    now=$(date +%s)
    elapsed_seconds=$(( now - start_epoch ))

    if [ "$mode" = "work" ]; then
        total_seconds=$((WORK_MINUTES * 60))
        remaining=$((total_seconds - elapsed_seconds))
        if [ $remaining -le 0 ]; then
            # Auto-switch to break
            echo "$(date +%s) break" > "$STATE_FILE"
            echo "#[fg=green]☕ BREAK"
        else
            minutes=$((remaining / 60))
            seconds=$((remaining % 60))
            echo "#[fg=red]🍅 ${minutes}:$(printf '%02d' $seconds)"
        fi
    else
        total_seconds=$((BREAK_MINUTES * 60))
        remaining=$((total_seconds - elapsed_seconds))
        if [ $remaining -le 0 ]; then
            # Break over, restart work
            echo "$(date +%s) work" > "$STATE_FILE"
            echo "#[fg=red]🍅 ${WORK_MINUTES}:00"
        else
            minutes=$((remaining / 60))
            seconds=$((remaining % 60))
            echo "#[fg=green]☕ ${minutes}:$(printf '%02d' $seconds)"
        fi
    fi
}

case "${1:-status}" in
    start)  start_pomodoro ;;
    stop)   stop_pomodoro ;;
    *)      show_status ;;
esac
