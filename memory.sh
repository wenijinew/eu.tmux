#!/usr/bin/env bash
source "utils.sh"

glamour_memory(){
    mem_total_and_used=$(free | grep Mem | sed -E -e's/\s+/ /g' | cut -d' ' -f2,3)
    mem_total=$(echo $mem_total_and_used | cut -d' ' -f1)
    mem_used=$(echo $mem_total_and_used | cut -d' ' -f2)
    local mem_usage_percentage
    mem_usage_percentage=$(percentage ${mem_used} ${mem_total})
    is_mem_over_used=$(is_over_used ${mem_used} ${mem_total})
    if [ $is_mem_over_used -eq $TRUE ];then
        style=$(tmux show -gqv "@style")
        fg_highlight=$(tmux show -gqv "@fg_highlight")
        bg_highlight=$(tmux show -gqv "@bg_highlight")
        _style="${style:-'nobold,nounderscore,noitalics'}"
        if [ "${fg_highlight}" != "" ];then
            _style="${_style},fg=${fg_highlight}"
        fi
        if [ "${bg_highlight}" != "" ];then
            _style="${_style},bg=${bg_highlight}"
        fi
        mem_usage_percentage="#[${_style}] ${mem_usage_percentage} "
    else
        mem_usage_percentage=" ${mem_usage_percentage} "
    fi
    echo "${mem_usage_percentage}"
}
export glamour_memory

glamour_memory
