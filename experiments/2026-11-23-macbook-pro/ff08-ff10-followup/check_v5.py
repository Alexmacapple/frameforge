from pathlib import Path
import subprocess, hashlib, json, re
R=Path('/Users/alex/Claude/git-hors-workflow/frameforge/experiments/2026-11-23-macbook-pro')
D=R/'vertical-v5-kokoro-siwis'; v=D/'media/prototype-v5.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]))
srt=(D/'captions.srt').read_text()
lines=(D/'transcript.txt').read_text().splitlines()
blocks=re.split(r'\n\s*\n',srt.strip())
captions=[]
for b in blocks:
 parts=b.splitlines()
 if len(parts)!=3:raise ValueError('Malformed SRT '+repr(b))
 captions.append(parts[2])
assert captions==lines,(captions,lines)
data=json.loads((D/'timings.json').read_text())
assert len(data['starts'])==3
assert all(data['starts'][i]+data['durations'][i]<data['starts'][i+1] for i in range(2))
assert all(data['starts'][i]+data['durations'][i]<float(info['format']['duration']) for i in range(3))
streams=info['streams']
vid=next(s for s in streams if s['codec_type']=='video')
audio=next(s for s in streams if s['codec_type']=='audio')
p=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf','scale=240:135','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
frame_size=240*135*3
assert len(p.stdout)%frame_size==0
frames=len(p.stdout)//frame_size
print(json.dumps({'sha256':sha(v),'duration':info['format']['duration'],'frames':frames,'codec_video':vid['codec_name'],'codec_audio':audio['codec_name'],'srt_matches_transcript':True,'narration_intervals_nonoverlapping':True,'voice_hashes':[sha(D/'media'/f'voice{i}.m4a') for i in range(1,4)]},indent=2))
