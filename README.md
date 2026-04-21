# JonArveSymphonyOfOrder

**JonArveSymphonyOfOrder** transforms raw data of power consumption and water-saving metrics into generative melodies — sonic alchemy that turns kilowatts saved and liters of clean water protected into audible beauty.

See [ROADMAP.md](ROADMAP.md) for the development plan.

---

## Files

| File | Description |
|------|-------------|
| `data_to_melody.py` | Converts daily power/water savings into a MIDI melody; supports multiple scales and CLI args |
| `genre_fusion.py` | Algorithmically blends classical, jazz, rock, electronic, blues, and ambient styles |
| `song_builder.py` | Multi-track composer: melody + bass + genre-harmony in one MIDI file |
| `block_breaker_journal.md` | Daily journal template for overcoming composer's block |
| `ROADMAP.md` | Development roadmap and feature backlog |

---

## Requirements

```
pip install -r requirements.txt
```

---

## Usage

### 1. Generate a melody from your daily metrics

```bash
python data_to_melody.py --power 7.8 --water 1850
```

Full options:

| Flag | Default | Description |
|------|---------|-------------|
| `--power KWH` | `7.8` | Kilowatt-hours of power saved today |
| `--water LITERS` | `1850` | Liters of water protected today |
| `--scale SCALE` | `major` | Scale: `major`, `minor`, `pentatonic`, `dorian`, `mixolydian` |
| `--tempo BPM` | `88` | Tempo in beats per minute |
| `--bars N` | `16` | Number of melodic bars |
| `--output FILE` | `order_YYYY-MM-DD.mid` | Output MIDI filename |

Example — minor pentatonic at 100 BPM:

```bash
python data_to_melody.py --power 12.5 --water 2300 --scale pentatonic --tempo 100
```

---

### 2. Generate a genre-fusion composition

```bash
python genre_fusion.py --genres jazz blues electronic --bars 32
```

Full options:

| Flag | Default | Description |
|------|---------|-------------|
| `--genres GENRE [...]` | `classical jazz rock electronic` | Genres to blend |
| `--bars N` | `16` | Number of bars |
| `--tempo BPM` | random 72–120 | Tempo in BPM |
| `--output FILE` | `fusion_order.mid` | Output MIDI filename |

Available genres: `classical`, `jazz`, `rock`, `electronic`, `blues`, `ambient`

---

### 3. Build a full multi-track song

```bash
python song_builder.py --power 9.1 --water 2100 --genre jazz --scale dorian
```

Produces three MIDI tracks in one file:

| Track | Content |
|-------|---------|
| 0 — Melody | Metrics-driven lead line |
| 1 — Bass | Low-octave counterpart |
| 2 — Harmony | Genre-profile chord fills |

Full options:

| Flag | Default | Description |
|------|---------|-------------|
| `--power KWH` | `7.8` | Kilowatt-hours of power saved |
| `--water LITERS` | `1850` | Liters of water protected |
| `--genre GENRE` | `classical` | Harmony genre (see list above) |
| `--scale SCALE` | `major` | Melodic scale |
| `--bars N` | `16` | Number of bars |
| `--tempo BPM` | `88` | Tempo in BPM |
| `--output FILE` | `song_YYYY-MM-DD.mid` | Output MIDI filename |

---

### 4. Composer's block journal

Open `block_breaker_journal.md`, copy it for today's date, and fill it in while the generated MIDI plays.
