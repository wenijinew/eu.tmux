#!/usr/bin/env python3
"""Provide utilities functions."""
import shlex
import subprocess

from const import EMPTY, UTF_8


def get_tmux_option(option_name, default_value):
    """Read tmux option."""
    assert option_name is not None, "option_name is None!"
    assert default_value is not None, "default_value is None!"

    if not option_name.startswith("@"):
        option_name = f"@{option_name}"
    shell_cmd = f'tmux show-option -gqv "{option_name}"'
    return run_shell_command(shell_cmd, default_value)


def run_shell_command(command, default_output=None):
    """Run shell command."""
    command_args = shlex.split(command)
    value = subprocess.check_output(command_args, shell=False).decode(UTF_8).strip()
    if value is not None and value.strip() != EMPTY:
        return value
    return default_output
