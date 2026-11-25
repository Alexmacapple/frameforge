"""Écrit output-reference.json depuis le brouillon témoin, avec les mesures mêmes du garde."""

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path

film = Path(sys.argv[1]).resolve()
draft = film / sys.argv[2]
sys.path.insert(0, str(film.parent / "film-chain"))
g = importlib.import_module("film_guard")
probe = json.loads(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration:format_tags", "-of", "json", str(draft)]))
pcm = subprocess.check_output(
    ["ffmpeg", "-v", "error", "-i", str(draft), "-map", "0:a:0", "-f", "s16le", "-ac", "2", "-ar", "48000", "-"])
fiche = json.loads((film / "provenance-manifest.json").read_text())
ref = {
    "expected_pcm_sha256": hashlib.sha256(pcm).hexdigest(),
    "expected_video_stream_sha256": g.video_stream_hash(draft),
    "expected_duration_s": fiche["film"]["duration_s"],
    "expected_fps": 30,
    "expected_packets_sha256": g.packets_hash(draft),
    "expected_format_tags": probe["format"].get("tags", {}),
}
(film / "output-reference.json").write_text(json.dumps(ref, indent=2) + "\n")
print(json.dumps({"duration_probe": probe["format"]["duration"], **ref}, indent=1))
