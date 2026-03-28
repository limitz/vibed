#!/usr/bin/env python3
"""Hit Song Generator - Creates and records a catchy pop song to MP3."""

import os
import sys

from song_structure import create_hit_song
from melody import (generate_lead_melody, generate_bass_line,
                    generate_chord_pads, generate_drum_pattern)
from lyrics import generate_lyrics
from synthesizer import (synthesize_lead, synthesize_bass,
                         synthesize_pads, synthesize_drums)
from mixer import mix_tracks, master
from exporter import export_mp3


def main():
    """Generate a hit song and export to MP3."""
    print("🎵 Hit Song Generator 🎵")
    print("=" * 40)

    # Step 1: Create song structure
    print("\n📝 Creating song structure...")
    song = create_hit_song()
    print(f"  Title: {song.title}")
    print(f"  Key: {song.key}")
    print(f"  Tempo: {song.tempo} BPM")
    print(f"  Duration: {song.total_duration:.1f}s")

    # Step 2: Generate lyrics
    print("\n✍️  Generating lyrics...")
    lyrics = generate_lyrics(song)
    for section_name, lines in lyrics.items():
        print(f"\n  [{section_name}]")
        for line in lines:
            print(f"    {line}")

    # Step 3: Generate musical parts
    print("\n🎹 Generating melody...")
    lead_notes = generate_lead_melody(song)
    print(f"  Lead: {len(lead_notes)} notes")

    print("🎸 Generating bass line...")
    bass_notes = generate_bass_line(song)
    print(f"  Bass: {len(bass_notes)} notes")

    print("🎹 Generating chord pads...")
    chord_notes = generate_chord_pads(song)
    print(f"  Chords: {len(chord_notes)} chord events")

    print("🥁 Generating drums...")
    drum_hits = generate_drum_pattern(song)
    print(f"  Drums: {len(drum_hits)} hits")

    # Step 4: Synthesize audio
    print("\n🔊 Synthesizing audio...")
    sr = song.sample_rate
    lead_audio = synthesize_lead(lead_notes, sr)
    bass_audio = synthesize_bass(bass_notes, sr)
    pad_audio = synthesize_pads(chord_notes, sr)
    drum_audio = synthesize_drums(drum_hits, sr)

    # Step 5: Mix
    print("🎛️  Mixing tracks...")
    tracks = [
        (lead_audio, 0.7),
        (bass_audio, 0.8),
        (pad_audio, 0.4),
        (drum_audio, 0.9),
    ]
    mixed = mix_tracks(tracks, sr)

    # Step 6: Master
    print("🎚️  Mastering...")
    mastered = master(mixed, sr)

    # Step 7: Export
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "hitsong.mp3")
    print(f"\n💿 Exporting to {output_file}...")
    result = export_mp3(mastered, output_file, sr)
    print(f"\n✅ Done! Your hit song is ready: {result}")


if __name__ == "__main__":
    main()
