"""FF-10 form-only guard. Fixture pin is technical, not human editorial approval."""
from pathlib import Path
import hashlib,json,subprocess,sys
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/'ff10-hyperframes-guarded-integration'))
import guarded_hyperframes_v2 as wrapper

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
# Reference digests fixed by this revision; changing code and manifest together is not an independent approval.
PIN_MANIFEST_SHA256='3fe73d024dc5e8bd9e0ad38cdfcc657d93cc7d9c6d2196b35e230cea80043adb'
PIN_HTML_SHA256='39e3d12879fa2229bb49aff087ce166b4807683bf350fa19b9e465c311077138'
PIN_OUTPUT_REFERENCE_SHA256='e90edc9814e0a24fd12763f7725c0ca2a74c6fe00030126f3665315ecfe60a00'

def preflight(reference,candidate):
    if sha(reference)!=PIN_HTML_SHA256 or sha(candidate)!=PIN_HTML_SHA256:
        raise ValueError('form_reference_or_candidate_changed')
    root=Path(candidate).parent
    manifest=root/'form-input-pins.json'
    if sha(manifest)!=PIN_MANIFEST_SHA256: raise ValueError('form_manifest_changed')
    for name,expected in json.loads(manifest.read_text()).items():
        f=root/name
        if not f.is_file() or sha(f)!=expected:
            raise ValueError('form_asset_changed:'+name)
    ref=root/'form-output-reference.json'
    if sha(ref)!=PIN_OUTPUT_REFERENCE_SHA256: raise ValueError('form_output_reference_changed')
    return True

def validate_output(path):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
      'format=duration:stream=codec_type,codec_name,width,height,nb_frames,avg_frame_rate,duration',
      '-of','json',str(path)]))
    if abs(float(data['format']['duration'])-16)>0.08: raise ValueError('form_output_duration_invalid')
    video=[s for s in data['streams'] if s['codec_type']=='video']
    audio=[s for s in data['streams'] if s['codec_type']=='audio']
    if len(video)!=1 or video[0].get('codec_name')!='h264' or (video[0].get('width'),video[0].get('height'))!=(1920,1080):
        raise ValueError('form_output_video_invalid')
    n,d=map(int,video[0].get('avg_frame_rate','0/0').split('/'))
    if d==0 or abs(n/d-30)>0.01 or int(video[0].get('nb_frames') or 0)<480:
        raise ValueError('form_output_framerate_invalid')
    if len(audio)!=1 or audio[0].get('codec_name')!='aac' or float(audio[0].get('duration') or 0)<15.9:
        raise ValueError('form_output_audio_invalid')
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                                  '-f','s16le','-ac','2','-ar','48000','-'])
    expected=json.loads((ROOT/'form-output-reference.json').read_text())['expected_pcm_sha256']
    if hashlib.sha256(pcm).hexdigest()!=expected:
        raise ValueError('form_output_audio_changed')
    return True

def main():
    args=SimpleNamespace(project=ROOT,baseline=ROOT/'baseline.html',candidate=ROOT/'index.html',
                         output=ROOT/'media/form-guarded.mp4')
    print(json.dumps(wrapper.run(args,preflight_fn=preflight,
        media=('capture.mp4','voice1.m4a','voice2.m4a','voice3.m4a'),
        config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt',
                'transcript.txt','form-input-pins.json','form-output-reference.json'),
        output_validator=validate_output)))

if __name__=='__main__':main()
