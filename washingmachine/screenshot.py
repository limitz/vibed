"""Generate screenshot.png from the washing machine JPEG output."""

import os
from PIL import Image


def main():
    """Open washing_machine.jpeg and save as screenshot.png."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    jpeg_path = os.path.join(script_dir, "washing_machine.jpeg")
    output_path = os.path.join(script_dir, "screenshot.png")

    img = Image.open(jpeg_path)
    img.save(output_path, "PNG")
    print(f"Saved screenshot: {output_path} ({os.path.getsize(output_path):,} bytes)")


if __name__ == "__main__":
    main()
