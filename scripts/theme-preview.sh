#!/usr/bin/env bash
# Theme preview with auto-revert
# Shows a theme for N seconds then reverts to previous.
# Usage: theme-preview.sh <theme-name> [seconds]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"

theme_name="${1:?Usage: theme-preview.sh <theme-name> [seconds]}"
preview_duration="${2:-3}"

# Save current theme
original_theme="$(tmux show-option -gqv @eutmux_current_theme 2>/dev/null)"
[ -z "$original_theme" ] && original_theme="burgundy-red"

# Apply preview
"${EUTMUX_SCRIPT}" -t "$theme_name"
tmux display-message "Preview: ${theme_name} (reverting in ${preview_duration}s)"

# Revert after delay
sleep "$preview_duration"
"${EUTMUX_SCRIPT}" -t "$original_theme"
tmux set-option -gq @eutmux_current_theme "$original_theme"
tmux display-message "Reverted to: ${original_theme}"
