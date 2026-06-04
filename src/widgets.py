#!/usr/bin/env python3
"""Widget system for eu.tmux — composable status bar modules.

Reads widget configuration from eutmux.yaml and assembles status-left/right
from individual widget scripts. Each widget is a script that outputs formatted
tmux status text.

Widget spec in eutmux.yaml:
    widgets:
      status_right:
        - name: git_branch
          script: widgets/git_branch.sh
          interval: 5
        - name: k8s_context
          script: widgets/k8s_context.sh
        - name: clock
          format: "%H:%M"
      separator: " │ "
"""
import os
import subprocess
import sys
from pathlib import Path

import yaml

WIDGETS_DIR = Path(__file__).parent.parent / "widgets"
CONFIG_SEARCH_PATHS = [
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "eutmux",
    Path(__file__).parent.parent,
]


def load_widget_config() -> dict:
    """Load widget configuration from eutmux.yaml.

    Returns:
        Widget config dict, or empty dict if not configured.
    """
    for config_dir in CONFIG_SEARCH_PATHS:
        config_file = config_dir / "eutmux.yaml"
        if config_file.exists():
            with open(config_file) as file_handle:
                config = yaml.safe_load(file_handle)
                return config.get("widgets", {})
    return {}


def resolve_widget_script(widget_entry: dict) -> Path | None:
    """Resolve widget script path from widget entry.

    Args:
        widget_entry: Widget dict with 'name' and optional 'script' keys.

    Returns:
        Resolved Path to script, or None if not found.
    """
    # Explicit script path
    if "script" in widget_entry:
        script_path = Path(widget_entry["script"])
        if script_path.is_absolute() and script_path.exists():
            return script_path
        resolved_path = WIDGETS_DIR / script_path
        if resolved_path.exists():
            return resolved_path

    # Convention: widgets/<name>.sh
    widget_name = widget_entry.get("name", "")
    convention_path = WIDGETS_DIR / f"{widget_name}.sh"
    if convention_path.exists():
        return convention_path

    return None


def execute_widget(widget_entry: dict) -> str:
    """Execute a single widget and return its output.

    Args:
        widget_entry: Widget configuration dict.

    Returns:
        Formatted widget output string, or empty string on failure.
    """
    # Built-in format widgets (no script needed)
    if "format" in widget_entry and "script" not in widget_entry:
        return widget_entry["format"]

    script_path = resolve_widget_script(widget_entry)
    if not script_path:
        return ""

    try:
        result = subprocess.run(
            [str(script_path)],
            capture_output=True, text=True, timeout=3,
            env={**os.environ, **widget_entry.get("env", {})},
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        return ""


def assemble_status(position: str = "status_right") -> str:
    """Assemble status string from configured widgets.

    Args:
        position: 'status_left' or 'status_right'.

    Returns:
        Concatenated widget outputs with separator.
    """
    widget_config = load_widget_config()
    if not widget_config:
        return ""

    widget_list = widget_config.get(position, [])
    separator = widget_config.get("separator", " │ ")

    widget_outputs = []
    for widget_entry in widget_list:
        output = execute_widget(widget_entry)
        if output:
            widget_outputs.append(output)

    return separator.join(widget_outputs)


if __name__ == "__main__":
    position_argument = sys.argv[1] if len(sys.argv) > 1 else "status_right"
    assembled_status = assemble_status(position_argument)
    print(assembled_status)
