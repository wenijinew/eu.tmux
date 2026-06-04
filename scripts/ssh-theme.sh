#!/usr/bin/env bash
# SSH host-aware theming — changes theme when SSH session detected
# Hashes the remote hostname to a deterministic theme color.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"
THEMES_DIR="${SCRIPT_DIR}/../themes"

# Detect if current pane is running SSH
pane_command=$(tmux display-message -p '#{pane_current_command}')
[ "$pane_command" != "ssh" ] && exit 0

# Extract hostname from pane title (SSH usually sets it)
pane_title=$(tmux display-message -p '#{pane_title}')
ssh_host="${pane_title%%:*}"
[ -z "$ssh_host" ] && exit 0

# Check for explicit mapping file
mapping_file="${XDG_CONFIG_HOME:-$HOME/.config}/eutmux/ssh-themes.conf"
if [ -f "$mapping_file" ]; then
    mapped_theme=$(grep "^${ssh_host}=" "$mapping_file" | cut -d= -f2)
    if [ -n "$mapped_theme" ]; then
        "${EUTMUX_SCRIPT}" -t "$mapped_theme"
        exit 0
    fi
fi

# Hash hostname to theme
available_themes=()
for theme_file in "$THEMES_DIR"/*.theme.yaml; do
    [ -f "$theme_file" ] || continue
    theme_name="$(basename "$theme_file" .theme.yaml)"
    [[ "$theme_name" == template* ]] && continue
    available_themes+=("$theme_name")
done

[ ${#available_themes[@]} -eq 0 ] && exit 0

hash_value=$(echo -n "$ssh_host" | cksum | awk '{print $1}')
theme_index=$((hash_value % ${#available_themes[@]}))
selected_theme="${available_themes[$theme_index]}"

current_theme="$(tmux show-option -gqv @eutmux_current_theme 2>/dev/null)"
if [ "$current_theme" != "$selected_theme" ]; then
    tmux set-option -gq @eutmux_current_theme "$selected_theme"
    tmux set-option -gq @eutmux_ssh_host "$ssh_host"
    "${EUTMUX_SCRIPT}" -t "$selected_theme"
fi
