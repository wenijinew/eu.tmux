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
    print(rgb_color)
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert"""
    scaled_rgb = rgb_color
    if rgb_color[0].isinstance(float):
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
    print(triadic_colors)
    return [hls2hex(hls_color) for hls_color in triadic_colors]


def get_random_dark_colors(n_colors, min_rgb=0, max_rgb=100):
    """ "Convert"""
    dark_colors = []
    for _i in range(n_colors):
        _r = random.randint(min_rgb, max_rgb)
        _g = random.randint(min_rgb, max_rgb)
        _b = random.randint(min_rgb, max_rgb)
        dark_colors.append(rgb2hex((_r, _g, _b)))
    return dark_colors


def generate_palette(n_palette=1):
    """ "Convert"""
    all_palettes = []
    for color in get_random_dark_colors(n_palette):
        color2, color3 = get_triadic_colors(color)
        colors = (color, color2, color3)
        palette = []
        for _c in colors:
            c_colors = sns.color_palette(f"light:{_c}", n_colors=3)
            palette.extend(c_colors.as_hex())
        all_palettes.append(palette)

    return all_palettes
