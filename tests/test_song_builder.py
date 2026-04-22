import os
import tempfile

import pytest

from song_builder import build_song
from genre_fusion import ALL_GENRES


def test_build_song_creates_file():
    """build_song should write a non-empty MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        build_song(filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


def test_invalid_genre_raises_value_error():
    """build_song should raise ValueError for an unknown genre."""
    with pytest.raises(ValueError, match="Unknown genre"):
        build_song(genre="not_a_genre")


def test_build_song_returns_filename():
    """build_song should return the path to the written file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        result = build_song(filename=tmppath)
        assert result == tmppath
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


@pytest.mark.parametrize("genre", ALL_GENRES)
def test_each_genre_generates_file(genre):
    """Every supported genre should produce a valid MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        build_song(genre=genre, bars=4, filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)
