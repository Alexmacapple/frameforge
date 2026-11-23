"""Re-render two-rush fixture after user approval of exact caption B wording."""
import json
from pathlib import Path
import sys
from types import SimpleNamespace

D=Path(__file__).resolve().parent
sys.path.insert(0,str(D))
from test_two_rushes import check
sys.path.insert(0,str(D.parent/'ff10-hyperframes-guarded-integration'))
import guarded_hyperframes_v2 as v2

def main():
    l=D/'local'
    approved='Rush B : barres de couleur, audio témoin.'
    baseline=l/'approved-fixture.html'
    candidate=l/'index.html'
    if approved not in baseline.read_text() or approved not in candidate.read_text():
        raise ValueError('approved_human_text_missing')
    check(baseline,candidate)
    args=SimpleNamespace(project=l,baseline=baseline,candidate=candidate,
        output=l/'two-rushes-after-human-text-approval.mp4')
    result=v2.run(args,preflight_fn=check,
        media=('rush-a-silent-24fps.webm','rush-b-tone-30fps.webm'),
        config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt'))
    print(json.dumps(result))

if __name__=='__main__':main()
