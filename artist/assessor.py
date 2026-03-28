"""Image analysis for pass/fail evaluation of lesson outputs."""

import math
import numpy as np
from PIL import Image
from scipy import ndimage


def _to_grayscale(img: Image.Image) -> np.ndarray:
    """Convert PIL Image to grayscale numpy array [0-255]."""
    return np.array(img.convert("L"), dtype=np.float64)


def _ink_mask(gray: np.ndarray, threshold: float = 245.0) -> np.ndarray:
    """Return boolean mask where True = ink (darker than threshold)."""
    return gray < threshold


def assess_coverage(image: Image.Image, min_pct: float = 0.0, max_pct: float = 100.0) -> dict:
    """Check what percentage of the canvas has ink on it."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    pct = 100.0 * mask.sum() / mask.size
    passed = min_pct <= pct <= max_pct
    return {"passed": passed, "score": pct,
            "details": f"Coverage: {pct:.1f}% (target: {min_pct:.0f}-{max_pct:.0f}%)"}


def assess_value_range(image: Image.Image, min_range: float = 0.0) -> dict:
    """Check the tonal range (difference between darkest and lightest ink)."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    if mask.sum() < 10:
        return {"passed": False, "score": 0, "details": "Not enough ink to assess value range"}
    ink_values = gray[mask]
    darkest = np.percentile(ink_values, 2)
    lightest = np.percentile(ink_values, 98)
    vrange = lightest - darkest
    bg_lightest = np.percentile(gray[~mask], 50) if (~mask).sum() > 0 else 255
    total_range = bg_lightest - darkest
    passed = total_range >= min_range
    return {"passed": passed, "score": total_range,
            "details": f"Value range: {total_range:.0f} (ink: {darkest:.0f}-{lightest:.0f}, bg: ~{bg_lightest:.0f}, target >= {min_range:.0f})"}


def assess_symmetry(image: Image.Image, threshold: float = 0.5) -> dict:
    """Check bilateral symmetry by comparing image with its horizontal flip."""
    gray = _to_grayscale(image)
    flipped = np.fliplr(gray)
    # Normalized cross-correlation
    a = gray - gray.mean()
    b = flipped - flipped.mean()
    ncc = np.sum(a * b) / (np.sqrt(np.sum(a ** 2) * np.sum(b ** 2)) + 1e-10)
    passed = ncc >= threshold
    return {"passed": passed, "score": float(ncc),
            "details": f"Symmetry NCC: {ncc:.3f} (target >= {threshold:.2f})"}


def assess_line_quality(image: Image.Image, expected_angle_deg: float = None,
                        max_deviation_px: float = 3.0) -> dict:
    """Assess straightness and consistency of lines in the image."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    if mask.sum() < 10:
        return {"passed": False, "score": 0, "details": "No ink found"}

    # Find ink pixel coordinates
    ys, xs = np.where(mask)

    if expected_angle_deg is not None:
        # Check deviation from expected line direction
        angle_rad = math.radians(expected_angle_deg)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
        # Project points onto perpendicular direction
        cx, cy = xs.mean(), ys.mean()
        perp_dist = -(xs - cx) * sin_a + (ys - cy) * cos_a
        rms = math.sqrt(np.mean(perp_dist ** 2))
    else:
        # Fit a line and measure RMS deviation
        if xs.std() > ys.std():
            # More horizontal: fit y = mx + b
            coeffs = np.polyfit(xs, ys, 1)
            predicted = np.polyval(coeffs, xs)
            deviations = ys - predicted
        else:
            # More vertical: fit x = my + b
            coeffs = np.polyfit(ys, xs, 1)
            predicted = np.polyval(coeffs, ys)
            deviations = xs - predicted
        rms = math.sqrt(np.mean(deviations ** 2))

    passed = rms <= max_deviation_px
    return {"passed": passed, "score": float(rms),
            "details": f"Line RMS deviation: {rms:.2f}px (target <= {max_deviation_px:.1f}px)"}


def assess_region_count(image: Image.Image, min_regions: int = 1, max_regions: int = 100) -> dict:
    """Count distinct connected ink regions."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray, threshold=240)
    labeled, n_regions = ndimage.label(mask)
    # Filter out tiny regions (< 20 pixels)
    sizes = ndimage.sum(mask, labeled, range(1, n_regions + 1))
    significant = sum(1 for s in sizes if s >= 20)
    passed = min_regions <= significant <= max_regions
    return {"passed": passed, "score": significant,
            "details": f"Regions: {significant} (target: {min_regions}-{max_regions})"}


