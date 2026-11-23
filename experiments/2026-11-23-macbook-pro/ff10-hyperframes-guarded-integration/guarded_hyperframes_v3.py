#!/usr/bin/env python3
"""FF-10 scoped approval hash check before V2 isolated HyperFrames render."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import guarded_hyperframes_v2 as v2

def check_approval(reference, expected_sha256):
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in expected_sha256):
        raise ValueError("invalid_approval_digest")
    actual = hashlib.sha256(Path(reference).read_bytes()).hexdigest()
    if actual != expected_sha256:
        raise ValueError("approved_reference_digest_mismatch")
    return True

def main():
    parser = argparse.ArgumentParser()
    for name in ("project", "baseline", "candidate", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--approved-sha256", required=True)
    args = parser.parse_args()
    try:
        check_approval(args.baseline, args.approved_sha256)
        return v2.main_from_args(args) if hasattr(v2,"main_from_args") else execute(args)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2

def execute(args):
    # Reuse V2's existing render, process supervision, snapshot and verification.
    try:
        print(json.dumps(v2.run(args)))
        return 0
    except (ValueError, OSError, RuntimeError, KeyboardInterrupt) as exc:
        print(json.dumps({"status":"BLOCKED_OR_INTERRUPTED","reason":str(exc)}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
