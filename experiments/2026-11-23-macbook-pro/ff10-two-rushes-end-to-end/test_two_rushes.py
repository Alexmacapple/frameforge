import hashlib
import re
import unittest
from pathlib import Path

D=Path(__file__).resolve().parent
L=D/'local'
EXPECTED='7d1dabfca5304d74929532fdeedc48684705024ce81e17b6d1674b1f2b748890'

def block(text, ident):
    matches=re.findall(r'<div\b[^>]*\bid="'+ident+r'"[^>]*>.*?</div>',text,re.S)
    if len(matches)!=1: raise ValueError('missing_or_duplicate_'+ident)
    return matches[0]

def check(reference,candidate):
    if hashlib.sha256(reference.read_bytes()).hexdigest()!=EXPECTED:
        raise ValueError('approval_fixture_digest_mismatch')
    old,new=reference.read_text(),candidate.read_text()
    for ident in ('label-b','transition'):
        if block(old,ident)!=block(new,ident):
            raise ValueError('protected_'+ident+'_changed')
    a,b=block(old,'label-a'),block(new,'label-a')
    if a.replace('background:#101010;', 'background:#222222;')!=b:
        raise ValueError('unapproved_label_a_change')
    if old.replace(a,b)!=new:
        raise ValueError('unapproved_other_change')
    return True

class Tests(unittest.TestCase):
    def test_allowed(self): self.assertTrue(check(L/'approved-fixture.html',L/'index.html'))
    def test_protected(self):
        with self.assertRaisesRegex(ValueError,'protected_label-b_changed'):
            check(L/'approved-fixture.html',L/'adversarial.html')
    def test_forged_baseline(self):
        with self.assertRaisesRegex(ValueError,'approval_fixture_digest_mismatch'):
            check(L/'adversarial.html',L/'adversarial.html')
    def test_two_video_tracks_in_html(self):
        s=(L/'index.html').read_text()
        self.assertIn('id="rush-a"',s)
        self.assertIn('id="rush-b"',s)

if __name__=='__main__':unittest.main()
