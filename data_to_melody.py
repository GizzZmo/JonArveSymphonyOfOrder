# data_to_melody.py - Sonification Engine
# Turns daily power-consumption savings or water-saving metrics into generative MIDI melodies.
# Run daily to hear the music of planetary healing.

import argparse
import csv
import datetime
import json
import random
import subprocess

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
    dry_run=False,
):
    """Generate a MIDI melody from environmental savings data.

    Args:
        power_saved_kwh (float): Kilowatt-hours of power saved today.
        water_saved_liters (float): Liters of water protected today.
        filename (str): Output MIDI file path.
        scale_name (str): Scale to use. One of: major, minor, pentatonic, dorian, mixolydian.
        tempo (int): BPM for the generated MIDI (default 88 — heartbeat of service).
        bars (int): Number of melodic bars to generate.
        dry_run (bool): If True, return notes without writing a MIDI file.

    Returns:
        list[dict]: List of note dicts with keys: pitch, time, duration, velocity.
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

    notes = []
    notes_generated = 0
    for i in range(bars):
        # Walk through the scale, nudged by iteration to create melodic movement
        pitch_index = (base_index + i) % scale_len
        pitch = scale[pitch_index] + random.randint(-1, 1)  # subtle micro-variation
        pitch = max(0, min(127, pitch))

        # Velocity = impact strength, capped at 127
        vel = min(127, int(60 + power_saved_kwh * 8))

        note_time = time + i * 0.5
        midi.addNote(track, channel, pitch, note_time, duration, vel)
        notes.append({"pitch": pitch, "time": note_time, "duration": duration, "velocity": vel})
        notes_generated += 1

        # Bass note every 4 bars for harmonic grounding
        if i % 4 == 0:
            bass_pitch = max(0, pitch - 12)
            bass_dur = duration * 2
            bass_vel = max(1, vel - 20)
            midi.addNote(track, channel, bass_pitch, note_time, bass_dur, bass_vel)
            notes.append({"pitch": bass_pitch, "time": note_time, "duration": bass_dur, "velocity": bass_vel})

    if not dry_run:
        with open(filename, "wb") as output_file:
            midi.writeFile(output_file)

        print(f"🎵 Melody generated: {filename}")
        print(f"   Scale: {scale_name} | Tempo: {tempo} BPM | Bars: {bars}")
        print(f"   Power saved: {power_saved_kwh} kWh → {notes_generated} notes of hope")
        print(f"   Water saved: {water_saved_liters} L → note duration {duration:.2f} beats")

    return notes


def _load_csv(filepath, fmt="default", date_filter=None):
    """Load power/water rows from a CSV file.

    Args:
        filepath (str): Path to the CSV file.
        fmt (str): Format variant: 'default' (date,power_kwh,water_liters) or 'tibber' (Consumption(kWh),Date).
        date_filter (str | None): Only return rows matching this date string (YYYY-MM-DD).

    Returns:
        list[dict]: Each dict has keys 'date', 'power_kwh', 'water_liters'.
    """
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if fmt == "tibber":
                rows.append({
                    "date": row.get("Date", ""),
                    "power_kwh": float(row.get("Consumption(kWh)", 0) or 0),
                    "water_liters": 0.0,
                })
            else:
                rows.append({
                    "date": row.get("date", ""),
                    "power_kwh": float(row.get("power_kwh", 0) or 0),
                    "water_liters": float(row.get("water_liters", 0) or 0),
                })

    if date_filter:
        rows = [r for r in rows if r["date"] == date_filter]
    return rows


def _load_json(filepath, fmt="default", date_filter=None):
    """Load power/water rows from a JSON file.

    Args:
        filepath (str): Path to the JSON file.
        fmt (str): Format variant: 'default' or 'homeassistant' (state/last_changed fields).
        date_filter (str | None): Only return rows matching this date string (YYYY-MM-DD).

    Returns:
        list[dict]: Each dict has keys 'date', 'power_kwh', 'water_liters'.
    """
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    rows = []
    for entry in data:
        if fmt == "homeassistant":
            raw_date = entry.get("last_changed", "")
            date_str = raw_date[:10] if raw_date else ""
            try:
                power = float(entry.get("state", 0) or 0)
            except ValueError:
                power = 0.0
            rows.append({"date": date_str, "power_kwh": power, "water_liters": 0.0})
        else:
            rows.append({
                "date": entry.get("date", ""),
                "power_kwh": float(entry.get("power_kwh", 0) or 0),
                "water_liters": float(entry.get("water_liters", 0) or 0),
            })

    if date_filter:
        rows = [r for r in rows if r["date"] == date_filter]
    return rows


def _filter_date_range(rows, start_date=None, end_date=None):
    """Return only rows whose date falls within [start_date, end_date]."""
    if start_date is None and end_date is None:
        return rows
    result = []
    for row in rows:
        try:
            d = datetime.date.fromisoformat(row["date"])
            if (start_date is None or d >= start_date) and (end_date is None or d <= end_date):
                result.append(row)
        except (ValueError, TypeError):
            pass
    return result


def _play_midi(filepath):
    """Attempt to play a MIDI file using FluidSynth."""
    try:
        subprocess.run(["fluidsynth", "-ni", "soundfont.sf2", filepath], check=True)
    except FileNotFoundError:
        print("⚠  FluidSynth not found. Install with: apt install fluidsynth (or brew install fluidsynth)")
        print("   Then place a soundfont at soundfont.sf2 (e.g., GeneralUser GS or FluidR3_GM).")
    except subprocess.CalledProcessError:
        print("⚠  FluidSynth could not play the file.")
        print("   Make sure soundfont.sf2 exists in the current directory.")


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
    # Phase 4: data input
    parser.add_argument("--csv", type=str, default=None,
                        metavar="FILE", help="CSV file with columns date,power_kwh,water_liters")
    parser.add_argument("--json", type=str, default=None,
                        metavar="FILE", help="JSON file with keys power_kwh and water_liters (or array)")
    parser.add_argument("--date", type=str, default=None,
                        metavar="YYYY-MM-DD", help="Select a specific date row from CSV/JSON input")
    parser.add_argument("--format", type=str, default="default",
                        choices=["default", "tibber", "homeassistant"],
                        help="Input file format: default, tibber, homeassistant (default: default)")
    parser.add_argument("--batch", action="store_true",
                        help="Generate one MIDI per date entry in the input file")
    parser.add_argument("--start", type=str, default=None,
                        metavar="YYYY-MM-DD", help="Batch start date inclusive (requires --batch)")
    parser.add_argument("--end", type=str, default=None,
                        metavar="YYYY-MM-DD", help="Batch end date inclusive (requires --batch)")
    # Phase 5: visualization and playback
    parser.add_argument("--dry-run", action="store_true",
                        help="Print piano-roll to terminal instead of writing a file")
    parser.add_argument("--play", action="store_true",
                        help="Play the generated MIDI with FluidSynth after writing")
    return parser


def _run_generation(power, water, outfile, scale, tempo, bars, dry_run, play):
    """Run a single melody generation with optional dry-run and playback."""
    notes = generate_melody_from_data(
        power_saved_kwh=power,
        water_saved_liters=water,
        filename=outfile,
        scale_name=scale,
        tempo=tempo,
        bars=bars,
        dry_run=dry_run,
    )
    if dry_run:
        from visualizer import piano_roll
        piano_roll(notes, scale)
    elif play:
        _play_midi(outfile)
    return notes


if __name__ == "__main__":
    args = _build_parser().parse_args()
    today = datetime.date.today()

    rows = None
    if args.csv:
        rows = _load_csv(args.csv, args.format, args.date)
    elif args.json:
        rows = _load_json(args.json, args.format, args.date)

    if rows is not None and args.batch:
        start_d = datetime.date.fromisoformat(args.start) if args.start else None
        end_d = datetime.date.fromisoformat(args.end) if args.end else None
        rows = _filter_date_range(rows, start_d, end_d)
        for row in rows:
            date_str = row.get("date") or today.isoformat()
            outfile = f"order_{date_str}.mid"
            _run_generation(row["power_kwh"], row["water_liters"], outfile,
                            args.scale, args.tempo, args.bars, args.dry_run, args.play)
    elif rows is not None:
        row = rows[0] if rows else {"power_kwh": args.power, "water_liters": args.water, "date": ""}
        date_str = row.get("date") or today.isoformat()
        outfile = args.output or f"order_{date_str}.mid"
        _run_generation(row["power_kwh"], row["water_liters"], outfile,
                        args.scale, args.tempo, args.bars, args.dry_run, args.play)
    else:
        outfile = args.output or f"order_{today}.mid"
        _run_generation(args.power, args.water, outfile,
                        args.scale, args.tempo, args.bars, args.dry_run, args.play)
