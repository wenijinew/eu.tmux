#!/usr/bin/env python3
"""Export eu.tmux theme colors to terminal emulator configs.

Supports: Alacritty (TOML), Kitty (conf), Windows Terminal (JSON).

Usage:
    python3 theme-export.py <theme-name> [--format alacritty|kitty|wt]
"""
import argparse
import sys
from pathlib import Path

import yaml

THEMES_DIR = Path(__file__).parent.parent / "themes"


def load_theme_colors(theme_name: str) -> dict:
    """Load color definitions from a theme YAML file.

    Args:
        theme_name: Theme name (without extension).

    Returns:
        Dict with color keys (bg, fg, accent, etc.).

    Raises:
        FileNotFoundError: If theme file doesn't exist.
    """
    theme_file = THEMES_DIR / f"{theme_name}.theme.yaml"
    if not theme_file.exists():
        raise FileNotFoundError(f"Theme not found: {theme_file}")

    with open(theme_file) as file_handle:
        theme_data = yaml.safe_load(file_handle)

    terminal_colors = theme_data.get("terminal", {})
    return {
        "background": terminal_colors.get("bg", "#1a1a2e"),
        "foreground": terminal_colors.get("fg", "#eaeaea"),
    }


def export_alacritty(colors: dict) -> str:
    """Generate Alacritty TOML color config.

    Args:
        colors: Dict with background/foreground colors.

    Returns:
        TOML string for alacritty.toml.
    """
    return f"""[colors.primary]
background = "{colors['background']}"
foreground = "{colors['foreground']}"
"""


def export_kitty(colors: dict) -> str:
    """Generate Kitty color config.

    Args:
        colors: Dict with background/foreground colors.

    Returns:
        Kitty conf string.
    """
    return f"""background {colors['background']}
foreground {colors['foreground']}
"""


def export_windows_terminal(colors: dict) -> str:
    """Generate Windows Terminal JSON color scheme.

    Args:
        colors: Dict with background/foreground colors.

    Returns:
        JSON string for Windows Terminal settings.
    """
    import json
    scheme = {
        "name": "eu.tmux",
        "background": colors["background"],
        "foreground": colors["foreground"],
    }
    return json.dumps(scheme, indent=2)


def main():
    """Parse args and export theme to specified format."""
    parser = argparse.ArgumentParser(description="Export eu.tmux theme to terminal config")
    parser.add_argument("theme", help="Theme name")
    parser.add_argument("--format", "-f", choices=["alacritty", "kitty", "wt"],
                        default="alacritty", help="Output format")
    args = parser.parse_args()

    try:
        colors = load_theme_colors(args.theme)
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

    exporters = {
        "alacritty": export_alacritty,
        "kitty": export_kitty,
        "wt": export_windows_terminal,
    }
    print(exporters[args.format](colors))


if __name__ == "__main__":
    main()
