#!/usr/bin/env python3
"""FF-10 integration test: interrupt the guarded export then rerun."""
import hashlib
import shutil
import json
import os
from pathlib import Path
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
local = here / "local"
source = here.parent / "ff12-independent-cut-v2" / "local" / "ff12-narrated-fr-subtitled-DRAFT.mp4"
reference = local / "baseline.srt"
candidate = local / "allowed.srt"
output = local / "guarded-interrupted-resumed.mp4"
if output.exists():
    raise SystemExit("Refusing to overwrite existing test output")
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
before = {str(p): digest(p) for p in (source, reference, candidate)}
cmd = [sys.executable, str(here / "guarded_export.py"), "--source", str(source),
       "--reference", str(reference), "--candidate", str(candidate),
       "--output", str(output)]
# Slow only the input read, not the production code. The wrapper is local and
# is never committed; source is snapshotted before ffmpeg is invoked.
wrapper = local / "ffmpeg-slow-wrapper"
wrapper.write_text("#!/bin/sh\nexec " + shutil.which("ffmpeg") + " -re \"$@\"\n")
wrapper.chmod(0o700)
# The exporter has a default ffmpeg argument; use a Python entry point to
# inject a slow wrapper without changing the CLI contract.
launcher = local / "slow-launcher.py"
launcher.write_text(
    "import importlib.util,sys\n"
    "spec=importlib.util.spec_from_file_location('g',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\n"
    "m.export(*sys.argv[2:6],ffmpeg=sys.argv[6])\n"
)
slow_cmd = [sys.executable, str(launcher), str(here / "guarded_export.py"),
            str(source), str(reference), str(candidate), str(output), str(wrapper)]
proc = subprocess.Popen(slow_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        start_new_session=True)
time.sleep(2.0)
# SIGTERM to the entire process group including FFmpeg.
os.killpg(proc.pid, 15)
stdout, stderr = proc.communicate(timeout=15)
interrupted = proc.returncode != 0 and not output.exists()
if not interrupted:
    raise RuntimeError(f"interruption failed: rc={proc.returncode}, output={output.exists()}")
# The temporary working directory may remain after SIGTERM, because Python
# cannot run its finally block; document and clean it explicitly.
orphans = sorted(p for p in local.glob(".ff10-*") if p.is_dir())
for orphan in orphans:
    shutil.rmtree(orphan)
result = subprocess.run(cmd, text=True, capture_output=True, timeout=40)
if result.returncode != 0 or not output.exists():
    raise RuntimeError(f"resume failed: {result.returncode} {result.stdout} {result.stderr}")
after = {str(p): digest(p) for p in (source, reference, candidate)}
assert before == after
report = {"interrupted_process_returncode": proc.returncode,
          "no_output_after_interruption": interrupted,
          "orphan_temp_dirs_cleaned": len(orphans),
          "relaunch_returncode": result.returncode,
          "relaunch_output": json.loads(result.stdout),
          "inputs_unchanged": before == after,
          "mode": "complete rerun; no checkpoint recovery"}
(here / "INTERRUPTION-RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
