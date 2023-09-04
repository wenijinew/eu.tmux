#!/usr/bin/env bash
_DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="${_DIR}:${PATH}"

PLACE_HOLDERS=("LIGHT_RED" "MIDDLE_RED" "DARK_RED" "LIGHT_GREEN" "MIDDLE_GREEN" "DARK_GREEN" "LIGHT_GRAY" "MIDDLE_GRAY" "DARK_GRAY")

palette=$(python3 -c "import palette; palette = palette.create_theme_palette(); print(palette)")
tmpfile=$(mktemp)
colors=$(echo $palette | grep -iEo '#[[:alnum:]]{6}' > ${tmpfile})

dynamic_theme_name=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)
dynamic_theme_name="dynamic"
tmux set-option -gq "@dynamic_theme_name" "${dynamic_theme_name}"
dynamic_theme_file_name="${dynamic_theme_name}.theme.yaml"
if [ -e "${dynamic_theme_file_name}" ];then
    rm -f "${dynamic_theme_file_name}"
fi
cp "template.theme.yaml" "${dynamic_theme_file_name}"
# trap "rm -f ${dynamic_theme_file_name}" EXIT INT TERM

index=1
while read -r _color;do
    sed -i "s/${PLACE_HOLDERS[$index]}/${_color}/g" "${dynamic_theme_file_name}"
    ((index++))
done < "${tmpfile}"

source violet.tmux
