#!/usr/bin/env python3
"""Palette and Colors"""

import colorsys
import random

import seaborn as sns


def hex2hls(hex_color):
    """ "Convert"""
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(
        normalized_rgb[0], normalized_rgb[1], normalized_rgb[2]
    )
    return hls_color


def hls2hex(hls_color):
    """ "Convert"""
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert"""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def get_triadic_colors(hex_color):
    """ "Convert"""
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in [120.0, 240.0]:
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    return [hls2hex(hls_color) for hls_color in triadic_colors]


def generate_random_colors(
    n_colors=1, hue=None, saturation=None, lightness=None
):
    """Generate random colors. By default, dark colors."""
    dark_colors = []
    for _i in range(n_colors):
        # Vary the hue from 0 to 1
        # Set the saturation to a constant value (0.5 for moderate saturation)
        # Vary the lightness from 0.2 to 0.5 for dark colors

        hue = hue or random.random()
        saturation = saturation or 0.5
        lightness = lightness or (0.2 + hue * 0.3)

        hex_color = hls2hex((hue, lightness, saturation))
        dark_colors.append(hex_color)
    return dark_colors


def generate_random_dark_red(n_colors=1):
    """Generate random dark red colors"""
    hue = random.randint(300, 360) / 360
    saturation = random.randint(75, 100) / 100
    lightness = random.randint(15, 40) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_dark_black(n_colors=1):
    """Generate random dark black/gray/blue colors"""
    hue = random.randint(230, 250) / 360
    saturation = random.randint(75, 100) / 100
    lightness = random.randint(0, 15) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_dark_green(n_colors=1):
    """Generate random dark green colors"""
    hue = random.randint(50, 190) / 360
    saturation = random.randint(60, 100) / 100
    lightness = random.randint(10, 20) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_palette(n_palette=1):
    """ "Convert"""

    all_palettes = []
    for _i in range(n_palette):
        palette = []

        dark_red = generate_random_dark_red()
        dark_green = generate_random_dark_green()
        dark_black = generate_random_dark_black()
        for dark_color in [
            c for dark in (dark_red, dark_green, dark_black) for c in dark
        ]:
            _colors = sns.color_palette(f"light:{dark_color}", n_colors=3)
            palette.extend(_colors.as_hex())

        all_palettes.append(palette)

    return all_palettes


def create_theme_palette():
    """Create palette for theme.

    Returned 9 colors:
        light red, red, dark red; light green, green, dark green, light gray,
        gray, dark gray.
    """
    return generate_palette()[0]


def main():
    """Test"""
    all_palettes = generate_palette(1)
    print(all_palettes)


if __name__ == "__main__":
    main()
