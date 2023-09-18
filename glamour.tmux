#!/usr/bin/env bash
_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${_DIR}/utils.sh"

TMUX_COMMANDS_FILENAME="tmux_commands.txt"
DEFAULT_PALETTE_FILENAME="default_palette.txt"
DYNAMIC_PALETTE_FILENAME="dynamic_palette.txt"
TEMPLATE_THEME_FILENAME="template.theme.yaml"
DEFAULT_CONFIG_FILENAME="glamour.yaml"
DYNAMIC_THEME_NAME="dynamic"
PALETTE_FILENAME="${DEFAULT_PALETTE_FILENAME}"

PLACE_HOLDERS=(
    "PALE_RED"
    "LIGHT_RED"
    "MIDDLE_RED"
    "STRONG_RED"
    "DARK_RED"
    "DEEP_RED"
    "PALE_PURPLE"
    "LIGHT_PURPLE"
    "MIDDLE_PURPLE"
    "STRONG_PURPLE"
    "DARK_PURPLE"
    "DEEP_PURPLE"
    "PALE_ORANGE"
    "LIGHT_ORANGE"
    "MIDDLE_ORANGE"
    "STRONG_ORANGE"
    "DARK_ORANGE"
    "DEEP_ORANGE"
    "PALE_GREEN"
    "LIGHT_GREEN"
    "MIDDLE_GREEN"
    "STRONG_GREEN"
    "DARK_GREEN"
    "DEEP_GREEN"
    "PALE_BLUE"
    "LIGHT_BLUE"
    "MIDDLE_BLUE"
    "STRONG_BLUE"
    "DARK_BLUE"
    "DEEP_BLUE"
    "PALE_GRAY"
    "LIGHT_GRAY"
    "MIDDLE_GRAY"
    "STRONG_GRAY"
    "DARK_GRAY"
    "DEEP_GRAY"
)

# function to replace legacy solution's placeholders with new solutions color
# name of palette colors
replace_legacy_placeholders(){
    index=0
    base_color_index=0
    for placeholder in "${PLACE_HOLDERS[@]}"
    do
        colormap_index="$(echo "${index} % 6" | bc)"
        if [ "${colormap_index}" -eq 0 ];then
           ((base_color_index++))
        fi
        color_name="C_${base_color_index}_${colormap_index}"

        find "${_DIR}" -maxdepth 1 -type f -exec sed -i "s/${placeholder}/${color_name}/g" '{}' \;
        sed -i "s/${placeholder}/${color_name}/g" "$HOME/.config/tmux/glamour.yaml"

        ((index++))
    done
}

# call python module to generate palette file
generate_palette_colors(){
    palette=$(python3 -c "import palette; palette = palette.generate_palette(); print(palette)")
    echo "$palette" | grep -iEo 'C(_[[:digit:]]{1,}){2}\:#[[:alnum:]]{6}' > "${DYNAMIC_PALETTE_FILENAME}"
}

create_dynamic_theme_file(){
    dynamic_theme_file_name="${DYNAMIC_THEME_NAME}.theme.yaml"
    tmux set-option -gq "@dynamic_theme_name" "${DYNAMIC_THEME_NAME}"
    if [ -e "${dynamic_theme_file_name}" ];then
       rm -f "${dynamic_theme_file_name}"
    fi
    cp "${TEMPLATE_THEME_FILENAME}" "${dynamic_theme_file_name}"
    replace_color "${dynamic_theme_file_name}"
}

create_dynamic_config_file(){
    dynamic_config_file_name="${DYNAMIC_THEME_NAME}.glamour.yaml"
    tmux set-option -gq "@dynamic_config_file_name" "${dynamic_config_file_name}"
    if [ -e "${dynamic_config_file_name}" ];then
        rm -f "${dynamic_config_file_name}"
    fi

    # use customized config file is exists
    config_file="${DEFAULT_CONFIG_FILENAME}"
    CONFIG_PATH="${XDG_CONFIG_HOME:-${HOME}}/.config"
    _config_file="${CONFIG_PATH}/tmux/${DEFAULT_CONFIG_FILENAME}"
    if [ -e "${_config_file}" ];then
       config_file="${_config_file}"
    fi

    cp "${config_file}" "${dynamic_config_file_name}"
    replace_color "${dynamic_config_file_name}"
}

replace_color(){
    target_file="${1}"
    palette_file="${2:-${PALETTE_FILENAME}}"
    while read -r _color;do
          color_name="$(echo "${_color}" | cut -d':' -f1)"
          color_value="$(echo "${_color}" | cut -d':' -f2)"
          sed -i "s/${color_name}/${color_value}/g" "${target_file}"
    done < "${palette_file}"
}

main(){
    if [ -z "${TMUX}" ];then
       _warn "Not in Tmux."
       exit "${E_ABNORMAL_STATE}"
    fi
    if [ ! "$(which pip)" ] ; then
        _warn "Python Environment:\t CHECK FAILED. 'pip' command not found."
        exit "$E_ABNORMAL_STATE"
    fi
    test -e "${_DIR}/.requirements.installed.txt"
    is_installed=$?
    is_latest=$FALSE
    if [ ${is_installed} -eq $TRUE ];then
       diff "${_DIR}/.requirements.installed.txt" "${_DIR}/requirements.txt" >/dev/null 2>/dev/null
       is_latest=$?
    fi
    if [[ $is_installed -ne $TURE || $is_latest -ne $TRUE ]];then
       env pip install -q -r "${_DIR}/requirements.txt" 2>/dev/null
       cp "${_DIR}/requirements.txt" "${_DIR}/.requirements.installed.txt"
    fi
    if [ $? -ne $TRUE ];then
       _warn "Python Environment:\t Dependencies Installation Failure."
    fi

    if [ "$CREATE_DYNMIC_THEME" -eq $TRUE ];then
       PALETTE_FILENAME=${DYNAMIC_PALETTE_FILENAME}
       generate_palette_colors
       create_dynamic_theme_file
    else
        tmux set-option -gq "@dynamic_theme_name" ""
    fi
    create_dynamic_config_file

    export PATH="${_DIR}:${PATH}"
    export PYTHONPATH="${_DIR}:${PATH}"
    find "${_DIR}" -name "*.sh" -exec chmod u+x '{}' \;
    tmux set-environment -g 'PATH' "${_DIR}:${PATH}"
    tmux set-environment -g 'PYTHONPATH' "${_DIR}:${PATH}"
    tmux_commands="$(python3 -c "import glamour; tmux_commands = glamour.glamour(); print(tmux_commands)")"
    echo "${tmux_commands}" | sed -e 's/True/on/g' | sed -e 's/False/off/g' | tr ';' '\n' > "${TMUX_COMMANDS_FILENAME}"
    tmux source "${TMUX_COMMANDS_FILENAME}"
}

usage(){
    echoh "./glamour.tmux [-d]"
}

CREATE_DYNMIC_THEME=${FALSE}

while getopts "dr" opt; do
    case $opt in
        d) CREATE_DYNMIC_THEME=${TRUE} ;;
        r) replace_legacy_placeholders; exit $? ;;
        *) usage ;;
    esac
done

main
