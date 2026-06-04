#!/usr/bin/env bash
# Widget: CI/pipeline status (checks last Jenkins/GitHub Actions result)
# Reads from env var or checks git remote for status

# Priority 1: explicit env var (set by CI watcher)
if [ -n "$EUTMUX_CI_STATUS" ]; then
    case "$EUTMUX_CI_STATUS" in
        pass*|success*) echo "#[fg=green]● CI" ;;
        fail*)          echo "#[fg=red]● CI" ;;
        running*)       echo "#[fg=yellow]◐ CI" ;;
        *)              echo "#[fg=grey]○ CI" ;;
    esac
    exit 0
fi

# Priority 2: gh CLI (GitHub Actions)
pane_path="$(tmux display-message -p '#{pane_current_path}' 2>/dev/null)"
[ -z "$pane_path" ] && exit 0

branch=$(git -C "$pane_path" rev-parse --abbrev-ref HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0

# Cache result for 60s to avoid API spam
cache_file="/tmp/eutmux_ci_${branch}.cache"
if [ -f "$cache_file" ]; then
    cache_age=$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file" 2>/dev/null || echo 0) ))
    if [ "$cache_age" -lt 60 ]; then
        cat "$cache_file"
        exit 0
    fi
fi

# Try gh CLI
if command -v gh &>/dev/null; then
    status=$(gh run list -b "$branch" --limit 1 --json conclusion -q '.[0].conclusion' 2>/dev/null)
    case "$status" in
        success)    result="#[fg=green]● CI" ;;
        failure)    result="#[fg=red]● CI" ;;
        "")         result="#[fg=yellow]◐ CI" ;;
        *)          result="#[fg=grey]○ CI" ;;
    esac
    echo "$result" | tee "$cache_file"
fi
