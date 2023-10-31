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
<<<<<<< HEAD
    result = (
        subprocess.popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    )
    if result.returncode != 0:
        return default_output
    else:
        return result.stdout.strip()
=======
    value = (
        subprocess.check_output(command_args, shell=False)
        .decode(UTF_8)
        .strip()
    )
    if value is not None and value.strip() != EMPTY:
        return value
    return default_output
>>>>>>> 207f932d2953bff5e20b53c65bbfd3466adf9f9a
