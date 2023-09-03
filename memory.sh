#!/usr/bin/env bash
source "utils.sh"

violet_memory(){
    mem_total_and_used=$(free | grep Mem | sed -E -e's/\s+/ /g' | cut -d' ' -f2,3)
    mem_total=$(echo $mem_total_and_used | cut -d' ' -f1)
    mem_used=$(echo $mem_total_and_used | cut -d' ' -f2)
    mem_usage_percentage=$(percentage $mem_used $mem_total)
    echo "${mem_usage_percentage}"
}
export violet_memory

violet_memory
