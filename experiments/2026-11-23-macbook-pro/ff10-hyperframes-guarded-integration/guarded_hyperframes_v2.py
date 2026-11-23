#!/usr/bin/env python3
"""Isolated FF-10 HyperFrames pilot; not a universal FrameForge export guard."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

from guarded_hyperframes import preflight

MEDIA = ("capture.webm", "voice1.m4a", "voice2.m4a", "voice3.m4a")
CONFIG = ("index.html", "hyperframes.json", "package.json", "captions.srt", "captions.vtt", "transcript.txt")
child = None

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stop_child():
    global child
    if child is not None and child.poll() is None:
        try:
            os.killpg(child.pid, signal.SIGTERM)
            child.wait(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait(timeout=8)
        except ProcessLookupError:
            pass

def interrupted(signum, frame):
    stop_child()
    raise KeyboardInterrupt("guarded render interrupted")

def run(args, preflight_fn=None, media=None, config=None):
    preflight_fn = preflight_fn or preflight
    media = MEDIA if media is None else tuple(media)
    config = CONFIG if config is None else tuple(config)
    global child
    for s in (signal.SIGTERM, signal.SIGINT):
        signal.signal(s, interrupted)
    project, baseline, candidate, output = map(Path, (args.project,args.baseline,args.candidate,args.output))
    if output.exists() or output.is_symlink():
        raise ValueError("output_already_exists")
    if candidate.resolve() != (project/"index.html").resolve():
        raise ValueError("candidate_not_project_entrypoint")
    preflight_fn(baseline,candidate)
    sources=[baseline, candidate, *[project/n for n in media], *[project/n for n in config if (project/n).exists()]]
    hashes={str(p):digest(p) for p in sources}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ff10-isolated-",dir=output.parent) as temp:
        work=Path(temp)
        snapshot=work/"project"
        snapshot.mkdir()
        for name in config + media:
            src=project/name
            if src.exists():
                shutil.copyfile(src,snapshot/name)
        baseline_snapshot=work/"baseline.html"
        shutil.copyfile(baseline,baseline_snapshot)
        preflight_fn(baseline_snapshot,snapshot/"index.html")
        for name in config + media:
            src=project/name
            if src.exists() and digest(src)!=digest(snapshot/name):
                raise ValueError("input_changed_while_snapshotting")
        if digest(baseline)!=digest(baseline_snapshot):
            raise ValueError("baseline_changed_while_snapshotting")
        if hashes!={str(p):digest(p) for p in sources}:
            raise ValueError("source_changed_during_preflight")
        # Keep all render inputs private to this invocation. An external mutation
        # of the original project cannot change the bytes HyperFrames reads.
        rendered=work/"rendered.mp4"
        cmd=["npx","--yes","hyperframes@0.8.33","render",str(snapshot),
             "--output="+str(rendered),"--workers=2","--no-best-effort"]
        child=subprocess.Popen(cmd,start_new_session=True,stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
        try:
            _,err=child.communicate()
            if child.returncode:
                raise RuntimeError("hyperframes_failed: "+err.decode(errors="replace")[-700:])
        finally:
            stop_child()
            child=None
        subprocess.run(["ffmpeg","-v","error","-i",str(rendered),"-f","null","-"],
                       check=True,stdout=subprocess.DEVNULL)
        # The source may have changed concurrently; this is reported, but the
        # render itself used an isolated, validated snapshot.
        changed=[str(p) for p in sources if digest(p)!=hashes[str(p)]]
        if changed:
            raise ValueError("source_changed_during_render")
        os.link(rendered,output)
    return {"status":"PASS","output":str(output),"sha256":digest(output)}

def main():
    parser=argparse.ArgumentParser()
    for name in ("project","baseline","candidate","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(run(args)))
    except (ValueError,OSError,RuntimeError,subprocess.CalledProcessError,KeyboardInterrupt) as exc:
        print(json.dumps({"status":"BLOCKED_OR_INTERRUPTED","reason":str(exc)}))
        return 2
    return 0

if __name__=="__main__":
    sys.exit(main())
