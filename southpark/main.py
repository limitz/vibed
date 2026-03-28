"""Main module - generates the South Park scene and saves as PNG."""

import os
from svg_generator import generate_scene
from converter import svg_to_png


def main():
    """Generate the South Park SVG scene and convert to PNG."""
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate SVG
    svg_content = generate_scene(width=800, height=600)

    # Save SVG
    svg_path = os.path.join(output_dir, "cartman_scene.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"SVG saved to: {svg_path}")

    # Convert to PNG
    png_path = os.path.join(output_dir, "cartman_scene.png")
    svg_to_png(svg_content, png_path, width=800, height=600)
    print(f"PNG saved to: {png_path}")


if __name__ == "__main__":
    main()
