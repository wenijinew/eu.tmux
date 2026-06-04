#!/usr/bin/env bash
# Project-aware auto-theming for eu.tmux
# Detects .eutmux.project in cwd ancestors and applies the specified theme.
# Falls back to hashing the directory path for a deterministic color theme.
#
# Usage: source this from session-window-changed hook or bind to a key.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EUTMUX_SCRIPT="${SCRIPT_DIR}/eutmux.tmux"

# Walk up directory tree looking for .eutmux.project
find_project_theme() {
    local search_dir="$1"
    [ -z "$search_dir" ] && return 1
    while [ "$search_dir" != "/" ] && [ "$search_dir" != "$(dirname "$search_dir")" ]; do
        if [ -f "$search_dir/.eutmux.project" ]; then
            cat "$search_dir/.eutmux.project"
            return 0
        fi
        search_dir="$(dirname "$search_dir")"
    done
    return 1
}

# Hash directory path to pick a deterministic theme from available themes
hash_directory_to_theme() {
    local directory_path="$1"
    local themes_dir="${SCRIPT_DIR}/../themes"
    local available_themes=()

    for theme_file in "$themes_dir"/*.theme.yaml; do
        [ -f "$theme_file" ] || continue
        local theme_name
        theme_name="$(basename "$theme_file" .theme.yaml)"
        # Skip templates
        [[ "$theme_name" == template* ]] && continue
        available_themes+=("$theme_name")
    done

    [ ${#available_themes[@]} -eq 0 ] && return 1

    # Hash path to index
    local hash_value
    hash_value=$(echo -n "$directory_path" | cksum | awk '{print $1}')
    local theme_index=$((hash_value % ${#available_themes[@]}))

    echo "${available_themes[$theme_index]}"
}

main() {
    local current_pane_path
    current_pane_path="$(tmux display-message -p '#{pane_current_path}')"

    [ -z "$current_pane_path" ] && exit 0

    # Priority 1: explicit .eutmux.project file
    local project_theme
    project_theme="$(find_project_theme "$current_pane_path")"

    # Only apply if explicit .eutmux.project was found
    if [ -z "$project_theme" ]; then
        exit 1
    fi

    # Only apply if theme changed (avoid flicker)
    local current_theme
    current_theme="$(tmux show-option -gqv @eutmux_current_theme 2>/dev/null)"
    if [ "$current_theme" != "$project_theme" ]; then
        tmux set-option -gq @eutmux_current_theme "$project_theme"
        "${EUTMUX_SCRIPT}" -t "$project_theme"
    fi
}

main "$@"
