from kokoro import KPipeline
import numpy as np, soundfile as sf
from pathlib import Path
text = "Une première tâche apparaît dans la liste. Une deuxième tâche apparaît. Les deux tâches sont visibles. La première tâche est cochée et barrée. La deuxième reste à faire."
out=Path('/tmp/frameforge-kokoro-pilot-20261123')
print('Loading French pipeline',flush=True)
pipeline=KPipeline(lang_code='f')
segments=[]
for i, (graphemes, phonemes, audio) in enumerate(pipeline(text, voice='ff_siwis', speed=1.0, split_pattern=r'\n+')):
 print('segment',i,repr(graphemes),len(audio),flush=True)
 segments.append(np.asarray(audio,dtype=np.float32))
if not segments:raise RuntimeError('No audio generated')
a=np.concatenate(segments)
sf.write(str(out/'kokoro-siwis.wav'),a,24000)
print('Saved',len(a)/24000,'seconds',flush=True)
