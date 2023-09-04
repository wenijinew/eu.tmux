#!/usr/bin/env bash
_DIR="$(cd "$(dirname "$0")" && pwd)"
main(){
    export PATH="${_DIR}:${PATH}"
    export PYTHONPATH="${_DIR}:${PATH}"
    find ${_DIR} -name "*.sh" -exec chmod u+x '{}' \;
    tmux set-environment -g 'PATH' "${_DIR}:${PATH}"
    tmux set-environment -g 'PYTHONPATH' "${_DIR}:${PATH}"
    tmux bind-key g "run 'python -c \"import palette; palettes = palette.generate_palette(); print(palettes)\"'"
    tmux_commands="$(python3 -c "import violet; tmux_commands = violet.violet(); print(tmux_commands)")"
    tmp_conf=$(mktemp)
    echo "${tmux_commands}" | sed -e 's/True/on/g' | sed -e 's/False/off/g' | tr ';' '\n' > "${tmp_conf}"
    tmux source "${tmp_conf}"
}

main
