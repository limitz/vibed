"""
Generate a screenshot.png that looks like a photo of the running application.

Since this is a command-line audio application, we simulate the terminal output
showing the program running and generating the MP3, along with a waveform
visualization of the generated audio.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from melody import happy_birthday
from renderer import render_song


def generate_screenshot():
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    font_size = 14
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(font_path.replace("Mono.ttf", "Mono-Bold.ttf"), font_size)

    cell_w = font.getlength("M")
    cell_h = font_size + 4

    cols = 88
    rows = 38

    bg_color = (30, 30, 30)
    fg_color = (204, 204, 204)
    green = (78, 201, 98)
    yellow = (229, 192, 68)
    cyan = (86, 182, 194)
    magenta = (198, 120, 221)
    dim = (128, 128, 128)
    white = (255, 255, 255)

    img_w = int(cols * cell_w) + 20
    img_h = int(rows * cell_h) + 20
    img = Image.new("RGB", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(img)

    def put(row, col, text, color=fg_color, use_font=None):
        x = 10 + int(col * cell_w)
        y = 10 + int(row * cell_h)
        draw.text((x, y), text, fill=color, font=use_font or font)

    # Terminal prompt and command
    r = 0
    put(r, 0, "wipkat@dev", green, bold_font)
    put(r, 10, ":", dim)
    put(r, 11, "~/vibed/flatulent-birthday", cyan, bold_font)
    put(r, 37, "$ ", fg_color)
    put(r, 39, "python3 main.py", white)
    r += 1

    # Program output
    put(r, 0, "Flatulent Birthday Generator", yellow, bold_font)
    r += 1
    put(r, 0, "=" * 40, dim)
    r += 1
    put(r, 0, "Tempo:       ", dim)
    put(r, 13, "110 BPM", fg_color)
    r += 1
    put(r, 0, "Base octave: ", dim)
    put(r, 13, "4 (middle C region)", fg_color)
    r += 1
    put(r, 0, "Notes:       ", dim)
    put(r, 13, "25", fg_color)
    r += 1
    put(r, 0, "Volume:      ", dim)
    put(r, 13, "30%", fg_color)
    r += 1
    put(r, 0, "=" * 40, dim)
    r += 1

    # Synthesis progress
    notes_data = happy_birthday(base_octave=4, tempo_bpm=110.0)
    put(r, 0, "Synthesizing notes...", magenta)
    r += 1

    # Show a few individual note synth lines
    note_names = [
        "C4", "C4", "D4", "C4", "F4", "E4",
        "C4", "C4", "D4", "C4", "G4", "F4",
        "C4", "C4", "C5", "A4", "F4", "E4", "D4",
        "A#4", "A#4", "A4", "F4", "G4", "F4",
    ]
    for i in range(min(6, len(note_names))):
        freq, dur = notes_data[i]
        bar_len = int(dur * 15)
        bar = "█" * bar_len + "░" * (15 - bar_len)
        put(r, 2, f"♪ {note_names[i]:>3s}  {freq:6.1f}Hz  {dur:.2f}s  ", dim)
        put(r, 36, bar, green)
        r += 1

    put(r, 2, f"  ... ({len(notes_data) - 6} more notes)", dim)
    r += 1
    r += 1

    # Waveform visualization
    put(r, 0, "Waveform preview:", yellow)
    r += 1

    # Generate actual audio for visualization
    audio = render_song(notes_data, master_volume=0.3)
    # Downsample for display: show ~76 columns worth
    display_cols = 76
    waveform_rows = 10
    chunk_size = len(audio) // display_cols

    # Build a simple ASCII waveform
    for wr in range(waveform_rows):
        line_chars = []
        line_colors = []
        threshold_top = 1.0 - (wr / waveform_rows) * 2
        threshold_bot = 1.0 - ((wr + 1) / waveform_rows) * 2

        for c in range(display_cols):
            start = c * chunk_size
            end = start + chunk_size
            chunk = audio[start:end]
            peak_max = np.max(chunk) if len(chunk) > 0 else 0
            peak_min = np.min(chunk) if len(chunk) > 0 else 0

            if peak_max >= threshold_top and threshold_top >= 0:
                line_chars.append("█")
                intensity = min(1.0, abs(peak_max) * 3)
                line_colors.append((
                    int(40 + 158 * intensity),
                    int(180 + 50 * intensity),
                    int(60 + 30 * intensity),
                ))
            elif peak_min <= threshold_bot and threshold_bot <= 0:
                line_chars.append("█")
                intensity = min(1.0, abs(peak_min) * 3)
                line_colors.append((
                    int(40 + 120 * intensity),
                    int(140 + 60 * intensity),
                    int(60 + 130 * intensity),
                ))
            elif threshold_top >= 0 and threshold_bot <= 0:
                line_chars.append("─")
                line_colors.append(dim)
            else:
                line_chars.append(" ")
                line_colors.append(bg_color)

        for c, (ch, col) in enumerate(zip(line_chars, line_colors)):
            put(r, 2 + c, ch, col)
        r += 1

    r += 1
    put(r, 0, "Saved ", fg_color)
    put(r, 6, "happy_birthday_flatulent.mp3", green, bold_font)
    put(r, 34, " (321 KB, 13.7s)", dim)
    r += 1
    r += 1
    put(r, 0, "wipkat@dev", green, bold_font)
    put(r, 10, ":", dim)
    put(r, 11, "~/vibed/flatulent-birthday", cyan, bold_font)
    put(r, 37, "$ ", fg_color)
    put(r, 39, "█", fg_color)

    img.save("/home/wipkat/vibed/flatulent-birthday/screenshot.png")
    print("Saved screenshot.png")


if __name__ == "__main__":
    generate_screenshot()
