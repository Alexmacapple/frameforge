"""Finalize the already human-approved Kokoro cut, without bypassing guarded render."""
from pathlib import Path
from types import SimpleNamespace
import hashlib,os,subprocess,tempfile
import render_guarded as g

ROOT=Path(__file__).resolve().parent
AUDIO_SHA='857e6be89c8747c264ae2d4fd65d6b1beddb9e89188d4ca31c52faf3b3c46ea0'
APPROVED_SHA='f4552189c24758879f60a87c0a0a369dbd49a8e3a333c683eac0b42057ecefad'
VIDEO_STREAM_SHA='0,v,SHA256=86a966e4f9bc6c7d000a179061eb0ba5e6422c10fb84329be6c273decba4eb52'

def stream_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
        '-map','0:v:0','-c','copy','-f','streamhash','-hash','sha256','-']).decode().strip()

def finalize(audio=None, output=None, render_fn=None):
    audio=Path(audio or ROOT/'media/kokoro-new-audio.m4a')
    output=Path(output or ROOT/'media/form-kokoro-guarded.mp4')
    if output.exists() or output.is_symlink(): raise ValueError('output_already_exists')
    if g.sha(audio)!=AUDIO_SHA: raise ValueError('unapproved_kokoro_audio')
    # Preflight before any expensive work, including source pins and technical fixture.
    g.preflight(ROOT/'baseline.html',ROOT/'index.html')
    with tempfile.TemporaryDirectory(prefix='.kokoro-final-',dir=output.parent) as td:
        temp=Path(td)
        intermediate=temp/'guarded-thomas.mp4'
        if render_fn is None:
            args=SimpleNamespace(project=ROOT,baseline=ROOT/'baseline.html',
                candidate=ROOT/'index.html',output=intermediate)
            g.wrapper.run(args,preflight_fn=g.preflight,
                media=('capture.mp4','voice1.m4a','voice2.m4a','voice3.m4a'),
                config=('index.html','hyperframes.json','package.json','captions.srt',
                    'captions.vtt','transcript.txt','form-input-pins.json','form-output-reference.json'),
                output_validator=g.validate_output)
        else: render_fn(intermediate)
        if stream_hash(intermediate)!=VIDEO_STREAM_SHA: raise ValueError('unapproved_video_stream')
        candidate=temp/'kokoro-final.mp4'
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(intermediate),'-i',str(audio),
            '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy',
            '-movflags','+faststart',str(candidate)],check=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(candidate),'-f','null','-'],check=True)
        if stream_hash(candidate)!=VIDEO_STREAM_SHA: raise ValueError('video_stream_changed')
        if g.sha(candidate)!=APPROVED_SHA: raise ValueError('final_not_approved_exact_version')
        if g.sha(audio)!=AUDIO_SHA: raise ValueError('audio_changed_during_render')
        if output.exists() or output.is_symlink(): raise ValueError('output_already_exists')
        os.link(candidate,output)
    return {'status':'PASS','output':str(output),'sha256':g.sha(output)}

if __name__=='__main__':
    import json
    print(json.dumps(finalize()))
