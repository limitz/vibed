"""
Main entry point — generates Happy Birthday sung in flatulence and saves to MP3.
"""

from melody import happy_birthday
from renderer import render_song, save_mp3


def main():
    """Generate the flatulent Happy Birthday MP3."""
    notes = happy_birthday(base_octave=4, tempo_bpm=110.0)
    # Half octave down
    notes = [(f * 0.7071 if f > 0 else 0, d) for f, d in notes]
    audio = render_song(notes, master_volume=0.3)
    save_mp3(audio, "happy_birthday_flatulent.mp3")
    print("Saved happy_birthday_flatulent.mp3")


if __name__ == "__main__":
    main()
