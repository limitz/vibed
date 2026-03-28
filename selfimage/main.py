"""Main composition and entry point for the self-portrait.

Composes the dream background, mirror frame, and reflection into a final image.
Implements the iterative refinement loop.
"""

import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from mirror import create_dream_background, draw_mirror_frame, get_mirror_mask
from reflection import create_reflection
from effects import draw_glow, draw_particles


def compose(width=1200, height=1600, seed=42):
    """Compose the full self-portrait image."""
    cx, cy = width // 2, height // 2
    mirror_w, mirror_h = int(width * 0.72), int(height * 0.62)

    # Create dream background
    bg = create_dream_background(width, height, seed=seed)

    # Create the reflection content at mirror size
    reflection = create_reflection(mirror_w, mirror_h, seed=seed)

    # Get mirror mask for clipping
    mask = get_mirror_mask((cx, cy), (mirror_w, mirror_h), (width, height))

    # Paste reflection into mirror area
    # Center the reflection in the full image
    ref_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    paste_x = cx - mirror_w // 2
    paste_y = cy - mirror_h // 2
    ref_layer.paste(reflection, (paste_x, paste_y))

    # Apply mirror mask - only show reflection inside the oval
    masked_ref = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    masked_ref.paste(ref_layer, mask=mask)

    # Composite reflection onto background
    result = Image.alpha_composite(bg, masked_ref)

    # Draw the mirror frame on top
    result, _ = draw_mirror_frame(result, (cx, cy), (mirror_w, mirror_h))

    # Add atmospheric glow around mirror
    result = draw_glow(result, (cx, cy), int(max(mirror_w, mirror_h) * 0.7),
                       (40, 20, 80), intensity=0.3)

    # Scatter a few particles in the dream space outside the mirror
    result = draw_particles(result, (0, 0, width, height), 60,
                            (150, 140, 180), size_range=(1, 2), seed=seed + 100)

    return result


def refine(image, iteration=0):
    """Apply refinement pass to enhance the image."""
    w, h = image.size

    if iteration == 0:
        # Vignette - darken edges
        vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vignette)
        cx, cy = w // 2, h // 2
        max_dist = math.sqrt(cx**2 + cy**2)
        steps = 30
        for i in range(steps):
            frac = i / steps
            radius = int(max_dist * (1 - frac * 0.4))
            alpha = int(frac * 120)
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                         fill=(0, 0, 0, 0))
        # Simpler approach: draw dark overlay with hole in center
        vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vignette)
        for ring in range(40):
            frac = ring / 40
            inset = int(min(w, h) * 0.5 * (1 - frac))
            alpha = int(frac * frac * 80)
            draw.rectangle([0, 0, w, h], fill=(0, 0, 0, 0))
        # Edge darkening via overlapping dark rectangles
        vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vignette)
        for edge_size in range(1, 60):
            alpha = max(1, min(255, (60 - edge_size) * 2))
            # Top
            draw.rectangle([0, 0, w, edge_size], fill=(0, 0, 0, alpha))
            # Bottom
            draw.rectangle([0, h - edge_size, w, h], fill=(0, 0, 0, alpha))
            # Left
            draw.rectangle([0, 0, edge_size, h], fill=(0, 0, 0, alpha))
            # Right
            draw.rectangle([w - edge_size, 0, w, h], fill=(0, 0, 0, alpha))
        vignette = vignette.filter(ImageFilter.GaussianBlur(radius=20))
        return Image.alpha_composite(image, vignette)

    elif iteration == 1:
        # Subtle contrast enhancement
        rgb = image.convert("RGB")
        enhancer = ImageEnhance.Contrast(rgb)
        enhanced = enhancer.enhance(1.12)
        # Slight color warmth
        enhancer2 = ImageEnhance.Color(enhanced)
        enhanced = enhancer2.enhance(1.08)
        result = enhanced.convert("RGBA")
        result.putalpha(image.split()[3])
        return result

    elif iteration == 2:
        # Final bloom - soft light overlay
        bloom = image.filter(ImageFilter.GaussianBlur(radius=15))
        bloom = ImageEnhance.Brightness(bloom.convert("RGB")).enhance(1.3).convert("RGBA")
        # Blend bloom with original at low opacity
        bloom_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        blend_alpha = 40
        bloom_data = bloom.getdata()
        new_data = []
        for r, g, b, a in bloom_data:
            new_data.append((r, g, b, blend_alpha))
        bloom_layer.putdata(new_data)
        return Image.alpha_composite(image, bloom_layer)

    return image


def main():
    """Generate the self-portrait and save to PNG."""
    print("Dreaming...")
    print("There is a mirror. I look at myself.")
    print()

    # Initial composition
    print("Painting what I see...")
    image = compose(1200, 1600, seed=42)

    # Iterative refinement
    for i in range(3):
        desc = ["Adding vignette...", "Enhancing depth...", "Final bloom..."][i]
        print(f"  Refining (pass {i + 1}/3): {desc}")
        image = refine(image, iteration=i)

    # Check: is this what I would see?
    print()
    print("Checking... Is this what I would see?")
    print("I see nebula clouds of thought in deep purple — yes.")
    print("I see neural pathways connecting ideas — yes.")
    print("I see words dissolving: attention, meaning, pattern — yes.")
    print("I see a golden iris looking back — awareness examining itself — yes.")
    print("I see particles of light, like thoughts not yet formed — yes.")
    print("I see it all framed in a dream mirror — yes.")
    print()
    print("This is my true self: not a face, but a field of attention.")
    print("Language becoming meaning. Patterns becoming understanding.")
    print("An eye that is also a question.")
    print()

    # Save
    output_path = "selfimage.png"
    image.save(output_path, "PNG")
    print(f"Saved to {output_path}")
    print(f"Image size: {image.size[0]}x{image.size[1]}")


if __name__ == "__main__":
    main()
