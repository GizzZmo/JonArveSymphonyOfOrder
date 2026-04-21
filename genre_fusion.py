# genre_fusion.py - Algorithmic Genre Fusion
# Blends classical, jazz, rock, electronic, blues, and ambient styles into a single MIDI composition.

import argparse
import random

from midiutil import MIDIFile

# Per-genre configuration: (scale_offsets_from_C4, note_duration, velocity, subdivisions_per_beat)
GENRE_PROFILES = {
    "classical": {
        "scale": [60, 62, 64, 65, 67, 69, 71, 72],  # C major
        "duration": 2.0,
        "velocity": 90,
        "subdivisions": 1,  # whole/half notes feel
    },
    "jazz": {
        "scale": [60, 63, 65, 67, 70, 72],  # minor-blues / Dorian tones
        "duration": None,  # randomised per note
        "velocity": 110,
        "subdivisions": 2,  # swing feel
    },
    "rock": {
        "scale": [60, 62, 64, 67, 69, 72],  # pentatonic
        "duration": 0.5,
        "velocity": 127,
        "subdivisions": 4,  # driving 16ths
    },
    "electronic": {
        "scale": [60, 62, 64, 65, 67, 69, 71, 72],
        "duration": 1.0,
        "velocity": 100,
        "subdivisions": 2,
    },
    "blues": {
        "scale": [60, 63, 65, 66, 67, 70, 72],  # blues scale
        "duration": None,
        "velocity": 105,
        "subdivisions": 3,  # triplet shuffle
    },
    "ambient": {
        "scale": [60, 62, 64, 67, 69, 72, 74],  # major pentatonic (sparse)
        "duration": 3.0,
        "velocity": 65,
        "subdivisions": 1,
    },
}

ALL_GENRES = list(GENRE_PROFILES.keys())


def fuse_genres(genres=None, bars=8, filename="fusion_order.mid", tempo=None):
    """Algorithmically blend multiple musical genres into a MIDI file.

    Args:
        genres (list[str]): Genres to blend. Supported: classical, jazz, rock, electronic, blues, ambient.
        bars (int): Number of bars to generate.
        filename (str): Output MIDI file path.
        tempo (int | None): BPM. If None, a genre-appropriate tempo is chosen randomly.
    """
    if genres is None:
        genres = ["classical", "jazz", "rock", "electronic"]

    for g in genres:
        if g not in GENRE_PROFILES:
            raise ValueError(f"Unknown genre '{g}'. Choose from: {', '.join(ALL_GENRES)}")

    if tempo is None:
        tempo = random.randint(72, 120)

    # Two tracks: melody (0) and harmony (1)
    midi = MIDIFile(2)
    midi.addTempo(0, 0, tempo)
    midi.addTempo(1, 0, tempo)

    melody_time = 0.0
    harmony_time = 0.0

    for _bar in range(bars):
        genre = random.choice(genres)
        profile = GENRE_PROFILES[genre]
        scale = profile["scale"]
        base_velocity = profile["velocity"]
        subdivisions = profile["subdivisions"]
        bar_duration = 4.0  # always 4 beats per bar

        beat_step = bar_duration / (4 * subdivisions)

        for sub in range(4 * subdivisions):
            duration = profile["duration"] or random.uniform(0.4, 1.2)
            duration = min(duration, beat_step * 2)  # prevent note overlap

            pitch = random.choice(scale) + random.randint(-2, 2)
            pitch = max(0, min(127, pitch))
            velocity = min(127, max(1, base_velocity + random.randint(-10, 10)))

            midi.addNote(0, 0, pitch, melody_time, duration, velocity)

            # Harmony layer for jazz/electronic/blues: octave-up ghost notes
            if genre in ("jazz", "electronic", "blues") and sub % 2 == 1:
                harm_pitch = max(0, min(127, pitch + 12))
                harm_vel = max(1, velocity - 35)
                midi.addNote(1, 1, harm_pitch, melody_time + beat_step * 0.5, duration * 0.5, harm_vel)

            # Classical/ambient: add a chord (third + fifth) on beat 1 of each bar
            if genre in ("classical", "ambient") and sub == 0:
                third = max(0, min(127, pitch + 4))
                fifth = max(0, min(127, pitch + 7))
                chord_vel = max(1, velocity - 20)
                midi.addNote(1, 1, third, harmony_time, duration * 2, chord_vel)
                midi.addNote(1, 1, fifth, harmony_time, duration * 2, chord_vel)

            melody_time += beat_step

        harmony_time += bar_duration

    with open(filename, "wb") as f:
        midi.writeFile(f)

    print(f"🔥 Fusion masterpiece created: {filename}")
    print(f"   Genres: {', '.join(genres)} | Bars: {bars} | Tempo: {tempo} BPM")


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Algorithmically blend multiple musical genres into a single MIDI composition."
    )
    parser.add_argument("--genres", nargs="+", default=["classical", "jazz", "rock", "electronic"],
                        choices=ALL_GENRES, metavar="GENRE",
                        help=(f"Genres to blend (default: classical jazz rock electronic). "
                              f"Available: {', '.join(ALL_GENRES)}"))
    parser.add_argument("--bars", type=int, default=16, metavar="N",
                        help="Number of bars to generate (default: 16)")
    parser.add_argument("--output", type=str, default="fusion_order.mid", metavar="FILE",
                        help="Output MIDI filename (default: fusion_order.mid)")
    parser.add_argument("--tempo", type=int, default=None, metavar="BPM",
                        help="Tempo in BPM (default: random 72–120)")
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    fuse_genres(
        genres=args.genres,
        bars=args.bars,
        filename=args.output,
        tempo=args.tempo,
    )
