#!/usr/bin/env bash
source "utils.sh"

utmux_disk(){
    disk_usage=$(df -h 2>/dev/null | grep rootvg-root | sed -E -e's/\s+/ /g' | cut -d ' ' -f5 | cut -d% -f1)
    echo "${disk_usage}%"
}
export utmux_disk

utmux_disk
