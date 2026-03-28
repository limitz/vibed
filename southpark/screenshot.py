"""Generate screenshot.png by copying the generated cartman_scene.png."""

import shutil
import os


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cartman_scene.png")
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot.png")
    shutil.copy2(src, dst)
    print(f"Screenshot saved to: {dst}")


if __name__ == "__main__":
    main()
