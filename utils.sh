#!/usr/bin/env bash
#
E_ABNORMAL_STATE=2
TRUE=0
FALSE=1

percentage(){
    local var1="$1"
    local var2="$2"
    if [ $var2 -le 0 ];then
        echo "0.00%"
        return $E_ABNORMAL_STATE
    fi
	declare result
    local awk_script='{ printf( "%3.2f%%\n", ($1/$2)*100 ) }'
    result=$(echo $var1 $var2 | env awk "$awk_script")
    echo "$result"
}

#
is_over_used(){
  local usage=$1
  local total=$2

  _is_high=`bc << EOF
    scale = 2
    benchmark = .60
    quotient = $usage / $total
    define flag(q){
      if (q < benchmark) return $FALSE
      return $TRUE
    }
    flag(quotient)
EOF
`
  echo $_is_high
}
