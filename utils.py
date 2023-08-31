#!/usr/bin/env python3
"""Provide utility functions for Tmux option reading and writing."""

import shlex
import subprocess

from loguru import logger


def read_tmux_option(option, default_value):
    """Read tmux option."""
    shell_cmd = f'tmux show-option -gqv "{option}"'
    try:
        shell_cmd_args = shlex.split(shell_cmd)
        value = subprocess.check_output(shell_cmd_args, shell=False)
    except Exception as err:
        logger.opt(exception=True).debug(
            f"{shell_cmd} is failed to run. use\
                                         {default_value} for {option}"
        )
        value = default_value
    return value
