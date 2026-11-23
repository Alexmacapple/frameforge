"""L'arrêt d'un rendu ne doit laisser aucun processus en vie.

Constat de l'expérience de révision et reprise (23 novembre 2026) : après une interruption, les
processus Chrome lancés par HyperFrames survivaient, rattachés au processus 1. Ils vivent dans un
autre groupe de processus que la commande arrêtée ; le test reproduit cette forme sans HyperFrames.
"""

import importlib
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN.parent / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")

# Le parent lance un petit-fils dans sa propre session, comme le fait un navigateur, puis attend.
PARENT = """
import subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
print(child.pid, flush=True)
time.sleep(120)
"""

# Cas constaté sur HyperFrames : la commande ignore le premier signal et, pendant le délai de
# grâce, lance un nouveau petit-fils dans sa propre session. Son numéro est écrit dans un fichier.
RESPAWNING_PARENT = """
import signal, subprocess, sys, time
def respawn(signum, frame):
    late = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    open(sys.argv[1], "w").write(str(late.pid))
signal.signal(signal.SIGTERM, respawn)
print("prêt", flush=True)
time.sleep(120)
"""


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # Un processus terminé mais pas encore récolté répond encore : on regarde son état.
    state = subprocess.run(
        ["ps", "-o", "stat=", "-p", str(pid)],
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(state.stdout.strip()) and not state.stdout.strip().startswith("Z")


class InterruptionTests(unittest.TestCase):
    def setUp(self):
        self.parent = subprocess.Popen(
            [sys.executable, "-c", PARENT],
            start_new_session=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        assert self.parent.stdout is not None
        self.grandchild = int(self.parent.stdout.readline())

    def tearDown(self):
        for pid in (self.grandchild, self.parent.pid):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.parent.wait(timeout=5)
        wrapper.child = None

    def test_descendant_in_another_session_is_found(self):
        self.assertIn(self.grandchild, wrapper.descendants(self.parent.pid))

    def test_stopping_the_render_leaves_no_descendant_alive(self):
        wrapper.child = self.parent
        wrapper.stop_child()
        deadline = time.time() + 5
        while alive(self.grandchild) and time.time() < deadline:
            time.sleep(0.1)
        self.assertFalse(
            alive(self.grandchild), "un descendant du rendu arrêté est encore en vie"
        )
        self.assertIsNotNone(self.parent.poll())

    def test_unrelated_process_is_left_alone(self):
        other = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(60)"],
            start_new_session=True,
        )
        try:
            wrapper.child = self.parent
            wrapper.stop_child()
            self.assertTrue(
                alive(other.pid), "un processus étranger au rendu a été arrêté"
            )
        finally:
            other.kill()
            other.wait(timeout=5)


class LateDescendantTests(unittest.TestCase):
    def test_descendant_started_during_the_grace_period_is_stopped_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "pid"
            parent = subprocess.Popen([sys.executable, "-c", RESPAWNING_PARENT, str(note)], start_new_session=True,
                                      stdout=subprocess.PIPE, text=True)
            assert parent.stdout is not None
            parent.stdout.readline()
            late = None
            try:
                wrapper.child = parent
                wrapper.stop_child()
                late = int(note.read_text())
                deadline = time.time() + 5
                while alive(late) and time.time() < deadline:
                    time.sleep(0.1)
                self.assertFalse(alive(late), "un processus lancé pendant le délai de grâce est encore en vie")
            finally:
                for pid in (late, parent.pid):
                    if pid:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                parent.wait(timeout=5)
                wrapper.child = None


if __name__ == "__main__":
    unittest.main()
