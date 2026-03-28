"""
Flatulence synthesis engine — physically-inspired aeroacoustic model.

The sphincter is modeled as an oscillating aperture driven by gas pressure.
The core nonlinearity is that the aperture cannot be negative (tissue contact),
so the oscillation is half-wave rectified. This naturally produces the
harmonic-rich "buzz" that characterizes flatulence — the same mechanism that
makes brass mouthpiece buzzes and lip trills ("raspberries") sound buzzy.

Physical chain:
1. APERTURE MOTION — Sphincter oscillates quasi-periodically with jitter.
   Half-wave rectified (aperture >= 0). This creates the harmonic content.
2. AIRFLOW — Flow through aperture: u(t) = sqrt(P) * aperture(t).
   Naturally couples gas pressure to loudness.
3. TURBULENCE — Noise proportional to flow velocity. High flow = more noise.
   This embeds the noise in the physics rather than mixing it in artificially.
4. ACOUSTIC RADIATION — Sound ~ d/dt(flow + turbulence). The time derivative
   emphasizes transients and gives the characteristic "edge" to each cycle.
5. TISSUE FILTER — Low-pass from surrounding flesh.
6. ENVELOPE — Pressure decay, sputtering from irregular muscle tension.
"""

import numpy as np
from scipy import signal
from typing import Optional


SAMPLE_RATE = 44100


def _make_aperture(frequency: float, n_samples: int,
                   rng: np.random.RandomState,
                   sample_rate: int) -> np.ndarray:
    """Model the sphincter aperture oscillation.

    The sphincter vibrates quasi-periodically. The aperture (opening size)
    oscillates around a mean value. When it tries to go negative, the tissue
    surfaces contact each other and the aperture clamps to zero.

    This half-wave rectification is the key nonlinearity that creates
    the buzzy harmonic spectrum.
    """
    t = np.arange(n_samples) / sample_rate
    duration = n_samples / sample_rate

    # Monotonic pitch slide: randomly up or down, 15-40% of frequency
    slide_amount = rng.uniform(0.15, 0.40) * frequency
    if rng.random() < 0.5:
        slide_amount = -slide_amount
    # Smooth curve (not linear — pressure change is nonlinear)
    slide_shape = (t / duration) ** rng.uniform(0.6, 1.5)
    slide = slide_amount * slide_shape

    # Per-sample jitter for organic raspiness (no wobble/vibrato)
    jitter_strength = rng.uniform(0.3, 1.5)
    jitter = np.cumsum(rng.randn(n_samples)) * jitter_strength
    jitter -= np.linspace(jitter[0], jitter[-1], n_samples)

    inst_freq = frequency + slide + jitter
    inst_freq = np.clip(inst_freq, frequency * 0.3, frequency * 2.5)

    # Phase
    phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate

    # Sphincter motion: asymmetric oscillation
    # The opening phase is faster than closing (tissue elasticity)
    # Model with a skewed sinusoid
    skew = rng.uniform(0.15, 0.40)  # sawtooth width param
    oscillation = signal.sawtooth(phase, width=skew)

    # The "rest position" of the aperture — how open the sphincter is on average
    # A value near 0 means it's barely open, creating more contact (more buzz)
    # A value near 1 means it's wide open (smoother, less buzz)
    openness = rng.uniform(-0.8, -0.3)

    aperture = oscillation + openness

    # HALF-WAVE RECTIFICATION: aperture can't be negative
    # This is where the buzz comes from
    aperture = np.maximum(aperture, 0.0)

    # Subtle cheek vibration — just enough for body, not wobbly
    for _ in range(rng.randint(1, 3)):
        cheek_freq = rng.uniform(10.0, 30.0)
        cheek_depth = rng.uniform(0.03, 0.08)
        cheek_wobble = cheek_depth * np.sin(2 * np.pi * cheek_freq * t + rng.uniform(0, 2 * np.pi))
        aperture += cheek_wobble

    # Light tremor — tight, not floppy
    tremor = rng.randn(n_samples) * rng.uniform(0.03, 0.08)
    aperture += tremor
    aperture = np.maximum(aperture, 0.0)

    return aperture


def _compute_flow(aperture: np.ndarray, pressure: np.ndarray,
                  rng: np.random.RandomState, frequency: float,
                  sample_rate: int) -> np.ndarray:
    """Compute airflow through the aperture.

    Flow is proportional to sqrt(pressure) * aperture area.
    Turbulence noise scales with flow velocity and is pre-filtered
    to low frequencies (gas through flesh has no HF content).
    """
    # Laminar flow component
    flow = np.sqrt(np.maximum(pressure, 0)) * aperture

    # Turbulence: low-pass filtered noise, scaled by flow velocity
    raw_noise = rng.randn(len(flow))
    # Pre-shape noise: cut everything above ~frequency * 3
    noise_cutoff = min(sample_rate * 0.45, frequency * 3.0)
    noise_cutoff = max(60, noise_cutoff)
    sos = signal.butter(3, noise_cutoff, btype='low', fs=sample_rate, output='sos')
    shaped_noise = signal.sosfilt(sos, raw_noise)
    shaped_noise /= np.std(shaped_noise) + 1e-10

    turb_strength = rng.uniform(0.15, 0.35)
    turbulence = shaped_noise * turb_strength * flow

    return flow + turbulence


