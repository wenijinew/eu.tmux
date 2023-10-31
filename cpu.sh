#!/usr/bin/env bash
#
#
#
eutmux_cpu(){
    cpu_usage="$(ps -eo %cpu,pid,cmd --sort -%cpu | sed -e '1d' | awk '{sum +=\
    $1};END {print sum}')"
    echo "${cpu_usage}%"
}
export eutmux_cpu

eutmux_cpu
