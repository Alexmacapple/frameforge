#!/usr/bin/env python3
"""FF-10 scoped guarded remux. Not a mandatory FrameForge-wide render path."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cues(path):
    normalized = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n").strip()
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


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def export(source, reference, candidate, output, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    source, reference, candidate, output = map(Path, (source, reference, candidate, output))
    # Fail closed before reading or creating any output.
    if output.exists() or output.is_symlink():
        raise ValueError("output_already_exists")
    check(reference, candidate)
    before = {str(p): sha256(p) for p in (source, reference, candidate)}
    output.parent.mkdir(parents=True, exist_ok=True)
    # Snapshot inputs to isolate FFmpeg from later edits to the original paths.
    with tempfile.TemporaryDirectory(prefix=".ff10-", dir=output.parent) as work:
        work = Path(work)
        snapshots = []
        for index, item in enumerate((source, reference, candidate)):
            copy = work / (str(index) + item.suffix)
            with item.open("rb") as src, copy.open("xb") as dst:
                while block := src.read(65536):
                    dst.write(block)
            if sha256(copy) != before[str(item)]:
                raise ValueError("input_changed_while_snapshotting")
            snapshots.append(copy)
        check(snapshots[1], snapshots[2])
        if before != {str(p): sha256(p) for p in (source, reference, candidate)}:
            raise ValueError("input_changed_before_export")
        tmp = work / "render.mp4"
        run([ffmpeg, "-nostdin", "-v", "error", "-i", str(snapshots[0]),
             "-i", str(snapshots[2]), "-map", "0:v:0", "-map", "0:a:0",
             "-map", "1:0", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text",
             "-metadata:s:s:0", "language=fra", str(tmp)])
        extracted = work / "extracted.srt"
        run([ffmpeg, "-nostdin", "-v", "error", "-i", str(tmp), "-map", "0:s:0",
             str(extracted)])
        if cues(extracted) != cues(snapshots[2]):
            raise ValueError("exported_subtitles_mismatch")
        run([ffmpeg, "-nostdin", "-v", "error", "-i", str(tmp), "-f", "null", "-"])
        # No replacement of a pre-existing output. Same-filesystem hard link
        # makes creation exclusive even if another process creates it meanwhile.
        os.link(tmp, output)
    return {"status": "PASS", "output": str(output), "sha256": sha256(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("source", "reference", "candidate", "output"):
        parser.add_argument("--" + arg, type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(export(args.source, args.reference, args.candidate, args.output)))
    except (ValueError, OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
