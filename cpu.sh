#!/usr/bin/env bash
#
#
#
utmux_cpu(){
    cpu_usage="$(ps -eo %cpu,pid,cmd --sort -%cpu | sed -e '1d' | awk '{sum +=\
    $1};END {print sum}')"
    echo "${cpu_usage}%"
}
export utmux_cpu

utmux_cpu
