"""Generate screenshot.png — a realistic terminal screenshot of SpeakUp running."""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


def get_mono_font(size: int):
    """Try to find a monospace font."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_waveform(draw: ImageDraw.ImageDraw, samples: np.ndarray,
                    x: int, y: int, width: int, height: int,
                    color: tuple):
    """Draw a waveform visualization."""
    if len(samples) == 0:
        return
    # Downsample to width
    step = max(1, len(samples) // width)
    downsampled = samples[::step][:width]
    mid_y = y + height // 2

    for i in range(len(downsampled) - 1):
        y1 = int(mid_y - downsampled[i] * (height // 2) * 0.9)
        y2 = int(mid_y - downsampled[i + 1] * (height // 2) * 0.9)
        draw.line([(x + i, y1), (x + i + 1, y2)], fill=color, width=1)


def render_spectrogram_bar(draw: ImageDraw.ImageDraw, samples: np.ndarray,
                           x: int, y: int, width: int, height: int):
    """Draw a simple spectrogram-like frequency visualization."""
    if len(samples) < 512:
        return
    # Take chunks and compute FFT magnitudes
    chunk_size = 512
    n_chunks = min(width, len(samples) // chunk_size)
    if n_chunks == 0:
        return

    n_freq_bins = height
    for i in range(n_chunks):
        start = i * (len(samples) // n_chunks)
        chunk = samples[start:start + chunk_size]
        if len(chunk) < chunk_size:
            break
        fft = np.abs(np.fft.rfft(chunk))[:n_freq_bins]
        fft = fft / (np.max(fft) + 1e-10)

        col_x = x + int(i * width / n_chunks)
        for j in range(min(len(fft), n_freq_bins)):
            intensity = fft[j]
            r = int(20 + intensity * 200)
            g = int(intensity * 255 * 0.6)
            b = int(40 + intensity * 100)
            draw.point((col_x, y + n_freq_bins - 1 - j), fill=(r, g, b))


def main():
    # Terminal dimensions
    font_size = 14
    font = get_mono_font(font_size)
    # Measure character cell
    bbox = font.getbbox("M")
    char_w = bbox[2] - bbox[0]
    char_h = int(font_size * 1.5)

    cols = 80
    rows = 38
    padding = 8

    img_w = cols * char_w + padding * 2
    img_h = rows * char_h + padding * 2

    bg_color = (18, 18, 24)
    img = Image.new("RGB", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(img)

    # Colors
    GREEN = (80, 220, 100)
    CYAN = (80, 200, 220)
    YELLOW = (220, 200, 80)
    WHITE = (200, 200, 210)
    DIM = (100, 100, 120)
    MAGENTA = (180, 100, 220)
    ORANGE = (220, 150, 60)
    BLUE = (80, 140, 240)

    def put(row, col, text, color=WHITE):
        x = padding + col * char_w
        y = padding + row * char_h
        draw.text((x, y), text, fill=color, font=font)

    # Title bar
    draw.rectangle([(0, 0), (img_w, char_h + padding)], fill=(40, 30, 60))
    put(0, 1, "$ python -m speakup.main", CYAN)

    # Output
    put(2, 0, "SpeakUp: Learning to speak with FM synthesis...", GREEN)
    put(3, 0, "", DIM)

    # Stage outputs
    stages = [
        ("Stage 1:", "Raw FM tones...", "01_raw_fm_tones.wav", "3.9s"),
        ("Stage 2:", "Vowels...", "02_vowels.wav", "4.8s"),
        ("Stage 3:", "Babbling...", "03_babbling.wav", "4.3s"),
        ("Stage 4:", "First words...", "04_first_words.wav", "4.2s"),
        ("Stage 5:", "Speaking...", "05_speaking.wav", "5.2s"),
        ("Stage 6:", "The prompt...", "06_the_prompt.wav", "4.7s"),
    ]

    row = 4
    for label, desc, filename, dur in stages:
        put(row, 2, label, YELLOW)
        put(row, 2 + len(label) + 1, desc, WHITE)
        row += 1
        put(row, 4, f"-> output/{filename} ({dur})", DIM)
        row += 2

    # "Done" message
    put(row, 0, "Done! Generated 6 audio files in output/", GREEN)
    row += 2

    # Waveform visualizations section
    put(row, 0, "--- Waveform Preview: Stage 6 (The Prompt) ---", MAGENTA)
    row += 1

    # Generate actual audio for visualization
    from speakup.text_to_phoneme import text_to_phonemes
    from speakup.speech import render_utterance
    from speakup.exporter import normalize

    phonemes = text_to_phonemes("Using only FM synthesis learn how to speak")
    audio = render_utterance(phonemes, 44100, f0_base=115.0, speed=0.7)
    audio = normalize(audio, 0.9)

    # Draw waveform
    wave_x = padding + 2 * char_w
    wave_y = padding + row * char_h
    wave_w = img_w - padding * 2 - 4 * char_w
    wave_h = 4 * char_h
    render_waveform(draw, audio, wave_x, wave_y, wave_w, wave_h, CYAN)
    row += 5

    # Draw spectrogram
    put(row, 0, "--- Spectrogram ---", MAGENTA)
    row += 1
    spec_x = padding + 2 * char_w
    spec_y = padding + row * char_h
    spec_h = 4 * char_h
    render_spectrogram_bar(draw, audio, spec_x, spec_y, wave_w, spec_h)
    row += 5

    # Phoneme sequence
    put(row, 0, "Phonemes:", ORANGE)
    phoneme_str = " ".join(phonemes[:30])
    put(row, 10, phoneme_str[:cols - 11], BLUE)
    row += 1
    if len(phonemes) > 30:
        phoneme_str2 = " ".join(phonemes[30:])
        put(row, 10, phoneme_str2[:cols - 11], BLUE)

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "screenshot.png")
    img.save(out_path)
    print(f"Screenshot saved to {out_path}")


if __name__ == "__main__":
    main()
