# song_builder.py - Multi-Track Song Builder
# Combines the metrics-driven melody, a matching bass line, and a genre-fusion harmony layer
# into a single multi-track MIDI file — your complete daily Symphony of Order.

import argparse
import datetime
import random

from midiutil import MIDIFile

from data_to_melody import SCALES
from genre_fusion import GENRE_PROFILES, ALL_GENRES

# Track assignments
TRACK_MELODY = 0
TRACK_BASS = 1
TRACK_HARMONY = 2


def build_song(
    power_saved_kwh=7.8,
    water_saved_liters=1850,
    genre="classical",
    bars=16,
    tempo=88,
    filename=None,
    scale_name="major",
):
    """Compose a multi-track MIDI from environmental metrics and a chosen genre.

    Tracks:
      0 — Melody  : metrics-driven lead line (from data_to_melody logic)
      1 — Bass    : low-octave counterpart to the melody
      2 — Harmony : genre-fusion chords and fill notes

    Args:
        power_saved_kwh (float): Kilowatt-hours of power saved today.
        water_saved_liters (float): Liters of water protected today.
        genre (str): Genre profile to use for harmony. See genre_fusion.GENRE_PROFILES.
        bars (int): Number of bars to generate.
        tempo (int): BPM for the whole composition.
        filename (str | None): Output MIDI path. Defaults to ``song_YYYY-MM-DD.mid``.
        scale_name (str): Melodic scale. One of: major, minor, pentatonic, dorian, mixolydian.

    Returns:
        str: Path to the written MIDI file.
    """
    if genre not in GENRE_PROFILES:
        raise ValueError(f"Unknown genre '{genre}'. Choose from: {', '.join(ALL_GENRES)}")

    today = datetime.date.today()
    if filename is None:
        filename = f"song_{today}.mid"

    scale = SCALES.get(scale_name, SCALES["major"])
    scale_len = len(scale)
    profile = GENRE_PROFILES[genre]
    genre_scale = profile["scale"]

    midi = MIDIFile(3)
    for t in range(3):
        midi.addTempo(t, 0, tempo)

    # ── Track 0: Melody ──────────────────────────────────────────────────────
    note_duration = max(0.5, min(2.0, water_saved_liters / 1000))
    base_index = int((power_saved_kwh / 20.0) * scale_len) % scale_len
    melody_vel = min(127, int(60 + power_saved_kwh * 8))

    for i in range(bars):
        pitch_index = (base_index + i) % scale_len
        pitch = scale[pitch_index] + random.randint(-1, 1)
        pitch = max(0, min(127, pitch))
        vel = min(127, max(1, melody_vel + random.randint(-5, 5)))
        midi.addNote(TRACK_MELODY, 0, pitch, i * 0.5, note_duration, vel)

    # ── Track 1: Bass ────────────────────────────────────────────────────────
    bass_vel = max(1, melody_vel - 25)
    for i in range(0, bars, 2):  # half-time bass feel
        pitch_index = (base_index + i) % scale_len
        bass_pitch = max(0, scale[pitch_index] - 12)
        midi.addNote(TRACK_BASS, 1, bass_pitch, i * 0.5, note_duration * 2, bass_vel)

    # ── Track 2: Genre-Harmony ───────────────────────────────────────────────
    subdivisions = profile["subdivisions"]
    bar_dur = 4.0
    beat_step = bar_dur / (4 * subdivisions)
    harm_vel_base = profile["velocity"]
    harm_duration = profile["duration"] or 1.0

    time = 0.0
    for _bar in range(bars):
        for sub in range(4 * subdivisions):
            pitch = random.choice(genre_scale) + random.randint(-2, 2)
            pitch = max(0, min(127, pitch))
            hv = min(127, max(1, harm_vel_base + random.randint(-10, 10)))
            dur = min(harm_duration, beat_step * 2)
            midi.addNote(TRACK_HARMONY, 2, pitch, time, dur, hv)

            # Chord voicing on beat 1 for classical/ambient
            if genre in ("classical", "ambient") and sub == 0:
                for interval in (4, 7):  # third + fifth
                    chord_p = max(0, min(127, pitch + interval))
                    midi.addNote(TRACK_HARMONY, 2, chord_p, time, dur * 1.5, max(1, hv - 20))

            time += beat_step

    with open(filename, "wb") as f:
        midi.writeFile(f)

    print(f"🎼 Song built: {filename}")
    print(f"   Scale: {scale_name} | Genre harmony: {genre} | Tempo: {tempo} BPM | Bars: {bars}")
    print(f"   Power saved: {power_saved_kwh} kWh  |  Water saved: {water_saved_liters} L")

    return filename


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Compose a multi-track MIDI from daily environmental savings data."
    )
    parser.add_argument("--power", type=float, default=7.8, metavar="KWH",
                        help="Kilowatt-hours of power saved (default: 7.8)")
    parser.add_argument("--water", type=float, default=1850, metavar="LITERS",
                        help="Liters of water protected (default: 1850)")
    parser.add_argument("--genre", type=str, default="classical", choices=ALL_GENRES,
                        metavar="GENRE",
                        help=f"Genre for the harmony layer (default: classical). "
                             f"Available: {', '.join(ALL_GENRES)}")
    parser.add_argument("--scale", type=str, default="major", choices=list(SCALES.keys()),
                        metavar="SCALE",
                        help="Melodic scale (default: major)")
    parser.add_argument("--bars", type=int, default=16, metavar="N",
                        help="Number of bars to generate (default: 16)")
    parser.add_argument("--tempo", type=int, default=88, metavar="BPM",
                        help="Tempo in BPM (default: 88)")
    parser.add_argument("--output", type=str, default=None, metavar="FILE",
                        help="Output MIDI filename (default: song_YYYY-MM-DD.mid)")
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    build_song(
        power_saved_kwh=args.power,
        water_saved_liters=args.water,
        genre=args.genre,
        scale_name=args.scale,
        bars=args.bars,
        tempo=args.tempo,
        filename=args.output,
    )
