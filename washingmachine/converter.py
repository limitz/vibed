"""Converter module: SVG string to JPEG/PNG image files."""

import io
import cairosvg
from PIL import Image


def svg_to_jpeg(svg_string: str, output_path: str, quality: int = 95) -> str:
    """Convert an SVG string to a JPEG file.

    Uses cairosvg to render SVG to PNG, then Pillow to convert to JPEG.

    Args:
        svg_string: Complete SVG markup.
        output_path: Path for the output JPEG file.
        quality: JPEG quality (1-95).

    Returns:
        The output_path.
    """
    png_bytes = cairosvg.svg2png(bytestring=svg_string.encode("utf-8"), scale=2.0)
    img = Image.open(io.BytesIO(png_bytes))
    img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=quality)
    return output_path


def svg_to_png(svg_string: str, output_path: str, scale: float = 2.0) -> str:
    """Convert an SVG string to a PNG file.

    Args:
        svg_string: Complete SVG markup.
        output_path: Path for the output PNG file.
        scale: Render scale factor.

    Returns:
        The output_path.
    """
    cairosvg.svg2png(
        bytestring=svg_string.encode("utf-8"),
        write_to=output_path,
        scale=scale,
    )
    return output_path
