# JonArveSymphonyOfOrder

**JonArveSymphonyOfOrder** transforms raw data of power consumption and water-saving metrics into generative melodies — sonic alchemy that turns kilowatts saved and liters of clean water protected into audible beauty.

🌐 **[GitHub Pages](https://gizzzmo.github.io/JonArveSymphonyOfOrder/)** · See [ROADMAP.md](ROADMAP.md) for the full development plan.

---

## Files

| File | Description |
|------|-------------|
| `data_to_melody.py` | Converts daily power/water savings into a MIDI melody; supports CSV/JSON, batch mode, multiple scales |
| `genre_fusion.py` | Algorithmically blends classical, jazz, rock, electronic, blues, and ambient styles |
| `song_builder.py` | Multi-track composer: melody + bass + genre-harmony in one MIDI file |
| `visualizer.py` | ASCII piano-roll terminal preview of generated notes |
| `app.py` | Flask web form — enter metrics, download MIDI |
| `block_breaker_journal.md` | Daily journal template for overcoming composer's block |
| `ROADMAP.md` | Development roadmap and feature backlog |
| `CONTRIBUTING.md` | Guide for contributors |

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

### 2. Phase 4 — CSV/JSON input & batch mode

Load data from a file instead of CLI flags:

```bash
# Default CSV format (columns: date,power_kwh,water_liters)
python data_to_melody.py --csv readings.csv

# Tibber export format
python data_to_melody.py --csv tibber_export.csv --format tibber

# Home Assistant JSON array (state/last_changed fields)
python data_to_melody.py --json ha_energy.json --format homeassistant

# Select a specific date
python data_to_melody.py --csv readings.csv --date 2024-06-01

# Batch: one MIDI per day in a range
python data_to_melody.py --csv readings.csv --batch --start 2024-01-01 --end 2024-01-31
```

---

### 3. Phase 5 — Dry-run, piano-roll preview, playback

```bash
# Preview notes as an ASCII piano-roll (no file written)
python data_to_melody.py --power 7.8 --water 1850 --dry-run

# Generate and immediately play via FluidSynth
python data_to_melody.py --power 7.8 --water 1850 --play
```

---

### 4. Generate a genre-fusion composition

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

### 5. Build a full multi-track song

```bash
python song_builder.py --power 9.1 --water 2100 --genre jazz --scale dorian
```

Produces three MIDI tracks in one file:

| Track | Content |
|-------|---------|
| 0 — Melody | Metrics-driven lead line |
| 1 — Bass | Low-octave counterpart |
| 2 — Harmony | Genre-profile chord fills |

---

### 6. Phase 6 — Web form

```bash
python app.py
# Open http://localhost:5000 — fill in your metrics, click Generate MIDI
```

---

### 7. Composer's block journal

Open `block_breaker_journal.md`, copy it for today's date, and fill it in while the generated MIDI plays.

---

## Testing

```bash
pytest tests/ -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

