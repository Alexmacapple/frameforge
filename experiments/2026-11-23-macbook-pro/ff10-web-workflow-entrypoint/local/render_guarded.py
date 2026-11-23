"""Scoped npm entrypoint for FF-10 web-demo pilot. No release authorization."""
from pathlib import Path
import hashlib
import json
import sys
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parent
EXPERIMENTS=ROOT.parents[1]
sys.path.insert(0,str(EXPERIMENTS/'ff10-hyperframes-guarded-integration'))
import guarded_hyperframes_v2 as v2
from guarded_hyperframes import preflight

PIN='de4a2b7c434d9e168f891999a4f82d782daaba76253a774dcbabbc1d72b8bfd1'

def check(reference,candidate):
    if hashlib.sha256(Path(reference).read_bytes()).hexdigest()!=PIN:
        raise ValueError('approved_fixture_digest_mismatch')
    return preflight(reference,candidate)

def main():
    baseline=ROOT/'baseline.html'
    candidate=ROOT/'index.html'
    check(baseline,candidate)
    args=SimpleNamespace(project=ROOT,baseline=baseline,candidate=candidate,
        output=ROOT/'guarded-web-demo.mp4')
    result=v2.run(args,preflight_fn=check,
        media=('capture.webm','voice1.m4a','voice2.m4a','voice3.m4a'),
        config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt'))
    print(json.dumps(result))

if __name__=='__main__':main()
