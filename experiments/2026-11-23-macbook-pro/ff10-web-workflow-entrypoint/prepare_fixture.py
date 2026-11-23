"""Rebuild the FF-10 web pilot from versioned V5 assets; no media generated."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
EXPERIMENTS=HERE.parent
V5=EXPERIMENTS/'vertical-v5-kokoro'
PINS='de4a2b7c434d9e168f891999a4f82d782daaba76253a774dcbabbc1d72b8bfd1'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare(dest):
    dest=Path(dest)
    dest.mkdir(parents=True,exist_ok=True)
    for name in ('render_guarded.py','asset-pins.json','package.json'):
        source=HERE/'local'/name
        if not source.is_file():
            raise FileNotFoundError('versioned pilot source missing: '+str(source))
        shutil.copyfile(source,dest/name)
    for name in ('hyperframes.json','captions.srt','captions.vtt','transcript.txt'):
        shutil.copyfile(V5/name,dest/name)
    for name in ('capture.webm','voice1.m4a','voice2.m4a','voice3.m4a'):
        shutil.copyfile(V5/'media'/name,dest/name)
    baseline=(V5/'index.html').read_bytes()
    (dest/'baseline.html').write_bytes(baseline)
    if sha(dest/'baseline.html')!=PINS:
        raise ValueError('baseline_digest_mismatch')
    old=b'<div id="caption1"'
    start=baseline.index(old)
    end=baseline.index(b'</div>',start)+len(b'</div>')
    block=baseline[start:end]
    modified=block.replace(b'background:#111;',b'background:#222;')
    if modified==block:
        raise ValueError('expected_caption1_style_missing')
    (dest/'index.html').write_bytes(baseline[:start]+modified+baseline[end:])
    (dest/'adversarial.html').write_bytes((dest/'index.html').read_bytes().replace(
        'Les deux tâches sont visibles.'.encode(), 'Les deux tâches ont disparu.'.encode()))
    pins=json.loads((dest/'asset-pins.json').read_text())
    for name, expected in pins.items():
        if sha(dest/name)!=expected:
            raise ValueError('asset_digest_mismatch:'+name)
    print(json.dumps({'status':'PASS','destination':str(dest),'assets_verified':len(pins),
                      'baseline_sha256':PINS,'historical_mp4_required':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--destination',type=Path,default=HERE/'local')
    prepare(p.parse_args().destination)
