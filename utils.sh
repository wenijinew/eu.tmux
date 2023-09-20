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
