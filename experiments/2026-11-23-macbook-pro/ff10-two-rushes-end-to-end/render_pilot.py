"""FF-10 fixture-only two-rushes pilot; uses V2's isolated renderer."""
import json
from pathlib import Path
import sys
from types import SimpleNamespace

D=Path(__file__).resolve().parent
sys.path.insert(0,str(D))
from test_two_rushes import check
V2=D.parent/'ff10-hyperframes-guarded-integration'
sys.path.insert(0,str(V2))
import guarded_hyperframes_v2 as v2

def main():
    l=D/'local'
    check(l/'approved-fixture.html',l/'index.html')
    media=('rush-a-silent-24fps.webm','rush-b-tone-30fps.webm')
    config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt')
    args=SimpleNamespace(project=l,baseline=l/'approved-fixture.html',
                         candidate=l/'index.html',output=l/'two-rushes-protected.mp4')
    try:
        result=v2.run(args,preflight_fn=check,media=media,config=config)
        print(json.dumps(result))
        return 0
    except (ValueError,OSError,RuntimeError) as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)}))
        return 2

if __name__=='__main__':sys.exit(main())
