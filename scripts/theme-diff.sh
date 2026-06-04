#!/usr/bin/env bash
# Theme diff — compare two eu.tmux themes side-by-side
# Usage: theme-diff.sh <theme1> <theme2>

THEMES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../themes" && pwd)"

theme_one="${1:?Usage: theme-diff.sh <theme1> <theme2>}"
theme_two="${2:?Usage: theme-diff.sh <theme1> <theme2>}"

file_one="${THEMES_DIR}/${theme_one}.theme.yaml"
file_two="${THEMES_DIR}/${theme_two}.theme.yaml"

[ ! -f "$file_one" ] && echo "Theme not found: $theme_one" && exit 1
[ ! -f "$file_two" ] && echo "Theme not found: $theme_two" && exit 1

if command -v delta &>/dev/null; then
    delta --side-by-side "$file_one" "$file_two"
elif command -v diff &>/dev/null; then
    diff --color=always -y "$file_one" "$file_two"
else
    echo "Install delta or diff for theme comparison"
    exit 1
fi