def assess_gradient_smoothness(image: Image.Image, max_banding: float = 0.3) -> dict:
    """Assess how smoothly values transition (detect banding artifacts)."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    if mask.sum() < 100:
        return {"passed": False, "score": 0, "details": "Not enough ink"}

    # Compute gradient magnitude
    dy = np.abs(np.diff(gray, axis=0))
    dx = np.abs(np.diff(gray, axis=1))

    # Banding metric: ratio of very sharp transitions to total
    sharp_threshold = 30.0
    sharp_y = (dy > sharp_threshold).sum() / dy.size
    sharp_x = (dx > sharp_threshold).sum() / dx.size
    banding = (sharp_y + sharp_x) / 2

    passed = banding <= max_banding
    return {"passed": passed, "score": float(banding),
            "details": f"Banding: {banding:.3f} (target <= {max_banding:.2f})"}


def assess_color_diversity(image: Image.Image, min_colors: int = 1) -> dict:
    """Count distinct color hue clusters in the image."""
    arr = np.array(image.convert("RGB"), dtype=np.float64)
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)

    if mask.sum() < 10:
        return {"passed": False, "score": 0, "details": "No ink found"}

    # Get ink pixels in RGB
    ink_r = arr[:, :, 0][mask]
    ink_g = arr[:, :, 1][mask]
    ink_b = arr[:, :, 2][mask]

    # Check saturation: are there colored (not just gray) pixels?
    max_rgb = np.maximum(np.maximum(ink_r, ink_g), ink_b)
    min_rgb = np.minimum(np.minimum(ink_r, ink_g), ink_b)
    saturation = (max_rgb - min_rgb) / (max_rgb + 1e-10)

    # Saturated pixels (actual colors, not grays)
    colored_mask = saturation > 0.15
    n_colored = colored_mask.sum()

    if n_colored < 10:
        # Monochrome drawing
        n_hues = 1
    else:
        # Compute hue for colored pixels
        r_c, g_c, b_c = ink_r[colored_mask], ink_g[colored_mask], ink_b[colored_mask]
        hue = np.arctan2(np.sqrt(3.0) * (g_c - b_c), 2.0 * r_c - g_c - b_c)
        hue_deg = np.degrees(hue) % 360

        # Bin hues into 30-degree buckets (12 bins)
        bins = np.histogram(hue_deg, bins=12, range=(0, 360))[0]
        n_hues = max(1, sum(1 for b in bins if b > n_colored * 0.03))

    passed = n_hues >= min_colors
    return {"passed": passed, "score": n_hues,
            "details": f"Color hues: {n_hues} (target >= {min_colors})"}


def assess_composition(image: Image.Image, centered: bool = None) -> dict:
    """Analyze composition using a 3x3 grid density analysis."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    h, w = mask.shape

    # Divide into 3x3 grid
    densities = np.zeros((3, 3))
    for row in range(3):
        for col in range(3):
            r0, r1 = row * h // 3, (row + 1) * h // 3
            c0, c1 = col * w // 3, (col + 1) * w // 3
            cell = mask[r0:r1, c0:c1]
            densities[row, col] = cell.mean()

    center_density = densities[1, 1]
    overall_density = mask.mean()
    max_density = densities.max()

    if centered is True:
        passed = center_density >= max_density * 0.7
        msg = "centered"
    elif centered is False:
        passed = center_density < max_density * 0.9
        msg = "not centered"
    else:
        passed = overall_density > 0
        msg = "any"

    return {"passed": passed, "score": float(center_density),
            "details": f"Composition ({msg}): center density {center_density:.3f}, max {max_density:.3f}"}


