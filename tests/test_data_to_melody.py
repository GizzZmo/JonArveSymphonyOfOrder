import os
import tempfile

import pytest

from data_to_melody import generate_melody_from_data, SCALES


def test_generate_melody_creates_file():
    """generate_melody_from_data should write a non-empty MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        generate_melody_from_data(filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


@pytest.mark.parametrize("scale_name", list(SCALES.keys()))
def test_each_scale_generates_file(scale_name):
    """Every supported scale should produce a valid MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        generate_melody_from_data(scale_name=scale_name, filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


def test_dry_run_returns_notes_without_file(tmp_path):
    """dry_run=True should return a note list and not write a file."""
    outfile = str(tmp_path / "should_not_exist.mid")
    notes = generate_melody_from_data(dry_run=True, filename=outfile)
    assert isinstance(notes, list)
    assert len(notes) > 0
    assert not os.path.exists(outfile)


def test_notes_have_required_keys():
    """Each returned note dict must contain pitch, time, duration, velocity."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        notes = generate_melody_from_data(filename=tmppath)
        required = {"pitch", "time", "duration", "velocity"}
        assert all(required.issubset(n.keys()) for n in notes)
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)
