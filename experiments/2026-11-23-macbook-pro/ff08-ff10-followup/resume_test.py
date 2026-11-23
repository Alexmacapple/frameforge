from pathlib import Path
import hashlib,json,re
R=Path('/Users/alex/Claude/git-hors-workflow/frameforge')
S=R/'experiments/2026-11-23-macbook-pro/vertical-v5-kokoro-siwis'
D=Path('/tmp/frameforge-ff10-revision-sandbox-20261123')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((D/'checkpoint.json').read_text())
a=json.loads((D/'approval.json').read_text())
assert c['stage']=='subtitle-edited'
assert digest(S/'captions.srt')==c['expected_source_sha']
assert digest(S/'media/voice1.m4a')==a['voice_hash']
original=(S/'captions.srt').read_text();edited=(D/'captions.srt').read_text()
o=original.split('\n\n');e=edited.split('\n\n')
assert len(o)==len(e)
changed=[i+1 for i,(x,y) in enumerate(zip(o,e)) if x!=y]
assert changed==[2],changed
assert o[0]==e[0] and o[2]==e[2]
assert 'Une deuxième tâche apparaît ; les deux restent visibles.' in e[1]
# Invalidation is explicit: text no longer matches voice, and derived embedded subtitles need rebuild.
report={'status':'PASS_LIMITED','test_type':'copy-only subtitle change with simulated interruption','changed_scenes':changed,'unchanged_scenes':[1,3],'approved_voice1_hash_preserved':True,'source_video_untouched':True,'source_subtitles_untouched':True,'invalidated':['scene2 voice-to-caption fidelity','scene2 embedded captions','whole-film subtitle approval'],'not_tested':['render rerun','cache reuse','actual human approval lock','real interruption during rendering','full pipeline resume']}
(D/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
