#!/usr/bin/env python3
"""Provide utilities functions."""
import shlex
import subprocess

UTF_8 = "utf-8"
EMPTY = ""


def get_tmux_option(name, default_value):
    """Read tmux option."""
    assert name is not None, "name is None!"
    assert default_value is not None, "default_value is None!"

    if not name.startswith("@"):
        name = f"@{name}"
    shell_cmd = f'tmux show-option -gqv "{name}"'
    return run_shell_command(shell_cmd, default_value)


def run_shell_command(command, default_output=None):
    """Run shell command."""
    command_args = shlex.split(command)
    result = (
        subprocess.popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    )
    if result.returncode != 0:
        return default_output
    else:
        return result.stdout.strip()