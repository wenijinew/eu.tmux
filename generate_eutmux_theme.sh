#!/usr/bin/env bash

THEME_ROOT="${WS_ROOT}/.themes"
PALETTE_ROOT="${THEME_ROOT}/palettes"
mkdir -p ${PALETTE_ROOT}

function _warn(){
    echo -e "\033[93mWARNING:\033[0m ${1}"
}

function generate(){
    if [ -z "${GITHUB_REPO_ROOT}" ];then
      _warn "The environment variable 'GITHUB_REPO_ROOT' is not set!"
      return $EXIT_ABNORMAL
    fi
    local eutmux_script=${GITHUB_REPO_ROOT}/eu.tmux/eutmux.tmux
    if [ ! -x ${eutmux_script} ];then
        _warn "Not found ${eutmux_script}"
        return $EXIT_ABNORMAL
    fi

    local palette_name="${1:-emacs-viiv-random-daylight-88}"
    local target_ide="${2:-emacs}"
    if [[ -n "${palette_name}" ]];then
        local palette_filepath="${PALETTE_ROOT}/${palette_name}.palette"
        for ide in vim nvim emacs vscode; do
            if [[ ( -n "${target_ide}" ) && ( "${ide}" != "${target_ide}" ) ]];then
                continue
            fi
            palette_filepath="${PALETTE_ROOT}/${palette_name}.palette"
            if [[ -f "${palette_filepath}" && -r "${palette_filepath}" ]];then
                ${eutmux_script}  -d -p "${palette_filepath}"
                ${eutmux_script}  -T "${target_ide}"
            else
                _warn "Not found ${palette_filepath}"
            fi
        done
    else
        ${eutmux_script} -d
    fi
}

generate $@ >/dev/null 2>/dev/null
