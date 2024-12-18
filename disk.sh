#!/usr/bin/env bash
source "utils.sh"

# culculate disk usage and show percentage of the free disk space
eutmux_disk(){
    disk_usage=$(df -h 2>/dev/null | grep rootvg-root | sed -E -e's/\s+/ /g' | cut -d ' ' -f5 | cut -d% -f1)
    echo "${disk_usage}%"
}
export eutmux_disk

eutmux_disk
