# visualizer.py - ASCII Piano Roll Visualization
# Prints a terminal piano-roll preview of generated MIDI note lists.

from data_to_melody import SCALES


def piano_roll(notes, scale_name="major"):
    """Print an ASCII piano-roll of a note list to stdout.

    Each row represents a 0.5-beat time step. Columns correspond to pitches
    present in the selected scale. Active notes are shown as ' * ', rests as ' . '.

    Args:
        notes (list[dict]): Note dicts with keys: pitch, time, duration, velocity.
        scale_name (str): Name of the scale to use as column headers.
    """
    scale = SCALES.get(scale_name, SCALES["major"])

    if not notes:
        print("(no notes to display)")
        return

    max_time = max(n["time"] + n["duration"] for n in notes)
    steps = max(1, int(max_time / 0.5) + 1)

    header = "Time  | " + " ".join(f"{p:3}" for p in scale)
    separator = "-" * len(header)

    print(f"\n🎹 Piano Roll — scale: {scale_name}")
    print(header)
    print(separator)

    for step in range(steps):
        t = step * 0.5
        active = {n["pitch"] for n in notes if n["time"] <= t < n["time"] + n["duration"]}
        row = " ".join(" * " if p in active else " . " for p in scale)
        print(f"{t:5.1f} | {row}")

    print(separator)
    print(f"  {len(notes)} notes  |  {steps * 0.5:.1f} beats total\n")
