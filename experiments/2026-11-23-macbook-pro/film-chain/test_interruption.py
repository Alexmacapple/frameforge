"""L'arrêt d'un rendu ne doit laisser aucun processus en vie.

Constat de l'expérience de révision et reprise (23 novembre 2026) : après une interruption, les
processus Chrome lancés par HyperFrames survivaient, rattachés au processus 1. La revue ShipGuard
du même jour a montré deux cas que le suivi par parenté manquait : un processus lancé par un
descendant pendant l'arrêt, et un processus laissé par une commande déjà terminée. Les processus
du rendu sont donc retrouvés par un jeton hérité dans leur environnement ; ces tests reproduisent
chaque forme sans HyperFrames.
"""

import importlib
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN.parent / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")

SLEEPER = "import time; time.sleep(120)"
# La commande lance un petit-fils dans sa propre session, comme le fait un navigateur, puis attend.
PARENT = f"""
import subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", {SLEEPER!r}], start_new_session=True)
print(child.pid, flush=True)
time.sleep(120)
"""
# La commande lance un petit-fils dans sa propre session puis sort aussitôt : rendu terminé.
FINISHED_PARENT = f"""
import subprocess, sys
child = subprocess.Popen([sys.executable, "-c", {SLEEPER!r}], start_new_session=True)
print(child.pid, flush=True)
"""
# Cas constaté sur HyperFrames : la commande ignore le premier signal et, pendant le délai de
# grâce, lance un nouveau petit-fils dans sa propre session. Son numéro est écrit dans un fichier.
RESPAWNING_PARENT = f"""
import signal, subprocess, sys, time
def respawn(signum, frame):
    late = subprocess.Popen([sys.executable, "-c", {SLEEPER!r}], start_new_session=True)
    open(sys.argv[1], "w").write(str(late.pid))
signal.signal(signal.SIGTERM, respawn)
print("prêt", flush=True)
time.sleep(120)
"""
# Cas de la revue : un petit-fils, dans sa propre session, lance un processus à la réception de
# son propre signal d'arrêt puis sort. Le processus tardif n'a jamais été l'enfant de la commande.
LATE_GRANDCHILD = f"""
import signal, subprocess, sys, time
def last_gasp(signum, frame):
    late = subprocess.Popen([sys.executable, "-c", {SLEEPER!r}], start_new_session=True)
    open(sys.argv[1], "w").write(str(late.pid))
    sys.exit(0)
signal.signal(signal.SIGTERM, last_gasp)
time.sleep(120)
"""
PARENT_OF_LATE_GRANDCHILD = f"""
import subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", {LATE_GRANDCHILD!r}, sys.argv[1]], start_new_session=True)
time.sleep(0.5)
print(child.pid, flush=True)
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


def gone(pid, within=5.0):
    deadline = time.time() + within
    while alive(pid) and time.time() < deadline:
        time.sleep(0.1)
    return not alive(pid)


class RenderCase(unittest.TestCase):
    """Lance une commande comme le fait le rendu : sa propre session, le jeton dans l'environnement."""

    def start(self, script, *args):
        wrapper.token = uuid.uuid4().hex
        parent = subprocess.Popen(
            [sys.executable, "-c", script, *args],
            start_new_session=True,
            stdout=subprocess.PIPE,
            text=True,
            env=dict(os.environ, **{wrapper.TOKEN_NAME: wrapper.token}),
        )
        self.addCleanup(self.reap, parent)
        wrapper.child = parent
        assert parent.stdout is not None
        return parent, parent.stdout.readline().strip()

    def reap(self, parent):
        # Filet de sécurité : tout porteur du jeton de ce test, puis la commande elle-même.
        for pid in [*wrapper.token_holders(), parent.pid]:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        parent.wait(timeout=5)
        if parent.stdout is not None:
            parent.stdout.close()
        wrapper.child = wrapper.token = None


