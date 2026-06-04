#!/usr/bin/env bash
# Time-of-day theme shifting for eu.tmux
# Warm tones at night, cool tones during work hours.
# Call from hook or cron: scripts/time-theme.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"

# Configurable theme mapping
MORNING_THEME="${EUTMUX_MORNING_THEME:-blue-green}"       # 06:00-11:59
AFTERNOON_THEME="${EUTMUX_AFTERNOON_THEME:-emerald-green}" # 12:00-17:59
EVENING_THEME="${EUTMUX_EVENING_THEME:-burgundy-red}"      # 18:00-21:59
NIGHT_THEME="${EUTMUX_NIGHT_THEME:-black-pearl}"           # 22:00-05:59

get_time_theme() {
    local hour
    hour=$(date +%H)
    hour=$((10#$hour))  # force base-10

    if [ $hour -ge 6 ] && [ $hour -lt 12 ]; then
        echo "$MORNING_THEME"
    elif [ $hour -ge 12 ] && [ $hour -lt 18 ]; then
        echo "$AFTERNOON_THEME"
    elif [ $hour -ge 18 ] && [ $hour -lt 22 ]; then
        echo "$EVENING_THEME"
    else
        echo "$NIGHT_THEME"
    fi
}

main() {
    local time_theme
    time_theme="$(get_time_theme)"

    # Only apply if different from current
    local current_theme
    current_theme="$(tmux show-option -gqv @eutmux_current_theme 2>/dev/null)"
    if [ "$current_theme" != "$time_theme" ]; then
        tmux set-option -gq @eutmux_current_theme "$time_theme"
        "${EUTMUX_SCRIPT}" -t "$time_theme"
    fi
}

main "$@"
