#!/usr/bin/env bash
# Widget: Spotify/media now playing (via playerctl or osascript)

if command -v playerctl &>/dev/null; then
    status=$(playerctl status 2>/dev/null)
    [ "$status" != "Playing" ] && exit 0
    artist=$(playerctl metadata artist 2>/dev/null | cut -c1-15)
    title=$(playerctl metadata title 2>/dev/null | cut -c1-20)
    echo "♪ ${artist} - ${title}"
elif [ "$(uname)" = "Darwin" ] && command -v osascript &>/dev/null; then
    track=$(osascript -e 'tell application "Spotify" to name of current track' 2>/dev/null)
    [ -z "$track" ] && exit 0
    echo "♪ ${track:0:30}"
fi