def _make_pressure_curve(n_samples: int, rng: np.random.RandomState,
                         sample_rate: int) -> np.ndarray:
    """Gas pressure over time.

    Starts at some level, may ramp up briefly, then decays as gas escapes.
    """
    t = np.linspace(0, n_samples / sample_rate, n_samples)
    duration = n_samples / sample_rate

    # Onset ramp — punchy attack
    onset = rng.uniform(0.002, 0.010)
    ramp = np.clip(t / onset, 0, 1)

    # Volume slope: randomly crescendo or decrescendo over the note
    slope_amount = rng.uniform(0.3, 0.7)
    if rng.random() < 0.5:
        # Crescendo: starts quieter, gets louder
        slope = 1.0 - slope_amount + slope_amount * (t / duration)
    else:
        # Decrescendo: starts louder, gets quieter
        slope = 1.0 - slope_amount * (t / duration)

    # Base pressure decay (gentle)
    decay = rng.uniform(0.2, 1.5)
    p = np.exp(-decay * t / duration) * slope

    # Don't let pressure die completely
    p = np.clip(p, rng.uniform(0.05, 0.2), 1.0)

    # End taper
    taper_time = rng.uniform(0.01, 0.04)
    remaining = duration - t
    taper = np.clip(remaining / taper_time, 0, 1)

    return ramp * p * taper


def _make_sputter(n_samples: int, rng: np.random.RandomState,
                  sample_rate: int) -> np.ndarray:
    """Irregular amplitude modulation from muscle tension variation."""
    t = np.linspace(0, n_samples / sample_rate, n_samples)
    duration = n_samples / sample_rate
    env = np.ones(n_samples)

    # Flutter: multiple overlapping modulation modes
    for _ in range(rng.randint(3, 6)):
        f = rng.uniform(4.0, 25.0)
        depth = rng.uniform(0.1, 0.5)
        ph = rng.uniform(0, 2 * np.pi)
        env *= 1.0 - depth * np.clip(np.sin(2 * np.pi * f * t + ph), 0, 1)

    # Brief dropouts (sphincter clenches)
    n_dropouts = rng.randint(1, max(2, int(duration * 10)))
    for _ in range(n_dropouts):
        pos = rng.uniform(0.05, 0.90) * duration
        width = rng.uniform(0.003, 0.018)
        depth = rng.uniform(0.5, 0.95)
        env *= 1.0 - depth * np.exp(-0.5 * ((t - pos) / width) ** 2)

    # Slight roughness
    rough = 1.0 + rng.uniform(0.03, 0.10) * np.cumsum(rng.randn(n_samples)) / sample_rate * 80
    rough = np.clip(rough, 0.6, 1.3)
    env *= rough

    return env


def _apply_tissue_filter(audio: np.ndarray, frequency: float,
                         rng: np.random.RandomState,
                         sample_rate: int) -> np.ndarray:
    """Low-pass through surrounding tissue + buttcheek resonance."""
    cutoff = rng.uniform(250, 500) + frequency * 0.7
    cutoff = min(cutoff, sample_rate * 0.45)
    sos = signal.butter(3, cutoff, btype='low', fs=sample_rate, output='sos')
    result = signal.sosfilt(sos, audio)

    # Buttcheek resonance: the flesh mass has a natural resonance in the
    # low-mid range that adds a thick, wobbly body to the sound
    cheek_res = rng.uniform(40, 130)
    bw = cheek_res * rng.uniform(0.8, 1.5)
    lo = max(20, cheek_res - bw / 2)
    hi = min(sample_rate * 0.45, cheek_res + bw / 2)
    if hi > lo:
        sos_res = signal.butter(1, [lo, hi], btype='band', fs=sample_rate, output='sos')
        resonant = signal.sosfilt(sos_res, audio)
        result += rng.uniform(0.6, 1.2) * resonant

    return result


def synthesize(
    frequency: float,
    duration: float,
    seed: Optional[int] = None,
    sample_rate: int = SAMPLE_RATE,
) -> np.ndarray:
    """Synthesize a single flatulence sound.

    Physically-inspired model: oscillating aperture → airflow → radiation → tissue filter.

    Args:
        frequency: Base frequency in Hz (typical range: 40-800 Hz).
        duration: Duration in seconds.
        seed: Random seed for reproducibility in tests. None = truly random.
        sample_rate: Audio sample rate.

    Returns:
        Mono audio samples as float64 numpy array, normalized to [-1, 1].
    """
    rng = np.random.RandomState(seed)
    n_samples = int(sample_rate * duration)

    # 1. Gas pressure over time
    pressure = _make_pressure_curve(n_samples, rng, sample_rate)

    # 2. Sphincter aperture oscillation (half-wave rectified → buzz)
    aperture = _make_aperture(frequency, n_samples, rng, sample_rate)

    # 3. Airflow through aperture (includes turbulence)
    flow = _compute_flow(aperture, pressure, rng, frequency, sample_rate)

    # 4. Sound from flow directly (no derivative — it adds HF)
    sound = flow - np.mean(flow)

    # 5. Sputtering modulation
    sputter = _make_sputter(n_samples, rng, sample_rate)
    sound *= sputter

    # 6. Moderate saturation for grit (not too hard — avoids HF harmonics)
    sound = np.tanh(2.0 * sound / (np.max(np.abs(sound)) + 1e-10))

    # 7. Tissue filtering LAST
    sound = _apply_tissue_filter(sound, frequency, rng, sample_rate)

    # Normalize
    peak = np.max(np.abs(sound))
    if peak > 0:
        sound /= peak

    return sound
