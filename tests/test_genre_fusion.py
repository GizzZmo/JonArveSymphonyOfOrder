import os
import tempfile

import pytest

from genre_fusion import fuse_genres, ALL_GENRES


def test_fuse_genres_creates_file():
    """fuse_genres should write a non-empty MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        fuse_genres(filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


def test_invalid_genre_raises_value_error():
    """fuse_genres should raise ValueError for an unknown genre."""
    with pytest.raises(ValueError, match="Unknown genre"):
        fuse_genres(genres=["not_a_genre"])


@pytest.mark.parametrize("genre", ALL_GENRES)
def test_each_genre_generates_file(genre):
    """Every supported genre should produce a valid MIDI file."""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        tmppath = f.name
    try:
        fuse_genres(genres=[genre], bars=4, filename=tmppath)
        assert os.path.exists(tmppath)
        assert os.path.getsize(tmppath) > 0
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)
