# data_to_melody.py - Sonification Engine
# Turns daily power-consumption savings or water-saving metrics into generative MIDI melodies.
# Run daily to hear the music of planetary healing.

from midiutil import MIDIFile
import datetime
import random


def generate_melody_from_data(power_saved_kwh=5.2, water_saved_liters=1200, filename="symphony_of_order.mid"):
    """Generate a MIDI melody from environmental savings data.

    Args:
        power_saved_kwh (float): Kilowatt-hours of power saved today.
        water_saved_liters (float): Liters of water protected today.
        filename (str): Output MIDI file path.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 88  # Heartbeat of service
    volume = 100  # noqa: F841

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)

    # Major scale for hope (C major)
    scale = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76]  # C4 to E5

    # Duration based on water savings (longer = more gratitude)
    duration = max(0.5, min(2.0, water_saved_liters / 1000))

    # Generate 16-bar melody
    for i in range(16):
        # Pitch influenced by power saved
        pitch_index = int(power_saved_kwh * 1.5) % len(scale)
        pitch = scale[pitch_index] + random.randint(-2, 2)  # slight variation

        # Velocity (volume) = impact strength
        vel = min(127, int(60 + power_saved_kwh * 8))

        MyMIDI.addNote(track, channel, pitch, time + i * 0.5, duration, vel)

        # Occasional harmonic chord for fusion depth
        if i % 4 == 0:
            MyMIDI.addNote(track, channel, pitch - 12, time + i * 0.5, duration * 2, vel - 20)  # bass

    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)

    print(f"🎵 Melody generated: {filename}")
    print(f"Power saved: {power_saved_kwh} kWh → {len(scale)} notes of hope")
    print(f"Water saved: {water_saved_liters} liters → flowing rhythm of life")


# Example daily use
if __name__ == "__main__":
    today = datetime.date.today()
    # Replace with your real metrics (from smart meter or water app)
    generate_melody_from_data(
        power_saved_kwh=7.8,
        water_saved_liters=1850,
        filename=f"order_{today}.mid",
    )
