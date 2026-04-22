# app.py - Flask Web Application
# Provides a web form for entering environmental metrics and downloading a generated MIDI file.

import os
import tempfile
from io import BytesIO

try:
    from flask import Flask, render_template, request, send_file
    _FLASK_AVAILABLE = True
except ImportError:
    _FLASK_AVAILABLE = False

from data_to_melody import SCALES
from genre_fusion import ALL_GENRES
from song_builder import build_song

app = None

if _FLASK_AVAILABLE:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", scales=list(SCALES.keys()), genres=ALL_GENRES)

    @app.route("/generate", methods=["POST"])
    def generate():
        power = float(request.form.get("power_kwh", 7.8))
        water = float(request.form.get("water_liters", 1850))
        scale = request.form.get("scale", "major")
        tempo = int(request.form.get("tempo", 88))
        bars = int(request.form.get("bars", 16))
        genre = request.form.get("genre", "classical")

        tmpfd, tmppath = tempfile.mkstemp(suffix=".mid")
        os.close(tmpfd)
        try:
            build_song(
                power_saved_kwh=power,
                water_saved_liters=water,
                genre=genre,
                bars=bars,
                tempo=tempo,
                filename=tmppath,
                scale_name=scale,
            )
            with open(tmppath, "rb") as fh:
                midi_data = fh.read()
        finally:
            if os.path.exists(tmppath):
                os.unlink(tmppath)

        return send_file(
            BytesIO(midi_data),
            as_attachment=True,
            download_name="symphony_of_order.mid",
            mimetype="audio/midi",
        )


if __name__ == "__main__":
    if not _FLASK_AVAILABLE:
        print("Flask is not installed. Run: pip install flask")
        import sys
        sys.exit(1)
    import os as _os
    app.run(debug=_os.environ.get("FLASK_DEBUG", "0") == "1")
