import pathlib,re,subprocess,json
D=pathlib.Path('/tmp/frameforge-work-20261123/experiments/2026-11-23-macbook-pro/vertical-v3')
video=D/'media/prototype-v3.mp4'
def command(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 return p.stdout,p.stderr
probe=json.loads(command(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)])[0])
dur=float(probe['format']['duration'])
streams=[(s['codec_type'],s['codec_name']) for s in probe['streams']]
srt=(D/'captions.srt').read_text()
def sec(t):
 h,m,ss=t.split(':');return int(h)*3600+int(m)*60+float(ss.replace(',','.'))
entries=[]
for part in re.split(r'\n\s*\n',srt.strip()):
 lines=part.splitlines()
 if len(lines)>=3:
  a,b=lines[1].split(' --> ')
  entries.append(dict(start=sec(a),end=sec(b),text=' '.join(lines[2:])))
_,audio=command(['ffmpeg','-hide_banner','-i',str(video),'-af','silencedetect=noise=-36dB:d=0.15','-f','null','-'])
silences=[(k,float(v)) for k,v in re.findall(r'silence_(start|end):\s*([0-9.]+)',audio)]
speech=[];pos=0
for kind,t in silences:
 if kind=='start' and t>pos:speech.append([pos,t])
 if kind=='end':pos=t
if pos<dur:speech.append([pos,dur])
print(json.dumps({'duration':dur,'streams':streams,'captions':entries,'silences':silences,'speech_intervals':speech},ensure_ascii=False,indent=2))
assert len(entries)==3
assert all(0<=e['start']<e['end']<=dur for e in entries)
assert all(entries[i]['end']<=entries[i+1]['start'] for i in range(len(entries)-1))
assert ('video','h264') in streams and ('audio','aac') in streams
command(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
print('TECHNICAL_PASS; HUMAN_REVIEW_NOT_RUN; 250MS_SYNC_NOT_PROVEN')
