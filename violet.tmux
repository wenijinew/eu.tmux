#!/usr/bin/env bash
_DIR="$(cd "$(dirname "$0")" && pwd)"
main(){
  export PATH="${_DIR}:${PATH}"
  find ${_DIR} -name "*.sh" -exec chmod u+x '{}' \;
  tmux set-environment -g PATH "${_DIR}:${PATH}"
  commands="$(python3 -c "import violet; commands = violet.violet(); print(commands)")"
  tmp_conf=$(mktemp)
  echo "${commands}" | sed -e 's/True/on/g' | sed -e 's/False/off/g' | tr ';' '\n' > "${tmp_conf}"
  tmux source "${tmp_conf}"
}

main
