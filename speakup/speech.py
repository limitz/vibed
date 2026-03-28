"""Speech renderer — converts phoneme sequences to audio via FM synthesis."""

from __future__ import annotations

import numpy as np

from .phonemes import PhonemeSpec, PHONEMES
from .fm_engine import FMOperator, Envelope, mix_signals, noise_modulated_fm


def render_phoneme(spec: PhonemeSpec, duration: float, f0: float,
                   sample_rate: int = 44100) -> np.ndarray:
    """Render a single phoneme to audio using FM synthesis."""
    n = int(duration * sample_rate)
    if n == 0:
        return np.zeros(0)
    t = np.linspace(0, duration, n, endpoint=False)

    # Silence
    if spec.name == "SIL" or (not spec.formants and not spec.is_plosive and spec.noise_level == 0):
        return np.zeros(n)

    # Plosive: silence (closure) + short FM noise burst
    if spec.is_plosive:
        return _render_plosive(spec, duration, f0, t, n, sample_rate)

    signals = []

    # Voiced component: FM formant pairs
    if spec.voiced and spec.formants and f0 > 0:
        env = Envelope(attack=spec.attack, decay=0.02, sustain=0.8, release=spec.release)
        # Modulator at F0 (fundamental pitch)
        modulator = np.sin(2 * np.pi * f0 * t)
        for formant in spec.formants:
            mod_index = formant.bandwidth / 50.0  # scale bandwidth to modulation index
            carrier = FMOperator(
                frequency=formant.frequency,
                amplitude=formant.amplitude,
                modulation_index=mod_index,
                envelope=env,
            )
            signals.append(carrier.generate(t, modulator_signal=modulator))

    # Noise/fricative component
    if spec.noise_level > 0 and spec.formants:
        env = Envelope(attack=spec.attack, decay=0.01, sustain=0.9, release=spec.release)
        for formant in spec.formants:
            noise_sig = noise_modulated_fm(
                formant.frequency, spec.noise_level,
                duration, sample_rate
            )
            noise_sig = noise_sig * formant.amplitude * spec.noise_level
            envelope = env.apply(t, duration)
            noise_sig = noise_sig * envelope
            signals.append(noise_sig)

    if not signals:
        return np.zeros(n)

    result = mix_signals(signals)
    # Normalize to prevent clipping
    peak = np.max(np.abs(result))
    if peak > 0:
        result = result / peak * 0.4
    return result


def _render_plosive(spec: PhonemeSpec, duration: float, f0: float,
                    t: np.ndarray, n: int, sample_rate: int) -> np.ndarray:
    """Render a plosive consonant: closure + burst."""
    result = np.zeros(n)
    burst_duration = min(0.015, duration * 0.4)
    closure_duration = duration - burst_duration
    burst_start = int(closure_duration * sample_rate)

    # Optional voicing during closure (voiced plosives)
    if spec.voiced and f0 > 0:
        closure_end = burst_start
        t_closure = t[:closure_end]
        if len(t_closure) > 0:
            voicing = np.sin(2 * np.pi * f0 * t_closure) * 0.15
            env = np.linspace(0.5, 0.1, len(t_closure))
            result[:closure_end] = voicing * env

    # Burst: short FM noise at characteristic frequency
    burst_samples = n - burst_start
    if burst_samples > 0:
        burst = noise_modulated_fm(
            spec.plosive_burst_freq, spec.noise_level,
            burst_samples / sample_rate, sample_rate
        )
        # Apply fast decay envelope
        decay = np.exp(-np.linspace(0, 8, len(burst)))
        result[burst_start:burst_start + len(burst)] = burst * decay * 0.3

    return result


def interpolate_phonemes(spec_a: PhonemeSpec, spec_b: PhonemeSpec,
                         transition_duration: float, f0: float,
                         sample_rate: int = 44100) -> np.ndarray:
    """Generate smooth transition between two phonemes by interpolating FM params."""
    n = int(transition_duration * sample_rate)
    if n == 0:
        return np.zeros(0)

    # Render both phonemes for the transition duration
    audio_a = render_phoneme(spec_a, transition_duration, f0, sample_rate)
    audio_b = render_phoneme(spec_b, transition_duration, f0, sample_rate)

    # Equal-power (cosine) crossfade for smoother transitions
    t_fade = np.linspace(0, np.pi / 2, n)
    fade_out = np.cos(t_fade)
    fade_in = np.sin(t_fade)

    return audio_a * fade_out + audio_b * fade_in


def render_utterance(phonemes: list[str], sample_rate: int = 44100,
                     f0_base: float = 120.0, speed: float = 1.0) -> np.ndarray:
    """Render a full phoneme sequence to audio with coarticulation and intonation."""
    if not phonemes:
        return np.zeros(0)

    # Get specs and intonation
    specs = []
    for p in phonemes:
        if p in PHONEMES:
            specs.append(PHONEMES[p])
        else:
            specs.append(PHONEMES.get("SIL", PHONEMES["AH"]))

    f0_contour = apply_intonation(phonemes, f0_base)
    transition_dur = 0.040 / speed  # 40ms transitions for smoother speech

    segments = []
    for i, spec in enumerate(specs):
        duration = spec.duration / speed
        f0 = f0_contour[i]

        # Shorten phoneme to make room for transitions
        if len(specs) > 1:
            effective_dur = max(duration - transition_dur, 0.01)
        else:
            effective_dur = duration

        audio = render_phoneme(spec, effective_dur, f0, sample_rate)
        segments.append(audio)

        # Add transition to next phoneme
        if i < len(specs) - 1:
            next_spec = specs[i + 1]
            next_f0 = (f0 + f0_contour[i + 1]) / 2
            trans = interpolate_phonemes(spec, next_spec, transition_dur, next_f0, sample_rate)
            segments.append(trans)

    return np.concatenate(segments)


def apply_intonation(phonemes: list[str], f0_base: float = 120.0) -> list[float]:
    """Generate F0 contour: gentle rise then fall for declarative intonation."""
    n = len(phonemes)
    if n == 0:
        return []
    if n == 1:
        return [f0_base]

    contour = []
    for i in range(n):
        # Rise to ~110% at 1/3, fall to ~90% by end
        position = i / (n - 1)
        if position < 0.33:
            # Rising
            factor = 1.0 + 0.1 * (position / 0.33)
        else:
            # Falling
            factor = 1.1 - 0.2 * ((position - 0.33) / 0.67)
        contour.append(f0_base * factor)

    return contour
