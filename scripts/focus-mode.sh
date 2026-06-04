#!/usr/bin/env bash
# Focus mode for eu.tmux — minimal status bar when pane is zoomed
# Call from session-window-changed hook or bind to a key.
#
# When zoomed: hide status-left content, shrink status bar
# When unzoomed: restore full status bar

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

is_zoomed=$(tmux display-message -p '#{window_zoomed_flag}')
current_focus=$(tmux show-option -gqv @eutmux_focus_mode 2>/dev/null)

if [ "$is_zoomed" = "1" ] && [ "$current_focus" != "on" ]; then
    # Enter focus mode — save current status-left, set minimal
    tmux set-option -gq @eutmux_saved_status_left "$(tmux show-option -gqv status-left)"
    tmux set-option -gq @eutmux_saved_status_left_length "$(tmux show-option -gqv status-left-length)"
    tmux set-option -g status-left " #S "
    tmux set-option -g status-left-length 10
    tmux set-option -gq @eutmux_focus_mode "on"

elif [ "$is_zoomed" = "0" ] && [ "$current_focus" = "on" ]; then
    # Exit focus mode — restore saved status
    saved_left=$(tmux show-option -gqv @eutmux_saved_status_left)
    saved_length=$(tmux show-option -gqv @eutmux_saved_status_left_length)
    [ -n "$saved_left" ] && tmux set-option -g status-left "$saved_left"
    [ -n "$saved_length" ] && tmux set-option -g status-left-length "$saved_length"
    tmux set-option -gq @eutmux_focus_mode "off"
fi
