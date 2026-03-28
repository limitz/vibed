"""Converter module - converts SVG string to PNG file."""

import cairosvg


def svg_to_png(svg_string: str, output_path: str, width: int = 800, height: int = 600) -> str:
    """Convert an SVG string to a PNG file.

    Args:
        svg_string: The SVG content as a string.
        output_path: Path to save the PNG file.
        width: Output width in pixels.
        height: Output height in pixels.

    Returns:
        The output_path on success.
    """
    cairosvg.svg2png(
        bytestring=svg_string.encode("utf-8"),
        write_to=output_path,
        output_width=width,
        output_height=height,
    )
    return output_path
