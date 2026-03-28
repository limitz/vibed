"""Main module: orchestrates washing machine SVG generation and JPEG conversion."""

import os

from svg_generator import generate_washing_machine_svg, refine_svg
from converter import svg_to_jpeg


REFINEMENT_PASSES = ["base", "materials", "lighting", "details", "polish"]


def main():
    """Generate a photorealistic washing machine SVG, refine it, and convert to JPEG."""
    print("=== Washing Machine SVG Generator ===\n")

    # Generate base SVG structure
    print("Generating base SVG canvas...")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="900" viewBox="0 0 800 900">
<defs>
</defs>
</svg>'''

    # Apply each refinement pass
    for pass_name in REFINEMENT_PASSES:
        print(f"  Applying refinement pass: {pass_name}...")
        svg = refine_svg(svg, pass_name)

    # Save SVG
    svg_path = "washing_machine.svg"
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"\nSaved SVG: {svg_path} ({os.path.getsize(svg_path):,} bytes)")

    # Convert to JPEG
    jpeg_path = "washing_machine.jpeg"
    svg_to_jpeg(svg, jpeg_path, quality=95)
    print(f"Saved JPEG: {jpeg_path} ({os.path.getsize(jpeg_path):,} bytes)")

    print("\nDone!")


if __name__ == "__main__":
    main()
