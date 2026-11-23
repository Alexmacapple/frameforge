from pathlib import Path
import hashlib,json,shutil,re
R=Path(__file__).resolve().parents[3]
S=R/'experiments/2026-11-23-macbook-pro/vertical-v5-kokoro-siwis'
D=Path('/tmp/frameforge-ff10-revision-sandbox-20261123')
if D.exists():shutil.rmtree(D)
D.mkdir(parents=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['captions.srt','transcript.txt','timings.json','index.html','media/voice1.m4a','media/voice2.m4a','media/voice3.m4a','media/capture.webm','media/prototype-v5.mp4']
before={p:digest(S/p) for p in files}
# Simulate a human-approved choice in scene 1; this is a test fixture, not a real approval.
approval={'scene':'1','approved_text':(S/'transcript.txt').read_text().splitlines()[0],'voice_hash':before['media/voice1.m4a'],'approval_scope':'test-fixture-only'}
(D/'approval.json').write_text(json.dumps(approval,ensure_ascii=False,indent=2))
# Copy only the editable subtitle file, not a whole pipeline.
shutil.copy2(S/'captions.srt',D/'captions.srt')
text=(D/'captions.srt').read_text()
old='Une deuxième tâche apparaît. Les deux tâches sont visibles.'
new='Une deuxième tâche apparaît ; les deux restent visibles.'
assert text.count(old)==1
text=text.replace(old,new)
(D/'captions.srt').write_text(text)
(D/'checkpoint.json').write_text(json.dumps({'stage':'subtitle-edited','changed_scene':2,'expected_source_sha':before['captions.srt'],'approved_voice_hash':before['media/voice1.m4a']},indent=2))
# INTERRUPT HERE: resume in a new process below.
print('CHECKPOINT_CREATED',str(D))
