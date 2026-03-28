"""Procedural texture generation for drawing tool simulation."""

import numpy as np
from scipy.ndimage import gaussian_filter


def pencil_grain(width: int, height: int, intensity: float = 0.5, seed: int = 0) -> np.ndarray:
    """Generate grainy pencil texture simulating graphite on paper fibers.

    Returns array of shape (height, width) with values in [0, 1].
    Higher values = more graphite deposited (darker).
    """
    rng = np.random.RandomState(seed)
    noise = np.zeros((height, width), dtype=np.float64)
    # Multi-octave noise for realistic grain
    for scale, weight in [(1.0, 0.5), (2.0, 0.3), (4.0, 0.2)]:
        layer = rng.random((height, width))
        sigma = max(0.5, 1.5 / scale)
        layer = gaussian_filter(layer, sigma=sigma)
        noise += layer * weight
    # Normalize to [0, 1]
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-10)
    # Apply intensity: higher intensity = more grain variation
    noise = 1.0 - intensity * (1.0 - noise)
    return noise


def paper_texture(width: int, height: int, seed: int = 0) -> np.ndarray:
    """Generate subtle paper fiber texture.

    Returns array of shape (height, width) with values in [0, 1].
    Values near 1.0 = flat paper, slight dips simulate fiber valleys.
    """
    rng = np.random.RandomState(seed)
    noise = rng.random((height, width))
    # Low frequency for overall paper surface
    base = gaussian_filter(noise, sigma=3.0)
    # High frequency for individual fibers
    fibers = gaussian_filter(rng.random((height, width)), sigma=0.8)
    combined = 0.7 * base + 0.3 * fibers
    combined = (combined - combined.min()) / (combined.max() - combined.min() + 1e-10)
    # Compress range: paper is mostly flat with subtle variation
    return 0.95 + 0.05 * combined


def brush_bristle_pattern(width: int, seed: int = 0) -> np.ndarray:
    """Generate 1D bristle spacing pattern for brush strokes.

    Returns 1D array of length `width` with values in [0, 1].
    Peaks correspond to bristle positions, valleys to gaps between bristles.
    """
    rng = np.random.RandomState(seed)
    # Create bristle positions as periodic peaks with random variation
    pattern = np.zeros(width, dtype=np.float64)
    bristle_spacing = max(2, width // 8)
    for i in range(0, width, bristle_spacing):
        offset = int(rng.normal(0, bristle_spacing * 0.2))
        pos = min(max(0, i + offset), width - 1)
        pattern[pos] = 1.0
    # Spread bristle influence
    pattern = gaussian_filter(pattern, sigma=bristle_spacing * 0.3)
    if pattern.max() > 0:
        pattern = pattern / pattern.max()
    # Add base level so gaps aren't completely empty
    pattern = 0.3 + 0.7 * pattern
    return pattern


def charcoal_noise(width: int, height: int, intensity: float = 0.5, seed: int = 0) -> np.ndarray:
    """Generate coarse, clumpy noise for charcoal effect.

    Returns array of shape (height, width) with values in [0, 1].
    Coarser and more irregular than pencil grain.
    """
    rng = np.random.RandomState(seed)
    # Coarser base noise
    noise = rng.random((height, width))
    coarse = gaussian_filter(noise, sigma=2.5)
    # Add sharp clumps via thresholding
    clumps = rng.random((height, width))
    clumps = gaussian_filter(clumps, sigma=1.5)
    clumps = (clumps > 0.5).astype(np.float64)
    clumps = gaussian_filter(clumps, sigma=0.8)
    combined = 0.5 * coarse + 0.5 * clumps
    combined = (combined - combined.min()) / (combined.max() - combined.min() + 1e-10)
    # Apply intensity
    combined = 1.0 - intensity * (1.0 - combined)
    return combined
