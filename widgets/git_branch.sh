#!/usr/bin/env bash
# Widget: git branch name with dirty indicator
branch=$(git -C "$(tmux display-message -p '#{pane_current_path}')" rev-parse --abbrev-ref HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0
dirty=$(git -C "$(tmux display-message -p '#{pane_current_path}')" status --porcelain 2>/dev/null | head -1)
[ -n "$dirty" ] && echo " ${branch}*" || echo " ${branch}"
