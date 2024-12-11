#!/usr/bin/env python3
"""Provide utilities functions."""
import shlex
import subprocess
from subprocess import TimeoutExpired

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
    with subprocess.Popen(
        command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        try:
            outs, errs = process.communicate(timeout=3)
        except TimeoutExpired:
            process.kill()
            outs, errs = process.communicate()
            raise TimeoutExpired
    output = outs.decode().strip()
    return output if output and len(output) > 0 else default_output


if __name__ == "__main__":
    value = get_tmux_option("@eutmux_base_color_total", 5)
    print(value)