def assess_horizontal_zones(image: Image.Image, min_zones: int = 2) -> dict:
    """Detect distinct horizontal zones (e.g., sky/ground in landscape)."""
    gray = _to_grayscale(image)
    h, w = gray.shape

    # Compute mean brightness per row band
    band_h = max(1, h // 20)
    bands = []
    for i in range(0, h, band_h):
        band = gray[i:min(i + band_h, h), :]
        bands.append(band.mean())

    bands = np.array(bands)
    if len(bands) < 3:
        return {"passed": False, "score": 1, "details": "Image too small"}

    # Detect zone boundaries: significant changes in mean brightness
    diffs = np.abs(np.diff(bands))
    threshold = max(5.0, np.std(bands) * 0.5)
    boundaries = (diffs > threshold).sum()
    zones = min(boundaries + 1, 5)

    passed = zones >= min_zones
    return {"passed": passed, "score": zones,
            "details": f"Horizontal zones: {zones} (target >= {min_zones})"}


def assess_closure(image: Image.Image, tolerance_px: float = 5.0) -> dict:
    """Check if shapes are closed (endpoints near each other)."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)
    labeled, n_regions = ndimage.label(mask)

    closed_count = 0
    total_count = 0
    for i in range(1, n_regions + 1):
        region = labeled == i
        size = region.sum()
        if size < 30:
            continue
        total_count += 1

        # Check if region forms a closed shape by looking at its boundary
        # A closed shape has no endpoints (all boundary pixels have >= 2 neighbors)
        # Simplified: check if interior has holes (enclosed white space)
        filled = ndimage.binary_fill_holes(region)
        interior = filled & ~region
        if interior.sum() > size * 0.05:
            closed_count += 1

    if total_count == 0:
        return {"passed": False, "score": 0, "details": "No significant regions found"}

    ratio = closed_count / total_count
    passed = ratio >= 0.5
    return {"passed": passed, "score": ratio,
            "details": f"Closed shapes: {closed_count}/{total_count} ({ratio:.0%})"}


def assess_line_spacing(image: Image.Image, target_angle_deg: float = 0.0,
                        max_spacing_cv: float = 0.25) -> dict:
    """Assess uniformity of parallel line spacing (for hatching)."""
    gray = _to_grayscale(image)
    mask = _ink_mask(gray)

    # Sample along the perpendicular direction to the expected lines
    angle_rad = math.radians(target_angle_deg)
    perp_angle = angle_rad + math.pi / 2

    h, w = gray.shape
    cx, cy = w / 2, h / 2

    # Create a scanline perpendicular to expected lines through center
    length = int(math.sqrt(w ** 2 + h ** 2))
    cos_p, sin_p = math.cos(perp_angle), math.sin(perp_angle)

    profile = []
    for d in range(-length // 2, length // 2):
        px = int(cx + d * cos_p)
        py = int(cy + d * sin_p)
        if 0 <= px < w and 0 <= py < h:
            profile.append(mask[py, px])

    profile = np.array(profile, dtype=float)

    # Find transitions (ink boundaries)
    transitions = np.where(np.abs(np.diff(profile)) > 0.5)[0]
    if len(transitions) < 4:
        return {"passed": False, "score": 0, "details": "Too few lines detected for spacing analysis"}

    # Compute spacings between consecutive line starts (every other transition)
    starts = transitions[::2]
    spacings = np.diff(starts).astype(float)
    if len(spacings) < 2:
        return {"passed": False, "score": 0, "details": "Not enough spacings to analyze"}

    cv = spacings.std() / (spacings.mean() + 1e-10)
    passed = cv <= max_spacing_cv
    return {"passed": passed, "score": float(cv),
            "details": f"Spacing CV: {cv:.3f} (target <= {max_spacing_cv:.2f}, mean={spacings.mean():.1f}px)"}
