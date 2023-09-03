#!/usr/bin/env bash
source "utils.sh"

violet_disk(){
    disk_usage=$(df -h 2>/dev/null | grep rootvg-root | sed -E -e's/\s+/ /g' | cut -d ' ' -f5 | cut -d% -f1)
    echo "${disk_usage}%"
}
export violet_disk

violet_disk