class InterruptionTests(RenderCase):
    def test_descendant_in_another_session_carries_the_token(self):
        parent, line = self.start(PARENT)
        self.assertIn(int(line), wrapper.token_holders())
        self.assertIn(parent.pid, wrapper.token_holders())

    def test_stopping_the_render_leaves_no_descendant_alive(self):
        parent, line = self.start(PARENT)
        wrapper.stop_child()
        self.assertTrue(
            gone(int(line)), "un descendant du rendu arrêté est encore en vie"
        )
        self.assertIsNotNone(parent.poll())

    def test_process_left_by_a_finished_command_is_stopped(self):
        parent, line = self.start(FINISHED_PARENT)
        parent.wait(timeout=5)
        self.assertTrue(alive(int(line)), "le cas n'est pas reproduit")
        wrapper.stop_child()
        self.assertTrue(
            gone(int(line)),
            "un processus laissé par un rendu terminé est encore en vie",
        )

    def test_process_without_the_token_is_left_alone(self):
        # Un processus étranger, enfant direct de ce test, donc parent connu et hors du rendu.
        other = subprocess.Popen(
            [sys.executable, "-c", SLEEPER], start_new_session=True
        )
        self.addCleanup(other.wait, 5)
        self.addCleanup(other.kill)
        self.start(PARENT)
        self.assertNotIn(other.pid, wrapper.token_holders())
        wrapper.stop_child()
        self.assertTrue(alive(other.pid), "un processus étranger au rendu a été arrêté")

    def test_token_given_as_an_argument_of_another_token_is_not_a_match(self):
        # Le jeton d'un autre rendu, plus long, ne doit pas être pris pour celui-ci.
        self.start(PARENT)
        mine = wrapper.token
        other = subprocess.Popen(
            [sys.executable, "-c", SLEEPER],
            start_new_session=True,
            env=dict(os.environ, **{wrapper.TOKEN_NAME: mine + "ff"}),
        )
        self.addCleanup(other.wait, 5)
        self.addCleanup(other.kill)
        self.assertNotIn(other.pid, wrapper.token_holders())


class LateDescendantTests(RenderCase):
    def late_pid(self, script):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        note = Path(tmp.name) / "pid"
        self.start(script, str(note))
        wrapper.stop_child()
        return int(note.read_text())

    def test_descendant_started_during_the_grace_period_is_stopped_too(self):
        late = self.late_pid(RESPAWNING_PARENT)
        self.assertTrue(
            gone(late), "un processus lancé pendant le délai de grâce est encore en vie"
        )

    def test_process_started_by_a_descendant_while_stopping_is_stopped_too(self):
        late = self.late_pid(PARENT_OF_LATE_GRANDCHILD)
        self.assertTrue(
            gone(late),
            "un processus lancé par un descendant pendant l'arrêt est encore en vie",
        )


class FailureTests(RenderCase):
    def test_unreadable_process_table_is_reported_not_taken_for_empty(self):
        self.start(PARENT)
        failed = subprocess.CompletedProcess([], 1, stdout="", stderr="ps: refusé")
        with (
            mock.patch.object(wrapper.subprocess, "run", return_value=failed),
            self.assertRaisesRegex(RuntimeError, "process_table_unavailable"),
        ):
            wrapper.stop_child()

    def test_survivors_are_reported(self):
        parent, line = self.start(FINISHED_PARENT)
        parent.wait(timeout=5)
        with (
            mock.patch.object(wrapper, "STOP_DEADLINE", 0.5),
            mock.patch.object(wrapper.os, "kill"),
            self.assertRaisesRegex(RuntimeError, "render_processes_left: .*" + line),
        ):
            wrapper.stop_child()

    def test_closing_the_terminal_is_handled_like_an_interruption(self):
        self.assertIn(signal.SIGHUP, wrapper.HANDLED_SIGNALS)

    def test_second_signal_during_the_stop_is_ignored(self):
        self.start(PARENT)
        seen = {}

        def note_handlers():
            seen.update({s: signal.getsignal(s) for s in wrapper.HANDLED_SIGNALS})

        previous = {s: signal.getsignal(s) for s in wrapper.HANDLED_SIGNALS}
        self.addCleanup(lambda: [signal.signal(s, h) for s, h in previous.items()])
        with (
            mock.patch.object(wrapper, "stop_child", side_effect=note_handlers),
            self.assertRaises(KeyboardInterrupt),
        ):
            wrapper.interrupted(signal.SIGINT, None)
        self.assertEqual(set(seen.values()), {signal.SIG_IGN})


if __name__ == "__main__":
    unittest.main()
