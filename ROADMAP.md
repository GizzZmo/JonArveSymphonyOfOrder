# JonArveSymphonyOfOrder — Roadmap

> Turning planetary healing into music, one commit at a time.

---

## ✅ Phase 1 — Foundation (complete)

- [x] `data_to_melody.py` — sonify daily power/water savings into a MIDI melody
- [x] `genre_fusion.py` — algorithmically blend classical, jazz, rock, and electronic styles
- [x] `block_breaker_journal.md` — daily composer's-block journal template
- [x] `README.md` — basic documentation

---

## ✅ Phase 2 — CLI, Scales & Enhanced Sonification (complete)

- [x] `requirements.txt` — pinned dependencies for reproducible installs
- [x] CLI argument parsing for `data_to_melody.py` (`--power`, `--water`, `--output`, `--scale`, `--tempo`, `--bars`)
- [x] Multiple scale support in `data_to_melody.py`: major, minor, pentatonic, dorian, mixolydian
- [x] Improved pitch mapping (linear spread across scale instead of hard modulo)
- [x] CLI argument parsing for `genre_fusion.py` (`--genres`, `--bars`, `--output`, `--tempo`)
- [x] Two additional genres: `blues` and `ambient`
- [x] Per-genre rhythm patterns (note subdivisions)
- [x] Chord voicings layer for jazz/classical bars

---

## ✅ Phase 3 — Multi-Track Song Builder (complete)

- [x] `song_builder.py` — combined composer:
  - Track 0: metrics-driven melody (from `data_to_melody`)
  - Track 1: bass line derived from the same metrics
  - Track 2: genre-fusion harmony layer
- [x] CLI interface (`--power`, `--water`, `--genre`, `--bars`, `--output`, `--tempo`)
- [x] Automatic output filename stamped with today's date

---

## ✅ Phase 4 — Data Input & Batch Processing (complete)

- [x] Accept CSV / JSON files as data source for `data_to_melody.py`
- [x] Batch mode: generate one MIDI per day in a date range
- [x] Integration with smart-meter export formats (Tibber, Home Assistant)

---

## ✅ Phase 5 — Visualization & Playback Helpers (complete)

- [x] ASCII piano-roll preview printed to the terminal (`visualizer.py`)
- [x] `--dry-run` flag (print note list, do not write file)
- [x] Optional FluidSynth playback hook after generation (`--play`)

---

## ✅ Phase 6 — Community & Polish (complete)

- [x] Web form (Flask) to enter metrics and download MIDI (`app.py`)
- [x] Unit test suite (`pytest`) in `tests/`
- [x] GitHub Actions CI (lint + import check + tests)
- [x] Example MIDI commands in `examples/`
- [x] Contribution guide (`CONTRIBUTING.md`)

