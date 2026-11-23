"""Scoped npm entrypoint for FF-10 web-demo pilot. No release authorization."""
from pathlib import Path
import hashlib
import json
import sys
from types import SimpleNamespace
import subprocess

ROOT=Path(__file__).resolve().parent
EXPERIMENTS=ROOT.parents[1]
sys.path.insert(0,str(EXPERIMENTS/'ff10-hyperframes-guarded-integration'))
import guarded_hyperframes_v2 as v2
from guarded_hyperframes import preflight

PIN='de4a2b7c434d9e168f891999a4f82d782daaba76253a774dcbabbc1d72b8bfd1'
ASSET_MANIFEST_SHA256='bd789b180e9f848113413241877985863aa00c45feadde79dc26782b149244a4'
ASSET_PINS=json.loads((ROOT/'asset-pins.json').read_text())

def check_assets(project=ROOT):
    manifest=project/'asset-pins.json'
    if not manifest.is_file() or hashlib.sha256(manifest.read_bytes()).hexdigest()!=ASSET_MANIFEST_SHA256:
        raise ValueError('asset_manifest_changed')
    for name, expected in ASSET_PINS.items():
        file=project/name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=expected:
            raise ValueError('protected_asset_changed:'+name)
    return True

def check(reference,candidate):
    if hashlib.sha256(Path(reference).read_bytes()).hexdigest()!=PIN:
        raise ValueError('approved_fixture_digest_mismatch')
    return preflight(reference,candidate)


EXPECTED_PCM='f6819e9e643df7e29951eb2fba046111177c65b6334fa05c6defe2c04652ca86'

def validate_output(path):
    probe=subprocess.run(
        ['ffprobe','-v','error','-show_entries',
         'format=duration:stream=codec_type,codec_name,width,height,nb_frames,avg_frame_rate,duration',
         '-of','json',str(path)],capture_output=True,text=True,check=True)
    data=json.loads(probe.stdout)
    duration=float(data.get('format',{}).get('duration',0))
    if not 16.10<=duration<=16.23:
        raise ValueError('output_duration_invalid')
    video=[s for s in data.get('streams',[]) if s.get('codec_type')=='video']
    audio=[s for s in data.get('streams',[]) if s.get('codec_type')=='audio']
    if len(video)!=1 or video[0].get('codec_name')!='h264' or video[0].get('width')!=1920 or video[0].get('height')!=1080:
        raise ValueError('output_video_format_invalid')
    if int(video[0].get('nb_frames') or 0)<480:
        raise ValueError('output_frame_count_invalid')
    if len(audio)!=1 or audio[0].get('codec_name')!='aac' or float(audio[0].get('duration') or 0)<16.0:
        raise ValueError('output_audio_missing_or_short')
    pcm=subprocess.run(
        ['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-ac','2','-ar','48000','-'],
        capture_output=True,check=True)
    if hashlib.sha256(pcm.stdout).hexdigest()!=EXPECTED_PCM:
        raise ValueError('output_audio_changed')
    return True

def main():
    baseline=ROOT/'baseline.html'
    candidate=ROOT/'index.html'
    check(baseline,candidate)
    check_assets(ROOT)
    args=SimpleNamespace(project=ROOT,baseline=baseline,candidate=candidate,
        output=ROOT/'guarded-web-demo.mp4')
    def render_preflight(reference,candidate):
        check(reference,candidate)
        check_assets(candidate.parent)
        return True
    result=v2.run(args,preflight_fn=render_preflight,
        media=('capture.webm','voice1.m4a','voice2.m4a','voice3.m4a'),
        config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt','asset-pins.json'),
        output_validator=validate_output)
    print(json.dumps(result))

if __name__=='__main__':main()
