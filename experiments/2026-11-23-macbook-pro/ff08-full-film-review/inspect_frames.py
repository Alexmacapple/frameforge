import subprocess, pathlib, json, hashlib
from PIL import Image
R=pathlib.Path('/tmp/frameforge-work-20261123')
D=R/'experiments/2026-11-23-macbook-pro/vertical-v3-reframed'
v=D/'media/reframed.mp4'
p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)],capture_output=True,text=True,check=True)
data=json.loads(p.stdout)
video=next(x for x in data['streams'] if x['codec_type']=='video')
w,h=int(video['width']),int(video['height'])
cmd=['ffmpeg','-v','error','-i',str(v),'-vf','scale=480:270','-pix_fmt','rgb24','-f','rawvideo','-']
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
sz=480*270*3; frames=0;red=[];nonblack=[]; sample=[]
while True:
 b=p.stdout.read(sz)
 if not b:break
 if len(b)!=sz:raise ValueError('partial frame')
 im=Image.frombytes('RGB',(480,270),b)
 # high-saturation red pixels in upper 80% excluding tiny icon elements
 pix=im.load();redcount=0;non=0
 for y in range(0,216,3):
  for x in range(0,480,3):
   r,g,bl=pix[x,y]
   if r>175 and g<90 and bl<90:redcount+=1
   if max(r,g,bl)>35:non+=1
 if redcount>300:red.append([frames,redcount])
 if non<10:nonblack.append(frames)
 frames+=1
p.wait()
print(json.dumps({'frames':frames,'resolution':[w,h],'fps':video['avg_frame_rate'],'duration':data['format']['duration'],'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'red_large_area_frames':red[:20],'black_frames':nonblack[:20],'audio_streams':[{'codec':x['codec_name'],'channels':x.get('channels')} for x in data['streams'] if x['codec_type']=='audio']},indent=2))
