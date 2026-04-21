# data_to_melody.py - Sonification Engine
# Turns daily power-consumption savings or water-saving metrics into generative MIDI melodies.
# Run daily to hear the music of planetary healing.

import argparse
import datetime
import random

from midiutil import MIDIFile

# Named scale definitions (MIDI note offsets from C4 = 60)
SCALES = {
    "major":       [60, 62, 64, 65, 67, 69, 71, 72, 74, 76],  # C major
    "minor":       [60, 62, 63, 65, 67, 68, 70, 72, 74, 75],  # C natural minor
    "pentatonic":  [60, 62, 64, 67, 69, 72, 74, 76, 79, 81],  # C major pentatonic
    "dorian":      [60, 62, 63, 65, 67, 69, 70, 72, 74, 75],  # C dorian
    "mixolydian":  [60, 62, 64, 65, 67, 69, 70, 72, 74, 76],  # C mixolydian
}


def generate_melody_from_data(
    power_saved_kwh=5.2,
    water_saved_liters=1200,
    filename="symphony_of_order.mid",
    scale_name="major",
    tempo=88,
    bars=16,
):
    """Generate a MIDI melody from environmental savings data.

    Args:
        power_saved_kwh (float): Kilowatt-hours of power saved today.
        water_saved_liters (float): Liters of water protected today.
        filename (str): Output MIDI file path.
        scale_name (str): Scale to use. One of: major, minor, pentatonic, dorian, mixolydian.
        tempo (int): BPM for the generated MIDI (default 88 — heartbeat of service).
        bars (int): Number of melodic bars to generate.
    """
    scale = SCALES.get(scale_name, SCALES["major"])

    track = 0
    channel = 0
    time = 0

    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)

    # Duration based on water savings (longer notes = more gratitude)
    duration = max(0.5, min(2.0, water_saved_liters / 1000))

    # Spread the starting pitch across the scale using power saved
    scale_len = len(scale)
    base_index = int((power_saved_kwh / 20.0) * scale_len) % scale_len

    notes_generated = 0
    for i in range(bars):
        # Walk through the scale, nudged by iteration to create melodic movement
        pitch_index = (base_index + i) % scale_len
        pitch = scale[pitch_index] + random.randint(-1, 1)  # subtle micro-variation
        pitch = max(0, min(127, pitch))

        # Velocity = impact strength, capped at 127
        vel = min(127, int(60 + power_saved_kwh * 8))

        midi.addNote(track, channel, pitch, time + i * 0.5, duration, vel)
        notes_generated += 1

        # Bass note every 4 bars for harmonic grounding
        if i % 4 == 0:
            bass_pitch = max(0, pitch - 12)
            midi.addNote(track, channel, bass_pitch, time + i * 0.5, duration * 2, max(1, vel - 20))

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

    print(f"🎵 Melody generated: {filename}")
    print(f"   Scale: {scale_name} | Tempo: {tempo} BPM | Bars: {bars}")
    print(f"   Power saved: {power_saved_kwh} kWh → {notes_generated} notes of hope")
    print(f"   Water saved: {water_saved_liters} L → note duration {duration:.2f} beats")


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Generate a MIDI melody from daily environmental savings data."
    )
    parser.add_argument("--power", type=float, default=7.8,
                        metavar="KWH", help="Kilowatt-hours of power saved (default: 7.8)")
    parser.add_argument("--water", type=float, default=1850,
                        metavar="LITERS", help="Liters of water protected (default: 1850)")
    parser.add_argument("--output", type=str, default=None,
                        metavar="FILE", help="Output MIDI filename (default: order_YYYY-MM-DD.mid)")
    parser.add_argument("--scale", type=str, default="major",
                        choices=list(SCALES.keys()),
                        help="Musical scale to use (default: major)")
    parser.add_argument("--tempo", type=int, default=88,
                        metavar="BPM", help="Tempo in BPM (default: 88)")
    parser.add_argument("--bars", type=int, default=16,
                        metavar="N", help="Number of melodic bars to generate (default: 16)")
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    today = datetime.date.today()
    output_file = args.output or f"order_{today}.mid"
    generate_melody_from_data(
        power_saved_kwh=args.power,
        water_saved_liters=args.water,
        filename=output_file,
        scale_name=args.scale,
        tempo=args.tempo,
        bars=args.bars,
    )
