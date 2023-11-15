#!/usr/bin/env bash
#
EXIT_SUCCESS=0
EXIT_ABNORMAL=2
TRUE=0
FALSE=1

percentage(){
    local var1="$1"
    local var2="$2"
    if [ "$var2" -le 0 ];then
        echo "0.00%"
        return "${EXIT_ABNORMAL}"
    fi
    declare result
    local awk_script="{ printf( \"%3.2f%%\n\", ($1/$2)*100 ) }"
    result=$(echo "$var1" "$var2" | env awk "$awk_script")
    echo "$result"
    return "${EXIT_SUCCESS}"
}

#
is_over_used(){
  local usage=$1
  local total=$2

  _is_high=$(bc << EOF
    scale = 2
    benchmark = .60
    quotient = $usage / $total
    define flag(q){
      if (q < benchmark) return $FALSE
      return $TRUE
    }
    flag(quotient)
EOF
)
  echo "$_is_high"
  return "${EXIT_SUCCESS}"
}

_warn(){
    echo -e "\033[35mWARNING:\033[0m ${1}"
    return "${EXIT_SUCCESS}"
}

echoh(){
    env echo -e "$@"
    return "${EXIT_SUCCESS}"
}
prepend_path(){
    for p in $*
    do
        readable "${p}"
        exists=$?
        echo "${PATH}" | grep -q "${p}" 2>/dev/null
        in_path=$?
        if [[ $exists -eq $TRUE && $in_path -ne $TRUE ]];then
            export PATH="${p}:${PATH}"
        fi
    done
}

prepend_pythonpath(){
    for p in $*
    do
        readable "${p}"
        exists=$?
        echo "${PYTHONPATH}" | grep -q "${p}" 2>/dev/null
        in_path=$?
        if [[ $exists -eq $TRUE && $in_path -ne $TRUE ]];then
            export PYTHONPATH="${p}:${PYTHONPATH}"
        fi
    done
}

readable(){
    if [[ "${1}" == "" ||  ! -r "${1}" ]];then
        _warn "${1} doesn't exist!"
        return ${FALSE}
    fi
    return ${TRUE}
}
