"""Distinct subsequent edit, retaining the user-approved caption B."""
import hashlib
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace

D=Path(__file__).resolve().parent
L=D/'local'
sys.path.insert(0,str(D.parent/'ff10-hyperframes-guarded-integration'))
import guarded_hyperframes_v2 as renderer
from test_two_rushes import EXPECTED, block, check

def verify(baseline, candidate):
    if hashlib.sha256(baseline.read_bytes()).hexdigest()!=EXPECTED:
        raise ValueError('approval_fixture_digest_mismatch')
    old=baseline.read_text()
    new=candidate.read_text()
    for ident in ('label-b','transition'):
        if block(old,ident)!=block(new,ident):
            raise ValueError('protected_'+ident+'_changed')
    a=block(old,'label-a')
    b=block(new,'label-a')
    allowed=a.replace('background:#101010;','background:#222222;').replace('font-size:30px','font-size:32px')
    if b!=allowed:raise ValueError('unauthorized_label_a_change')
    if old.replace(a,b)!=new:raise ValueError('unauthorized_other_change')
    if 'Rush B : barres de couleur, audio témoin.' not in b and 'Rush B : barres de couleur, audio témoin.' not in block(new,'label-b'):
        raise ValueError('approved_text_missing')
    return True

def main():
    baseline=L/'approved-fixture.html'
    candidate=L/'successive-index.html'
    original=(L/'index.html').read_text()
    updated=original.replace('font-size:30px">Rush A', 'font-size:32px">Rush A')
    assert original!=updated
    candidate.write_text(updated)
    verify(baseline,candidate)
    # v2 requires the candidate to be the actual project entrypoint.
    project=L/'successive-project'
    if project.exists():raise ValueError('project_exists')
    project.mkdir()
    for n in ('hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt'):
        p=L/n
        if p.exists():(project/n).write_bytes(p.read_bytes())
    (project/'index.html').write_text(updated)
    for n in ('rush-a-silent-24fps.webm','rush-b-tone-30fps.webm'):
        (project/n).symlink_to((L/n).resolve())
    adversarial=project/'adversarial.html'
    adversarial.write_text(updated.replace('audio témoin.','son témoin.'))
    checks={}
    for name,path,base in [('protected_change',adversarial,baseline),('forged_baseline',adversarial,adversarial)]:
        try:verify(base,path)
        except ValueError as e:checks[name]=str(e)
        else:raise AssertionError(name+'_not_blocked')
    args=SimpleNamespace(project=project,baseline=baseline,candidate=project/'index.html',
        output=L/'two-rushes-successive-edit.mp4')
    result=renderer.run(args,preflight_fn=verify,
        media=('rush-a-silent-24fps.webm','rush-b-tone-30fps.webm'),
        config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt'))
    print(json.dumps({'checks':checks,'render':result},ensure_ascii=False))
if __name__=='__main__':main()
