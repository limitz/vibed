"""Phoneme definitions — each phoneme mapped to FM synthesis parameters."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FormantSpec:
    """Specification for a single formant."""
    frequency: float  # Hz — carrier frequency
    amplitude: float  # relative amplitude 0.0–1.0
    bandwidth: float  # controls modulation index


@dataclass
class PhonemeSpec:
    """Complete specification for a phoneme's FM synthesis parameters."""
    name: str
    formants: list[FormantSpec] = field(default_factory=list)
    f0: float = 120.0
    voiced: bool = True
    noise_level: float = 0.0
    duration: float = 0.12
    attack: float = 0.01
    release: float = 0.02
    is_plosive: bool = False
    plosive_burst_freq: float = 0.0


# Phoneme inventory — formant values from acoustic phonetics literature
PHONEMES: dict[str, PhonemeSpec] = {
    # === VOWELS ===
    "AH": PhonemeSpec(  # /ɑ/ as in "father"
        name="AH",
        formants=[FormantSpec(800, 1.0, 80), FormantSpec(1200, 0.7, 90), FormantSpec(2500, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "EE": PhonemeSpec(  # /i/ as in "see"
        name="EE",
        formants=[FormantSpec(270, 1.0, 60), FormantSpec(2300, 0.7, 100), FormantSpec(3000, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "EH": PhonemeSpec(  # /ɛ/ as in "bed"
        name="EH",
        formants=[FormantSpec(530, 1.0, 70), FormantSpec(1850, 0.7, 100), FormantSpec(2500, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "IH": PhonemeSpec(  # /ɪ/ as in "sit"
        name="IH",
        formants=[FormantSpec(390, 1.0, 65), FormantSpec(1990, 0.6, 100), FormantSpec(2550, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.10,
    ),
    "OH": PhonemeSpec(  # /oʊ/ as in "go"
        name="OH",
        formants=[FormantSpec(500, 1.0, 70), FormantSpec(900, 0.7, 80), FormantSpec(2500, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "OO": PhonemeSpec(  # /u/ as in "boot"
        name="OO",
        formants=[FormantSpec(300, 1.0, 60), FormantSpec(870, 0.6, 80), FormantSpec(2250, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "UH": PhonemeSpec(  # /ʌ/ as in "but"
        name="UH",
        formants=[FormantSpec(640, 1.0, 75), FormantSpec(1200, 0.7, 90), FormantSpec(2400, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.10,
    ),
    "AE": PhonemeSpec(  # /æ/ as in "cat"
        name="AE",
        formants=[FormantSpec(660, 1.0, 75), FormantSpec(1720, 0.7, 100), FormantSpec(2410, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "ER": PhonemeSpec(  # /ɝ/ as in "bird"
        name="ER",
        formants=[FormantSpec(490, 1.0, 70), FormantSpec(1350, 0.6, 90), FormantSpec(1690, 0.4, 100)],
        f0=120.0, voiced=True, duration=0.12,
    ),
    "AW": PhonemeSpec(  # /aʊ/ as in "how" — diphthong start
        name="AW",
        formants=[FormantSpec(700, 1.0, 80), FormantSpec(1100, 0.7, 90), FormantSpec(2500, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.15,
    ),
    "AY": PhonemeSpec(  # /aɪ/ as in "my" — diphthong start
        name="AY",
        formants=[FormantSpec(750, 1.0, 80), FormantSpec(1200, 0.7, 90), FormantSpec(2500, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.15,
    ),
    "OW": PhonemeSpec(  # /oʊ/ diphthong
        name="OW",
        formants=[FormantSpec(570, 1.0, 70), FormantSpec(850, 0.7, 80), FormantSpec(2400, 0.3, 120)],
        f0=120.0, voiced=True, duration=0.15,
    ),

    # === FRICATIVES ===
    "S": PhonemeSpec(  # /s/
        name="S",
        formants=[FormantSpec(5000, 0.8, 500), FormantSpec(7500, 0.5, 400), FormantSpec(10000, 0.3, 300)],
        f0=0.0, voiced=False, noise_level=0.9, duration=0.10, attack=0.02, release=0.02,
    ),
    "SH": PhonemeSpec(  # /ʃ/
        name="SH",
        formants=[FormantSpec(3000, 0.8, 400), FormantSpec(5000, 0.5, 400), FormantSpec(8000, 0.3, 300)],
        f0=0.0, voiced=False, noise_level=0.85, duration=0.10, attack=0.02, release=0.02,
    ),
    "F": PhonemeSpec(  # /f/
        name="F",
        formants=[FormantSpec(4000, 0.6, 600), FormantSpec(7000, 0.4, 500), FormantSpec(9500, 0.2, 400)],
        f0=0.0, voiced=False, noise_level=0.7, duration=0.08, attack=0.02, release=0.02,
    ),
    "V": PhonemeSpec(  # /v/ — voiced fricative
        name="V",
        formants=[FormantSpec(4000, 0.5, 500), FormantSpec(7000, 0.3, 400), FormantSpec(9500, 0.2, 400)],
        f0=120.0, voiced=True, noise_level=0.5, duration=0.08, attack=0.02, release=0.02,
    ),
    "Z": PhonemeSpec(  # /z/ — voiced fricative
        name="Z",
        formants=[FormantSpec(5000, 0.6, 500), FormantSpec(7500, 0.4, 400), FormantSpec(10000, 0.2, 300)],
        f0=120.0, voiced=True, noise_level=0.6, duration=0.10, attack=0.02, release=0.02,
    ),
    "TH": PhonemeSpec(  # /θ/ voiceless th
        name="TH",
        formants=[FormantSpec(6000, 0.5, 600), FormantSpec(8000, 0.3, 500), FormantSpec(10000, 0.2, 400)],
        f0=0.0, voiced=False, noise_level=0.6, duration=0.08, attack=0.02, release=0.02,
    ),
    "DH": PhonemeSpec(  # /ð/ voiced th
        name="DH",
        formants=[FormantSpec(6000, 0.4, 600), FormantSpec(8000, 0.2, 500), FormantSpec(10000, 0.15, 400)],
        f0=120.0, voiced=True, noise_level=0.4, duration=0.06, attack=0.01, release=0.02,
    ),

    # === PLOSIVES ===
    "P": PhonemeSpec(
        name="P", formants=[], f0=0.0, voiced=False, noise_level=0.5,
        duration=0.08, attack=0.005, release=0.01,
        is_plosive=True, plosive_burst_freq=800.0,
    ),
    "B": PhonemeSpec(
        name="B", formants=[], f0=120.0, voiced=True, noise_level=0.4,
        duration=0.08, attack=0.005, release=0.01,
        is_plosive=True, plosive_burst_freq=800.0,
    ),
    "T": PhonemeSpec(
        name="T", formants=[], f0=0.0, voiced=False, noise_level=0.6,
        duration=0.06, attack=0.003, release=0.01,
        is_plosive=True, plosive_burst_freq=3000.0,
    ),
    "D": PhonemeSpec(
        name="D", formants=[], f0=120.0, voiced=True, noise_level=0.5,
        duration=0.06, attack=0.003, release=0.01,
        is_plosive=True, plosive_burst_freq=3000.0,
    ),
    "K": PhonemeSpec(
        name="K", formants=[], f0=0.0, voiced=False, noise_level=0.6,
        duration=0.08, attack=0.005, release=0.01,
        is_plosive=True, plosive_burst_freq=1500.0,
    ),
    "G": PhonemeSpec(
        name="G", formants=[], f0=120.0, voiced=True, noise_level=0.5,
        duration=0.08, attack=0.005, release=0.01,
        is_plosive=True, plosive_burst_freq=1500.0,
    ),

    # === NASALS ===
    "M": PhonemeSpec(
        name="M",
        formants=[FormantSpec(250, 1.0, 50), FormantSpec(1000, 0.2, 80), FormantSpec(2500, 0.1, 100)],
        f0=120.0, voiced=True, duration=0.08, attack=0.01, release=0.02,
    ),
    "N": PhonemeSpec(
        name="N",
        formants=[FormantSpec(250, 1.0, 50), FormantSpec(1400, 0.2, 80), FormantSpec(2500, 0.1, 100)],
        f0=120.0, voiced=True, duration=0.06, attack=0.01, release=0.02,
    ),
    "NG": PhonemeSpec(
        name="NG",
        formants=[FormantSpec(250, 1.0, 50), FormantSpec(1100, 0.15, 80), FormantSpec(2500, 0.1, 100)],
        f0=120.0, voiced=True, duration=0.08, attack=0.01, release=0.02,
    ),

    # === LIQUIDS & GLIDES ===
    "L": PhonemeSpec(
        name="L",
        formants=[FormantSpec(350, 1.0, 60), FormantSpec(1050, 0.5, 80), FormantSpec(2400, 0.3, 100)],
        f0=120.0, voiced=True, duration=0.06, attack=0.01, release=0.02,
    ),
    "R": PhonemeSpec(
        name="R",
        formants=[FormantSpec(420, 1.0, 65), FormantSpec(1300, 0.5, 90), FormantSpec(1600, 0.4, 100)],
        f0=120.0, voiced=True, duration=0.06, attack=0.01, release=0.02,
    ),
    "W": PhonemeSpec(
        name="W",
        formants=[FormantSpec(300, 1.0, 55), FormantSpec(800, 0.6, 70), FormantSpec(2300, 0.3, 100)],
        f0=120.0, voiced=True, duration=0.06, attack=0.02, release=0.02,
    ),
    "Y": PhonemeSpec(
        name="Y",
        formants=[FormantSpec(280, 1.0, 55), FormantSpec(2200, 0.6, 90), FormantSpec(3000, 0.3, 110)],
        f0=120.0, voiced=True, duration=0.05, attack=0.02, release=0.02,
    ),

    # === SPECIAL ===
    "HH": PhonemeSpec(  # /h/
        name="HH",
        formants=[FormantSpec(500, 0.3, 200), FormantSpec(1500, 0.2, 200), FormantSpec(2500, 0.1, 200)],
        f0=0.0, voiced=False, noise_level=0.3, duration=0.06, attack=0.01, release=0.02,
    ),
    "SIL": PhonemeSpec(  # silence
        name="SIL", formants=[], f0=0.0, voiced=False, noise_level=0.0,
        duration=0.05, attack=0.0, release=0.0,
    ),
}
