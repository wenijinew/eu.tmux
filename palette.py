#!/usr/bin/env python3
"""Palette and Colors."""

import colorsys
import random

import seaborn as sns

from log import logger


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
    """ "Convert."""
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


def get_triadic_colors(hex_color, n_colors=7):
    """ "Convert."""
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in range(0, 360, 360 // n_colors):
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    return [hls2hex(hls_color) for hls_color in triadic_colors]


def generate_random_colors(n_colors=1, hue=None, saturation=None, lightness=None):
    """
    Generate random colors.

    By default, dark colors.
    """
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


def generate_random_red(n_colors=1, lightness=15):
    """Generate random dark red colors."""
    lightness_min = lightness or 15
    lightness_max = lightness_min + 25
    hue = random.randint(0, 20) / 360
    saturation = random.randint(75, 100) / 100
    lightness = random.randint(lightness_min, lightness_max) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_orange(n_colors=1, lightness=10):
    """Generate random dark orange colors."""
    lightness_min = lightness or 10
    lightness_max = lightness_min + 10
    hue = random.randint(20, 60) / 360
    saturation = random.randint(60, 100) / 100
    lightness = random.randint(lightness_min, lightness_max) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_purple(n_colors=1, lightness=20):
    """Generate random dark orange colors."""
    lightness_min = lightness or 20
    lightness_max = lightness_min + 20
    hue = random.randint(270, 330) / 360
    saturation = random.randint(60, 100) / 100
    lightness = random.randint(lightness_min, lightness_max) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_black(n_colors=1, lightness=0):
    """Generate random dark black/gray/blue colors."""
    lightness_min = lightness or 0
    lightness_max = lightness_min + 5
    hue = random.randint(1, 30) / 36
    saturation = 1
    lightness = random.randint(lightness_min, lightness_max) / 100

    logger.debug(f"generate_random_black: ({hue}, {saturation}, {lightness})")
    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_blue(n_colors=1, lightness=0):
    """Generate random dark black/gray/blue colors."""
    lightness_min = lightness or 0
    lightness_max = lightness_min + 15
    hue = random.randint(180, 240) / 360
    saturation = random.randint(75, 100) / 100
    lightness = random.randint(lightness_min, lightness_max) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def generate_random_green(n_colors=1, lightness=10):
    """Generate random dark green colors."""
    lightness_min = lightness or 10
    lightness_max = lightness_min + 10
    hue = random.randint(90, 150) / 360
    saturation = random.randint(60, 100) / 100
    lightness = random.randint(lightness_min, lightness_max) / 100

    return generate_random_colors(n_colors, hue, saturation, lightness)


def _generate_palette(n_palette=1, lightness=None):
    """Convert."""

    n_colors = 24
    groups = 6
    counts = n_colors / groups
    all_palettes = []
    for _i in range(n_palette):
        palette = []

        red = generate_random_red(lightness=lightness)
        purple = generate_random_purple(lightness=lightness)
        orange = generate_random_orange(lightness=lightness)
        green = generate_random_green(lightness=lightness)
        blue = generate_random_blue(lightness=lightness)
        black = generate_random_black(lightness=lightness)
        for dark_color in [
            c
            for dark in (
                red,
                purple,
                orange,
                green,
                blue,
                black,
            )
            for c in dark
        ]:
            _colors = sns.color_palette(f"light:{dark_color}", n_colors=n_colors)
            _colors_hex = _colors.as_hex()
            _picked_colors_index = [
                c + (counts - 1) for c in range(n_colors) if c % counts == 0
            ]
            _picked_colors = [_colors_hex[int(index)] for index in _picked_colors_index]
            palette.extend(_picked_colors)

        all_palettes.append(palette)

    return all_palettes


def create_theme_palette():
    """
    Create palette for theme.

    Returned 9 colors:     light red, red, dark red; light green, green,
    dark green, light gray,     gray, dark gray.
    """
    return generate_palette()[0]


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
    base_colors_total=7,
    lighter_colors_total=24,
):
    """
    Generate random color hex codes.

    Firstly, it will generate random integer from min_color (0-(255 - lighter_colors_total - 1)) to max_color (0-(255 - lighter_colors_total)).
    The max_color should be less than (255 - lighter_colors_total) because it needs the room to generate lighter colors.

    To generate darker colors, use smaller value for max_color.
    To generate ligher colors, use bigger value for min_color.

    It's recommended to use default values.
    If you want to make change, please make sure what you are doing.

    Secondly, it will generate 'lighter_colors_total' different hex color codes from base color to the lightest color.
    Note that 'lighter_colors_total' includes base color also. It means it will generate 'lighter_colors_total - 1' lighter colors besides base color.

    Parameters:
        min_color - minimum color code. default: 0.
        max_color - maximum color code. default: 254.
        base_colors_total - how many base colors to generate. default: 7.
        lighter_colors_total - how many lighter colors to generate. default: 24.
        plot: True to plot the generated color. Otherwise, False. default: False.

    Retrun:
        Generated random base colors and all lighter colors of each base color.
        The returned value is a two-dimention list. First dimention length is the value of base_colors_total. Second dimention length is lighter_colors_total.
    """

    random_int = random.randint(0, 15**6)
    _min = min_color
    _max = max_color
    random_color_code = "#"
    for c in range(0, 3):
        random_int = random.randint(_min, _max)
        random_color = padding(hex(random_int), 2)
        random_color_code = random_color_code + random_color

    base_colors = get_triadic_colors(random_color_code, base_colors_total)[
        0:base_colors_total
    ]

    random_colors = []
    for base_color in base_colors:
        lighter_colors = lighter(base_color, lighter_colors_total)
        random_colors.append(lighter_colors)

    return random_colors


def generate_palette():
    """
    Generate random palette.

    6 group base colors: 5 base colors + dark gray color. echo base
    color has 6 different colors from dark to light. placeholders are
    from light to dark, so need to reverse the order.
    """
    random_colors = random_color(
        max_color=100, base_colors_total=5, lighter_colors_total=6
    )
    gray_colors = random_color(
        max_color=30, base_colors_total=1, lighter_colors_total=6
    )
    random_colors.extend(gray_colors)
    for r_colors in random_colors:
        r_colors.reverse()
    return [color for r_colors in random_colors for color in r_colors]


def main():
    """Test."""
    for c in range(9):
        r_colors = random_color(max_color=100)
        logger.info(r_colors)
    logger.info(generate_palette())


if __name__ == "__main__":
    main()


# def main():
#    """Test."""
#    all_palettes = generate_palette(1)
#    print(all_palettes)
#
#
# if __name__ == "__main__":
#    main()
