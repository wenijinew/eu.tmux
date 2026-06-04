#!/usr/bin/env bash
# Widget: Git branch with accent color derived from branch name hash
# Outputs styled branch name where the color is deterministic per branch

pane_path="$(tmux display-message -p '#{pane_current_path}' 2>/dev/null)"
[ -z "$pane_path" ] && exit 0

branch=$(git -C "$pane_path" rev-parse --abbrev-ref HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0

# Hash branch name to a color (16-255 range for 256-color terminals)
hash_value=$(echo -n "$branch" | cksum | awk '{print $1}')
color_index=$(( (hash_value % 200) + 21 ))  # avoid first 21 (too dark/basic)

dirty=$(git -C "$pane_path" status --porcelain 2>/dev/null | head -1)
dirty_marker=""
[ -n "$dirty" ] && dirty_marker="*"

echo "#[fg=colour${color_index}] ${branch}${dirty_marker}#[default]"
