#!/usr/bin/env python3
"""Palette and Colors."""

import colorsys
import random

from utils import get_format


def hex2hls(hex_color):
    """ "Convert."""
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
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert."""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def get_scheme_colors(hex_color, n_colors=7):
    """ "Convert."""
    assert hex_color is not None, "Invalid argument: hex_color is None."
    assert (
        n_colors is not None and isinstance(n_colors, int) and n_colors > 0
    ), f"Invalid argument: n_colors = {n_colors}"
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in range(0, 360, 360 // n_colors):
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    return [hls2hex(hls_color) for hls_color in triadic_colors][0:n_colors]


def padding(num, target_length):
    """
    Padding left for number to make it's string format length reaches the target length.

    This is mainly used to construct valid hex color number in R,G,B
    position. Example, if the given num is a hex number 0xf and the
    target length is 2, then the padding result is 0f.
    """
    str_num = str(num)
    if str_num.startswith("0x"):
        str_num = str_num[2:]
    if len(str_num) < target_length:
        str_num = (
            f"{''.join(['0' for i in range(target_length - len(str_num))])}{str_num}"
        )
    return str_num


def lighter(base_color, n_color):
    """Given base color, return 'n' color hex codes from base color to lightest
    color."""
    color_rgb = tuple(int(base_color[1:][i : i + 2], 16) for i in (0, 2, 4))
    color_rgb_ligher = tuple(
        [c for c in range(color, 255, (255 - color) // n_color)][0:n_color]
        for color in color_rgb
    )

    lighter_colors = [
        f"#{''.join(tuple(padding(hex(color_ligher[index]), 2) for color_ligher in color_rgb_ligher))}"
        for index in range(0, n_color)
    ]

    return lighter_colors


def random_color(
    min_color=0,
    max_color=231,
    eutmux_base_color_total=7,
    eutmux_light_color_total=24,
):
    """
    Generate random color hex codes.

    Firstly, it will generate random integer from min_color (0-(255 - eutmux_light_color_total - 1)) to max_color (0-(255 - eutmux_light_color_total)).
    The max_color should be less than (255 - eutmux_light_color_total) because it needs the room to generate lighter colors.

    To generate darker colors, use smaller value for max_color.
    To generate ligher colors, use bigger value for min_color.

    It's recommended to use default values.
    If you want to make change, please make sure what you are doing.

    Secondly, it will generate 'eutmux_light_color_total' different hex color codes from base color to the lightest color.
    Note that 'eutmux_light_color_total' includes base color also. It means it will generate 'eutmux_light_color_total - 1' lighter colors besides base color.

    Parameters:
        min_color - minimum color code. default: 0.
        max_color - maximum color code. default: 254.
        eutmux_base_color_total - how many base colors to generate. default: 7.
        eutmux_light_color_total - how many lighter colors to generate. default: 24.
        plot: True to plot the generated color. Otherwise, False. default: False.

    Retrun:
        Generated random base colors and all lighter colors of each base color.
        The returned value is a two-dimention list. First dimention length is the value of eutmux_base_color_total. Second dimention length is eutmux_light_color_total.
    """

    random_int = random.randint(0, 15**6)
    _min = min_color
    _max = max_color
    random_color_code = "#"
    for counter in range(0, 3):
        random_int = random.randint(_min, _max)
        random_color = padding(hex(random_int), 2)
        random_color_code = random_color_code + random_color

    base_colors = get_scheme_colors(random_color_code, eutmux_base_color_total)[
        0:eutmux_base_color_total
    ]

    random_colors = []
    for base_color in base_colors:
        lighter_colors = lighter(base_color, eutmux_light_color_total)
        random_colors.append(lighter_colors)

    return random_colors


class Palette:
    """Generate palette colors."""

    def __init__(self):
        # random colors are used for sections, components, and pieces
        self.eutmux_base_color_total = get_format("@eutmux_base_color_total", 5)
        self.eutmux_light_color_total = get_format("@eutmux_light_color_total", 6)

    def generate_palette_colors(self):
        """
        Generate random palette.

        6 group base colors: 5 base colors + dark gray color. echo base
        color has 6 different colors from dark to light. placeholders
        are from light to dark, so need to reverse the order.
        """
        random_colors = random_color(
            max_color=200,
            eutmux_base_color_total=self.eutmux_base_color_total,
            eutmux_light_color_total=self.eutmux_light_color_total,
        )
        # dark colors are used for status-line
        dark_colors = random_color(
            max_color=30, eutmux_base_color_total=1, eutmux_light_color_total=6
        )
        random_colors.extend(dark_colors)
        for r_colors in random_colors:
            r_colors.reverse()
        return [color for r_colors in random_colors for color in r_colors]

    def generate_palette(self):
        """
        Generate palette content.

        Palette contains a list of colors. Each color is a pair of color
        name and color code.
        The format is "C_[base color sequence]_[colormap sequence]".

        For example, "C_1_1":"#8f67ff".

        Note:
        The 'base color sequence' starts from 1 to @eutmux_base_color_total (not
        included)
        The 'colormap sequence' starts from 0 to @eutmux_light_color_total (not
        included)
        When "colormap sequence" is 0, then it represents the lightest color.

        One continuous colormap is for one base color and consists of a
        group of colors from lightest color to the base color.

        Return:
        A list of palette colors.
        """
        palette_color_codes = self.generate_palette_colors()
        base_color_sequence = 0
        colormap_sequence = 0
        palette_colors = []
        for index, color in enumerate(palette_color_codes):
            colormap_sequence = index % self.eutmux_light_color_total
            if colormap_sequence == 0:
                base_color_sequence += 1
            color_name = f"C_{base_color_sequence}_{colormap_sequence}"
            palette_colors.append(f"{color_name}:{color}")
        return palette_colors


def generate_palette():
    """Generate palette colors."""
    return Palette().generate_palette()


def main():
    """Test."""
    palette = Palette()
    for counter in range(9):
        r_colors = random_color(max_color=100)
        print(r_colors)
    print(palette.generate_palette())


if __name__ == "__main__":
    main()
