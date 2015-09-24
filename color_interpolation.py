"""
color_map = {
    0.0: (255, 0, 0),
    0.2: (255, 255, 255),
    0.8: (0, 200, 255),
    1.0: (0, 0, 255)
}
"""

from __future__ import division


def color_interpolate_map(color_map, progress):
    """Interpolate multiple colors according to the progress

    Parameters:
        color_map - dictionary where keys are floats from 0.0 to 1.0 to indicate progress
            and values are tuples of RGB color (see top of this file)

        progress - float from 0.0 to 1.0 indicating how far down we've gone

    Returns:
        RGB color tuple such as (255, 255, 255) for white
    """
    keys = sorted(color_map.keys())

    for i, key in enumerate(keys):
        if i + 1 == len(keys):
            break

        next_key = keys[i + 1]
        if key <= progress <= next_key:
            start_color = color_map[key]
            end_color = color_map[next_key]
            new_progress = (progress - key) / (next_key - key)
            return color_interpolate(start_color, end_color, new_progress)


def color_interpolate(start_color, end_color, progress):
    """Auxiliary color interpolation function

    What this really does is just calculate start_color + progress * (end_color - start_color)

    Parameters:
        start_color - tuple RGB color 0 - 255; the color at 0.0 progress
        end_color - tuple RGB color 0 - 255; the color at 1.0 progress
        progress - float 0.0 - 1.0; indicates the distance on the way between the 2 colors

    Returns:
        interpolated color, tuple RGB 0-255
    """
    start_r = start_color[0]
    start_g = start_color[1]
    start_b = start_color[2]

    end_r = end_color[0]
    end_g = end_color[1]
    end_b = end_color[2]

    final_r = int(start_r + (end_r - start_r) * progress)
    final_g = int(start_g + (end_g - start_g) * progress)
    final_b = int(start_b + (end_b - start_b) * progress)

    return (final_r, final_g, final_b)


def color_interpolate_fade_in(dst_color, progress):
    """Fade to the given color from black

    Parameters:
        dst_color - tuple RGB color 0 - 255; color to fade to
        progress - float 0.0 - 1.0; how far along we are in the fade

    Returns:
        interpolated color, tuple RGB 0-255
    """
    return color_interpolate((0, 0, 0), dst_color, progress)


def color_interpolate_fade_out(src_color, progress):
    """Fade to the given color to black

    Parameters:
        src_color - tuple RGB color 0 - 255; color to fade from
        progress - float 0.0 - 1.0; how far along we are in the fade
        
    Returns:
        interpolated color, tuple RGB 0-255
    """
    return color_interpolate(src_color, (0, 0, 0), progress)
