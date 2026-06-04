#!/usr/bin/env python3
"""Import terminal theme colors into eu.tmux theme format.

Reads Alacritty TOML, Kitty conf, or raw hex pairs and generates
a eu.tmux .theme.yaml file.

Usage:
    python3 theme-import.py --from alacritty ~/.config/alacritty/alacritty.toml --name my-theme
    python3 theme-import.py --from kitty ~/.config/kitty/current-theme.conf --name my-theme
    python3 theme-import.py --bg "#1a1a2e" --fg "#eaeaea" --name my-theme
"""
import argparse
import sys
from pathlib import Path

import yaml

THEMES_DIR = Path(__file__).parent.parent / "themes"
TEMPLATE_THEME = THEMES_DIR / "template.theme.yaml"


def extract_from_alacritty(config_path: str) -> dict:
    """Extract bg/fg from Alacritty TOML config.

    Args:
        config_path: Path to alacritty.toml.

    Returns:
        Dict with 'bg' and 'fg' hex colors.
    """
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    with open(config_path, "rb") as file_handle:
        config = tomllib.load(file_handle)

    primary = config.get("colors", {}).get("primary", {})
    return {
        "bg": primary.get("background", "#1a1a2e"),
        "fg": primary.get("foreground", "#eaeaea"),
    }


def extract_from_kitty(config_path: str) -> dict:
    """Extract bg/fg from Kitty theme conf.

    Args:
        config_path: Path to kitty theme file.

    Returns:
        Dict with 'bg' and 'fg' hex colors.
    """
    colors = {"bg": "#1a1a2e", "fg": "#eaeaea"}
    with open(config_path) as file_handle:
        for line in file_handle:
            line = line.strip()
            if line.startswith("background"):
                colors["bg"] = line.split()[-1]
            elif line.startswith("foreground"):
                colors["fg"] = line.split()[-1]
    return colors


def generate_theme_yaml(theme_name: str, colors: dict) -> str:
    """Generate eu.tmux theme YAML from colors.

    Args:
        theme_name: Name for the new theme.
        colors: Dict with 'bg' and 'fg'.

    Returns:
        YAML string for the theme file.
    """
    # Load template as base
    if TEMPLATE_THEME.exists():
        with open(TEMPLATE_THEME) as file_handle:
            template = yaml.safe_load(file_handle)
    else:
        template = {}

    template["terminal"] = {"bg": colors["bg"], "fg": colors["fg"]}
    return yaml.dump(template, default_flow_style=False, sort_keys=False)


def main():
    """Parse args and import theme."""
    parser = argparse.ArgumentParser(description="Import terminal theme into eu.tmux")
    parser.add_argument("--name", required=True, help="Output theme name")
    parser.add_argument("--from", dest="source", choices=["alacritty", "kitty"],
                        help="Source format")
    parser.add_argument("config_file", nargs="?", help="Source config file path")
    parser.add_argument("--bg", help="Background hex color")
    parser.add_argument("--fg", help="Foreground hex color")
    args = parser.parse_args()

    # Extract colors
    if args.bg and args.fg:
        colors = {"bg": args.bg, "fg": args.fg}
    elif args.source and args.config_file:
        extractors = {"alacritty": extract_from_alacritty, "kitty": extract_from_kitty}
        colors = extractors[args.source](args.config_file)
    else:
        parser.error("Provide --bg/--fg or --from <format> <config-file>")
        sys.exit(1)

    # Generate and write
    theme_yaml = generate_theme_yaml(args.name, colors)
    output_file = THEMES_DIR / f"{args.name}.theme.yaml"
    output_file.write_text(theme_yaml)
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
