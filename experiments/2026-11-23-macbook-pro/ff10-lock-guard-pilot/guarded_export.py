#!/usr/bin/env python3
"""Scoped FF-10 guarded SRT remux. No claim of integration into other render paths."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cues(path):
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    parts = [p for p in normalized.split("\n\n") if p.strip()]
    if len(parts) != 2:
        raise ValueError("expected exactly two SRT cues")
    return parts


def check(reference, candidate):
    old, new = cues(reference), cues(candidate)
    if old[1] != new[1]:
        raise ValueError("protected_cue_2_changed")
    if old[0].replace("\n", " ") != new[0].replace("\n", " "):
        raise ValueError("cue_1_words_or_times_changed")
    return True


def export(source, reference, candidate, output, ffmpeg="ffmpeg"):
    source, reference, candidate, output = map(Path, (source, reference, candidate, output))
    if output.exists():
        raise ValueError("output_already_exists")
    check(reference, candidate)
    before = {str(p): sha256(p) for p in (source, reference, candidate)}
    # Re-check inputs immediately before invoking FFmpeg. This is not an atomic
    # lock and does not protect against concurrent mutation after this check.
    if before != {str(p): sha256(p) for p in (source, reference, candidate)}:
        raise ValueError("input_changed_before_export")
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_name(output.stem + ".partial" + output.suffix)
    if tmp.exists():
        raise ValueError("partial_output_already_exists")
    try:
        subprocess.run([
            ffmpeg, "-nostdin", "-v", "error", "-i", str(source), "-i", str(candidate),
            "-map", "0:v:0", "-map", "0:a:0", "-map", "1:0",
            "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text",
            "-metadata:s:s:0", "language=fra", "-y", str(tmp)
        ], check=True)
        if before != {str(p): sha256(p) for p in (source, reference, candidate)}:
            raise ValueError("input_changed_during_export")
        tmp.replace(output)
    finally:
        tmp.unlink(missing_ok=True)
    return {"status": "PASS", "output": str(output), "sha256": sha256(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("source", "reference", "candidate", "output"):
        parser.add_argument("--" + arg, type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(export(args.source, args.reference, args.candidate, args.output)))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
