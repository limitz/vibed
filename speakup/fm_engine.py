"""FM synthesis engine — core operators, envelopes, and patches."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field


@dataclass
class Envelope:
    """ADSR amplitude envelope."""
    attack: float = 0.01
    decay: float = 0.05
    sustain: float = 0.8
    release: float = 0.05

    def apply(self, t: np.ndarray, duration: float) -> np.ndarray:
        """Return amplitude multiplier array for given time array and note duration."""
        n = len(t)
        out = np.zeros(n)
        if n == 0:
            return out

        dt = t[1] - t[0] if n > 1 else 1.0 / 44100
        attack_samples = int(self.attack / dt)
        decay_samples = int(self.decay / dt)
        release_samples = int(self.release / dt)
        sustain_end = n - release_samples

        for i in range(n):
            if i < attack_samples:
                # Attack: ramp 0 → 1
                out[i] = i / max(attack_samples, 1)
            elif i < attack_samples + decay_samples:
                # Decay: ramp 1 → sustain
                progress = (i - attack_samples) / max(decay_samples, 1)
                out[i] = 1.0 - progress * (1.0 - self.sustain)
            elif i < sustain_end:
                # Sustain
                out[i] = self.sustain
            else:
                # Release: ramp sustain → 0
                progress = (i - sustain_end) / max(release_samples, 1)
                out[i] = self.sustain * (1.0 - progress)

        return np.clip(out, 0.0, 1.0)


@dataclass
class FMOperator:
    """Single FM operator (oscillator)."""
    frequency: float = 440.0
    amplitude: float = 1.0
    modulation_index: float = 0.0
    envelope: Envelope | None = None

    def generate(self, t: np.ndarray, modulator_signal: np.ndarray | None = None) -> np.ndarray:
        """Generate samples. If modulator_signal provided, use it for FM."""
        phase = 2 * np.pi * self.frequency * t
        if modulator_signal is not None:
            phase = phase + self.modulation_index * modulator_signal
        signal = self.amplitude * np.sin(phase)
        if self.envelope is not None:
            duration = t[-1] - t[0] + (t[1] - t[0]) if len(t) > 1 else 0.0
            env = self.envelope.apply(t, duration)
            signal = signal * env
        return signal


@dataclass
class FMPatch:
    """A complete FM voice: multiple operators with a connection algorithm."""
    operators: list[FMOperator] = field(default_factory=list)
    algorithm: list[tuple[int, int]] = field(default_factory=list)

    def render(self, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """Render the full patch to audio samples."""
        n = int(duration * sample_rate)
        t = np.linspace(0, duration, n, endpoint=False)

        if not self.operators:
            return np.zeros(n)

        # Build modulation graph: for each operator, collect its modulator signals
        num_ops = len(self.operators)
        outputs = [None] * num_ops
        # Find which operators are modulators (have outgoing connections)
        modulates = {}  # carrier_idx -> list of modulator_idx
        carriers = set()
        modulators = set()
        for mod_idx, car_idx in self.algorithm:
            modulates.setdefault(car_idx, []).append(mod_idx)
            carriers.add(car_idx)
            modulators.add(mod_idx)

        # Operators that are not modulated by anything get rendered first
        # Simple topological: render modulators first, then carriers
        # For simplicity, do two passes (supports 1 level of modulation depth)
        for i in range(num_ops):
            if i not in carriers:
                outputs[i] = self.operators[i].generate(t)

        for i in range(num_ops):
            if i in carriers and outputs[i] is None:
                mod_signal = np.zeros(n)
                for mod_idx in modulates.get(i, []):
                    if outputs[mod_idx] is None:
                        outputs[mod_idx] = self.operators[mod_idx].generate(t)
                    mod_signal = mod_signal + outputs[mod_idx]
                outputs[i] = self.operators[i].generate(t, modulator_signal=mod_signal)

        # Output is the sum of all carriers (non-modulator operators)
        # plus any operators not connected at all
        output_indices = [i for i in range(num_ops) if i not in modulators]
        if not output_indices:
            output_indices = list(range(num_ops))

        result = np.zeros(n)
        for i in output_indices:
            if outputs[i] is not None:
                result = result + outputs[i]
        return result


def mix_signals(signals: list[np.ndarray], amplitudes: list[float] | None = None) -> np.ndarray:
    """Mix multiple audio signals together, zero-padding shorter ones."""
    if not signals:
        return np.zeros(1)

    max_len = max(len(s) for s in signals)
    result = np.zeros(max_len)

    for i, sig in enumerate(signals):
        amp = amplitudes[i] if amplitudes is not None else 1.0
        padded = np.zeros(max_len)
        padded[:len(sig)] = sig
        result = result + padded * amp

    return result


def noise_modulated_fm(frequency: float, noise_amount: float, duration: float,
                       sample_rate: int = 44100) -> np.ndarray:
    """FM operator modulated by noise — for fricatives/unvoiced consonants."""
    n = int(duration * sample_rate)
    t = np.linspace(0, duration, n, endpoint=False)
    noise = np.random.randn(n) * noise_amount
    # Carrier modulated by noise
    phase = 2 * np.pi * frequency * t + noise_amount * 10.0 * noise
    return np.sin(phase)
