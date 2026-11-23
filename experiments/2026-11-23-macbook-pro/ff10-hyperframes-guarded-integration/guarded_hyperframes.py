#!/usr/bin/env python3
"""FF-10 scoped preflight + real HyperFrames render."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

def block(html, ident):
    matches = re.findall(r'<div\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*>.*?</div>', html, re.S)
    if len(matches) != 1:
        raise ValueError('missing_or_duplicate_' + ident)
    return matches[0]

def preflight(baseline, candidate):
    old = baseline.read_text()
    new = candidate.read_text()
    protected = ['caption2','caption3']
    for ident in protected:
        if block(old,ident) != block(new,ident):
            raise ValueError('protected_' + ident + '_changed')
    a,b=block(old,'caption1'),block(new,'caption1')
    if a.replace('background:#111;', 'background:#222;') != b:
        raise ValueError('unapproved_caption1_change')
    if old.replace(a,b) != new:
        raise ValueError('unapproved_outside_caption1')
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.output.exists(): raise ValueError('output_already_exists')
        preflight(args.baseline,args.candidate)
        if args.candidate.resolve() != (args.project/'index.html').resolve():
            raise ValueError('candidate_not_project_entrypoint')
        inputs=[args.baseline,args.candidate,*[args.project/n for n in ['capture.webm','voice1.m4a','voice2.m4a','voice3.m4a']]]
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
        if before != {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}:
            raise ValueError('inputs_changed_before_render')
        cmd=['npx','--yes','hyperframes@0.8.33','render',str(args.project),'--output='+str(args.output),'--workers=2','--no-best-effort']
        subprocess.run(cmd,check=True)
        if before != {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}:
            raise ValueError('inputs_changed_during_render')
        subprocess.run(['ffmpeg','-v','error','-i',str(args.output),'-f','null','-'],check=True)
        print(json.dumps({'status':'PASS','sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),'output':str(args.output)}))
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'status':'BLOCKED_OR_FAILED','reason':str(exc)}))
        return 2
    return 0

if __name__=='__main__':sys.exit(main())
