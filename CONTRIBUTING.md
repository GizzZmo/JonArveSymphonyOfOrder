# Contributing to JonArve Symphony of Order

Thank you for wanting to help turn planetary healing into music! 🌍🎵

---

## Project philosophy

Every watt of power saved and every litre of clean water protected deserves to
be heard. This project exists to make that invisible work audible — one commit
at a time. Keep that spirit in mind: contributions should move us closer to
beautiful, accessible, planet-friendly music generation.

---

## Setting up a development environment

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/JonArveSymphonyOfOrder.git
cd JonArveSymphonyOfOrder

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install all dependencies (including dev tools)
pip install -r requirements.txt
```

---

## Code style

- Follow **PEP 8** with a maximum line length of **120 characters**.
- Use `flake8` for linting:

  ```bash
  flake8 --max-line-length=120 data_to_melody.py genre_fusion.py song_builder.py visualizer.py app.py
  ```

- Write clear, concise docstrings for every public function (Google style).
- Use f-strings; avoid `%`-formatting or `.format()`.
- Keep CLI flags backward-compatible — never remove or rename existing flags.

---

## Running tests

```bash
pytest tests/ -v
```

All tests use `tempfile` for output files and clean up after themselves.
New features must include tests in the appropriate `tests/test_*.py` file.

---

## How to submit a pull request

1. **Branch** from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes, following the code style guide above.
3. Run linting and tests locally — both must pass.
4. Commit with a descriptive message:
   ```bash
   git commit -m "feat: add Tibber batch import"
   ```
5. Push and open a pull request against `main`.
6. Fill in the PR template and describe *what* you changed and *why*.

---

## What makes a good contribution?

- New data-source integrations (smart meters, weather APIs, solar panel data).
- Additional musical scales or genre profiles.
- Better ASCII visualizations or export formats.
- Documentation improvements or new example commands.
- Bug fixes with a failing test that the fix makes pass.

---

## Questions?

Open an issue or start a discussion on GitHub. We're a friendly community and
happy to help you get started.
