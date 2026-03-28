"""Tests for the FM synthesis engine."""

import unittest
import numpy as np
from speakup.fm_engine import Envelope, FMOperator, FMPatch, mix_signals, noise_modulated_fm


SAMPLE_RATE = 44100


class TestEnvelope(unittest.TestCase):
    def test_output_length(self):
        env = Envelope(attack=0.01, decay=0.05, sustain=0.8, release=0.05)
        duration = 0.5
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = env.apply(t, duration)
        self.assertEqual(len(result), len(t))

    def test_starts_at_zero(self):
        env = Envelope(attack=0.05, decay=0.05, sustain=0.7, release=0.05)
        duration = 0.3
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = env.apply(t, duration)
        self.assertAlmostEqual(result[0], 0.0, places=2)

    def test_peak_reaches_one(self):
        env = Envelope(attack=0.01, decay=0.05, sustain=0.8, release=0.05)
        duration = 0.5
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = env.apply(t, duration)
        self.assertAlmostEqual(np.max(result), 1.0, places=1)

    def test_sustain_level(self):
        env = Envelope(attack=0.01, decay=0.05, sustain=0.6, release=0.05)
        duration = 0.5
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = env.apply(t, duration)
        # Check sustain region (middle of the note)
        mid = int(0.2 * SAMPLE_RATE)
        self.assertAlmostEqual(result[mid], 0.6, places=1)

    def test_ends_near_zero(self):
        env = Envelope(attack=0.01, decay=0.05, sustain=0.8, release=0.05)
        duration = 0.3
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = env.apply(t, duration)
        self.assertAlmostEqual(result[-1], 0.0, delta=0.1)


class TestFMOperator(unittest.TestCase):
    def test_output_length(self):
        op = FMOperator(frequency=440.0, amplitude=1.0)
        duration = 0.5
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = op.generate(t)
        self.assertEqual(len(result), len(t))

    def test_pure_sine_no_modulator(self):
        """Without modulator, should produce a pure sine wave."""
        op = FMOperator(frequency=440.0, amplitude=1.0, modulation_index=0.0)
        duration = 0.1
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = op.generate(t)
        expected = np.sin(2 * np.pi * 440.0 * t)
        np.testing.assert_allclose(result, expected, atol=1e-10)

    def test_amplitude_scaling(self):
        op = FMOperator(frequency=440.0, amplitude=0.5)
        duration = 0.1
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = op.generate(t)
        self.assertAlmostEqual(np.max(np.abs(result)), 0.5, places=1)

    def test_fm_with_modulator(self):
        """FM should produce different output than pure sine."""
        op = FMOperator(frequency=440.0, amplitude=1.0, modulation_index=5.0)
        duration = 0.1
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        modulator = np.sin(2 * np.pi * 110.0 * t)
        result = op.generate(t, modulator_signal=modulator)
        pure_sine = np.sin(2 * np.pi * 440.0 * t)
        # FM output should differ from pure sine
        self.assertGreater(np.max(np.abs(result - pure_sine)), 0.1)

    def test_fm_with_envelope(self):
        env = Envelope(attack=0.01, decay=0.02, sustain=0.7, release=0.02)
        op = FMOperator(frequency=440.0, amplitude=1.0, envelope=env)
        duration = 0.1
        t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
        result = op.generate(t)
        # First sample should be near zero due to envelope attack
        self.assertAlmostEqual(result[0], 0.0, places=2)


class TestFMPatch(unittest.TestCase):
    def test_render_length(self):
        patch = FMPatch(
            operators=[FMOperator(frequency=440.0, amplitude=1.0)],
            algorithm=[]
        )
        duration = 0.5
        result = patch.render(duration, SAMPLE_RATE)
        expected_len = int(duration * SAMPLE_RATE)
        self.assertEqual(len(result), expected_len)

    def test_render_not_silent(self):
        patch = FMPatch(
            operators=[FMOperator(frequency=440.0, amplitude=1.0)],
            algorithm=[]
        )
        result = patch.render(0.1, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.1)

    def test_modulator_carrier_connection(self):
        """Test that algorithm connections produce FM output."""
        patch = FMPatch(
            operators=[
                FMOperator(frequency=110.0, amplitude=1.0, modulation_index=5.0),  # modulator
                FMOperator(frequency=440.0, amplitude=1.0, modulation_index=5.0),  # carrier
            ],
            algorithm=[(0, 1)]  # op0 modulates op1
        )
        result = patch.render(0.1, SAMPLE_RATE)
        # Should produce non-trivial output
        self.assertGreater(np.max(np.abs(result)), 0.1)


class TestMixSignals(unittest.TestCase):
    def test_single_signal(self):
        sig = np.ones(100)
        result = mix_signals([sig])
        np.testing.assert_allclose(result, sig)

    def test_two_signals_equal(self):
        sig1 = np.ones(100)
        sig2 = np.ones(100) * 2
        result = mix_signals([sig1, sig2])
        np.testing.assert_allclose(result, np.ones(100) * 3)

    def test_amplitude_weighting(self):
        sig1 = np.ones(100)
        sig2 = np.ones(100)
        result = mix_signals([sig1, sig2], amplitudes=[0.5, 0.3])
        np.testing.assert_allclose(result, np.ones(100) * 0.8)

    def test_different_lengths(self):
        sig1 = np.ones(100)
        sig2 = np.ones(50) * 2
        result = mix_signals([sig1, sig2])
        self.assertEqual(len(result), 100)
        # First 50 samples: 1 + 2 = 3
        np.testing.assert_allclose(result[:50], np.ones(50) * 3)
        # Last 50 samples: 1 + 0 = 1
        np.testing.assert_allclose(result[50:], np.ones(50))


class TestNoiseModulatedFM(unittest.TestCase):
    def test_output_length(self):
        result = noise_modulated_fm(5000.0, 0.8, 0.1, SAMPLE_RATE)
        self.assertEqual(len(result), int(0.1 * SAMPLE_RATE))

    def test_not_silent(self):
        result = noise_modulated_fm(5000.0, 0.8, 0.1, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.01)

    def test_noise_produces_spread_spectrum(self):
        """Noise-modulated FM should have spread energy, not a single peak."""
        result = noise_modulated_fm(2000.0, 1.0, 0.5, SAMPLE_RATE)
        fft = np.abs(np.fft.rfft(result))
        freqs = np.fft.rfftfreq(len(result), 1.0 / SAMPLE_RATE)
        # Energy should be spread: check that peak doesn't contain most energy
        peak_idx = np.argmax(fft)
        peak_energy = np.sum(fft[max(0, peak_idx-5):peak_idx+5] ** 2)
        total_energy = np.sum(fft ** 2)
        # Peak region should be less than 50% of total energy (spread spectrum)
        self.assertLess(peak_energy / total_energy, 0.5)


if __name__ == "__main__":
    unittest.main()
