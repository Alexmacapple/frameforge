#!/usr/bin/env python3
"""Two isolated real HyperFrames integration tests; artifacts remain local."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE / "local"
WORK = ROOT / "interruption-concurrency"
SOURCE = ROOT / "index.html"
BASE = ROOT / "baseline.html"
GUARD = HERE / "guarded_hyperframes.py"
MEDIA = ("capture.webm", "voice1.m4a", "voice2.m4a", "voice3.m4a")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def project(name):
    d = WORK / name
    if d.exists():
        raise RuntimeError("Existing test folder; refusing overwrite: " + str(d))
    d.mkdir(parents=True)
    for f in ("index.html", "baseline.html", "hyperframes.json", "package.json"):
        shutil.copy2(ROOT / f, d / f)
    for f in MEDIA:
        (d / f).symlink_to((ROOT / f).resolve())
    return d

def command(d):
    return [sys.executable, str(GUARD), "--project", str(d),
            "--baseline", str(d / "baseline.html"),
            "--candidate", str(d / "index.html"),
            "--output", str(d / "result.mp4")]

def run_interrupted():
    d = project("interrupt")
    proc = subprocess.Popen(command(d), stdout=(d/"run-interrupted.log").open("wb"),
                            stderr=subprocess.STDOUT, start_new_session=True)
    time.sleep(8)
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        rc = proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        rc = proc.wait()
    no_final = not (d/"result.mp4").exists()
    # HyperFrames may leave a partial file or workdir. Do not delete it before reporting.
    partials = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name not in
                ("index.html", "baseline.html", "hyperframes.json", "package.json", "run-interrupted.log")]
    return {"interrupted_rc":rc,"no_final_after_interrupt":no_final,"leftovers":partials[:12],"dir":str(d)}

def run_race():
    d = project("race")
    original=(d/"index.html").read_text()
    changed=original.replace("Les deux tâches sont visibles.", "Les deux tâches ont disparu.")
    assert changed!=original
    before=sha(d/"index.html")
    log=(d/"run-race.log").open("wb")
    proc=subprocess.Popen(command(d),stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    try:
        # Mutation after preflight while HyperFrames is rendering.
        time.sleep(12)
        (d/"index.html").write_text(changed)
        time.sleep(5)
        (d/"index.html").write_text(original)
        rc=proc.wait(timeout=180)
    finally:
        if proc.poll() is None:
            os.killpg(proc.pid,signal.SIGTERM)
            proc.wait(timeout=15)
        (d/"index.html").write_text(original)
        log.close()
    final=(d/"result.mp4")
    return {"rc":rc,"input_restored":sha(d/"index.html")==before,
            "final_exists":final.exists(),"final_sha256":sha(final) if final.exists() else None,
            "dir":str(d)}

def main():
    WORK.mkdir(exist_ok=True)
    a=run_interrupted()
    b=run_race()
    report={"interruption":a,"concurrent_transient_mutation":b,
            "scope":"real HyperFrames, copies only, not a universal security boundary"}
    (HERE/"INTERRUPTION-CONCURRENCY-RESULTS.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    main()
