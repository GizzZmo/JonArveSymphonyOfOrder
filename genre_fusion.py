# genre_fusion.py - Algorithmic Genre Fusion
# Blends classical, jazz, rock, and electronic styles into a single MIDI composition.

from midiutil import MIDIFile
import random


def fuse_genres(genres=None, bars=8, filename="fusion_order.mid"):
    """Algorithmically blend multiple musical genres into a MIDI file.

    Args:
        genres (list[str]): List of genres to blend. Supported values:
            "classical", "jazz", "rock", "electronic".
        bars (int): Number of bars to generate.
        filename (str): Output MIDI file path.
    """
    if genres is None:
        genres = ["classical", "jazz", "rock", "electronic"]

    track = 0
    channel = 0
    time = 0
    tempo = random.randint(72, 120)  # Dynamic energy
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)

    scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C major base scale

    for bar in range(bars):
        genre = random.choice(genres)
        if genre == "classical":
            duration = 2.0
            velocity = 90
        elif genre == "jazz":
            duration = random.uniform(0.5, 1.5)
            velocity = 110
            scale = [60, 63, 65, 67, 70, 72]  # bluesy
        elif genre == "rock":
            duration = 0.5
            velocity = 127
        else:  # electronic
            duration = 1.0
            velocity = 100

        for beat in range(4):
            pitch = random.choice(scale) + random.randint(-3, 3)
            MyMIDI.addNote(track, channel, pitch, time, duration, velocity)
            if genre in ["jazz", "electronic"]:
                # Add a harmony layer one octave up
                MyMIDI.addNote(track, channel, pitch + 12, time + 0.25, 0.5, velocity - 30)
            time += duration

    with open(filename, "wb") as f:
        MyMIDI.writeFile(f)

    print(f"🔥 Fusion masterpiece created: {filename} — {', '.join(genres)} blended!")


# Run it
if __name__ == "__main__":
    fuse_genres(genres=["classical", "jazz", "rock", "electronic"], bars=16)
