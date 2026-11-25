#!/usr/bin/env python3
"""Isolated FF-10 HyperFrames pilot; not a universal FrameForge export guard."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid

from guarded_hyperframes import preflight

MEDIA = ("capture.webm", "voice1.m4a", "voice2.m4a", "voice3.m4a")
CONFIG = ("index.html", "hyperframes.json", "package.json", "captions.srt", "captions.vtt", "transcript.txt")
child = None
# Jeton du rendu en cours : voir token_holders.
TOKEN_NAME = "FF_RENDER_TOKEN"
token = None
# Fermer le terminal (SIGHUP) arrête le rendu comme Ctrl-C.
HANDLED_SIGNALS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)
TERM_GRACE, STOP_DEADLINE = 3.0, 15.0
# Un rendu de film court dure une à deux minutes : au-delà de ce délai, il est tenu pour bloqué.
RENDER_TIMEOUT = float(os.environ.get("FF_RENDER_TIMEOUT_S", "1800"))

# Aucune connexion sortante pendant le rendu, sauf vers la machine elle-même : HyperFrames sert la
# composition par un serveur local. Sans cela, il demande la police Inter à Google Fonts dès qu'une
# composition nomme Arial ; mesure du 25 novembre 2026 (ticket 65) : le film 47 rendu sans réseau
# redonne son empreinte approuvée. Un rendu qui aurait besoin du réseau échoue au lieu de télécharger.
NO_NETWORK_PROFILE = ('(version 1)(allow default)(deny network-outbound)'
                      '(allow network-outbound (remote ip "localhost:*"))'
                      '(allow network-outbound (remote unix-socket))')

def render_command(snapshot, rendered):
    """Commande de rendu HyperFrames 0.8.33, enfermée dans le bac à sable sans réseau."""
    sandbox = shutil.which("sandbox-exec")
    if sandbox is None:
        raise ValueError("no_network_sandbox_unavailable")
    return [sandbox, "-p", NO_NETWORK_PROFILE, "npx", "--yes", "hyperframes@0.8.33", "render",
            str(snapshot), "--output="+str(rendered), "--workers=2", "--no-best-effort"]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def token_holders():
    """PID des processus qui portent le jeton de ce rendu dans leur environnement.

    Le jeton est une valeur aléatoire, propre à ce rendu, donnée à la commande par son
    environnement : tout ce qu'elle lance en hérite, quels que soient son groupe, sa session ou
    son rattachement au processus 1 une fois son parent sorti. Chercher par le jeton plutôt que
    par la parenté trouve aussi un processus lancé pendant l'arrêt, et ne peut pas désigner un
    processus étranger qui aurait repris un numéro. Si ps échoue, on le dit : une table vide
    passerait pour « plus personne à arrêter ».
    """
    if token is None:
        return []
    done = subprocess.run(["ps", "-A", "-wwE", "-o", "pid=,command="], capture_output=True,
                          text=True, check=False, timeout=10)
    if done.returncode != 0:
        raise RuntimeError("process_table_unavailable")
    mark = TOKEN_NAME + "=" + token
    holders = []
    for line in done.stdout.splitlines():
        parts = line.split()
        if parts and parts[0].isdigit() and mark in parts[1:] and int(parts[0]) != os.getpid():
            holders.append(int(parts[0]))
    return holders

def stop_token_holders():
    """Arrête tout porteur du jeton ; rend ceux qui vivent encore à l'échéance.

    La liste est relue à chaque tour : un processus apparu entre deux tours est vu au suivant.
    D'abord SIGTERM, puis SIGKILL après TERM_GRACE secondes.
    """
    start = time.time()
    while True:
        holders = token_holders()
        if not holders or time.time() - start > STOP_DEADLINE:
            return holders
        sig = signal.SIGTERM if time.time() - start < TERM_GRACE else signal.SIGKILL
        for pid in holders:
            try:
                os.kill(pid, sig)
            except (ProcessLookupError, PermissionError):
                pass
        time.sleep(0.1)

def stop_child():
    """Arrête la commande de rendu si elle vit encore, puis tout ce qu'elle a lancé.

    Appelé aussi après un rendu terminé : la commande est sortie, mais un navigateur peut rester.
    """
    if child is not None and child.poll() is None:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(child.pid, sig)
            except ProcessLookupError:
                break
            try:
                child.wait(timeout=8)
                break
            except subprocess.TimeoutExpired:
                continue
    left = stop_token_holders()
    if left:
        raise RuntimeError("render_processes_left: " + ",".join(map(str, left)))

def interrupted(signum, frame):
    # Un second signal pendant l'arrêt ne doit pas interrompre le nettoyage en cours.
    for s in HANDLED_SIGNALS:
        signal.signal(s, signal.SIG_IGN)
    stop_child()
    raise KeyboardInterrupt("guarded render interrupted")

def run(args, preflight_fn=None, media=None, config=None, output_validator=None):
    preflight_fn = preflight_fn or preflight
    media = MEDIA if media is None else tuple(media)
    config = CONFIG if config is None else tuple(config)
    previous = {s: signal.signal(s, interrupted) for s in HANDLED_SIGNALS}
    try:
        return guarded_render(args, preflight_fn, media, config, output_validator)
    finally:
        # Les gestionnaires de qui nous appelle sont rendus tels quels.
        for s, handler in previous.items():
            signal.signal(s, handler)

def guarded_render(args, preflight_fn, media, config, output_validator):
    global child, token
    project, baseline, candidate, output = map(Path, (args.project,args.baseline,args.candidate,args.output))
    if output.exists() or output.is_symlink():
        raise ValueError("output_already_exists")
    if candidate.resolve() != (project/"index.html").resolve():
        raise ValueError("candidate_not_project_entrypoint")
    preflight_fn(baseline,candidate)
    sources=[baseline, candidate, *[project/n for n in media], *[project/n for n in config if (project/n).exists()]]
    hashes={str(p):digest(p) for p in sources}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ff10-isolated-",dir=output.parent) as temp:
        work=Path(temp)
        snapshot=work/"project"
        snapshot.mkdir()
        for name in config + media:
            src=project/name
            if src.exists():
                # Une entrée peut être rangée dans un sous-dossier (insert dans compositions/).
                (snapshot/name).parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(src,snapshot/name)
        baseline_snapshot=work/"baseline.html"
        shutil.copyfile(baseline,baseline_snapshot)
        preflight_fn(baseline_snapshot,snapshot/"index.html")
        for name in config + media:
            src=project/name
            if src.exists() and digest(src)!=digest(snapshot/name):
                raise ValueError("input_changed_while_snapshotting")
        if digest(baseline)!=digest(baseline_snapshot):
            raise ValueError("baseline_changed_while_snapshotting")
        if hashes!={str(p):digest(p) for p in sources}:
            raise ValueError("source_changed_during_preflight")
        # Keep all render inputs private to this invocation. An external mutation
        # of the original project cannot change the bytes HyperFrames reads.
        rendered=work/"rendered.mp4"
        cmd=render_command(snapshot, rendered)
        token=uuid.uuid4().hex
        child=subprocess.Popen(cmd,start_new_session=True,stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE,env=dict(os.environ,**{TOKEN_NAME:token}))
        try:
            try:
                _,err=child.communicate(timeout=RENDER_TIMEOUT)
            except subprocess.TimeoutExpired:
                raise RuntimeError("hyperframes_timeout") from None
            if child.returncode:
                raise RuntimeError("hyperframes_failed: "+err.decode(errors="replace")[-700:])
        finally:
            try:
                stop_child()
            finally:
                child=None
                token=None
        subprocess.run(["ffmpeg","-v","error","-i",str(rendered),"-f","null","-"],
                       check=True,stdout=subprocess.DEVNULL,timeout=300)
        # A project-specific validator must inspect the temporary media before
        # it can acquire the final output name. This remains opt-in for old pilots.
        if output_validator is not None:
            output_validator(rendered)
        # The source may have changed concurrently; this is reported, but the
        # render itself used an isolated, validated snapshot.
        changed=[str(p) for p in sources if digest(p)!=hashes[str(p)]]
        if changed:
            raise ValueError("source_changed_during_render")
        # Le film va être déposé : une interruption à partir d'ici ne doit plus faire dire
        # « bloqué » alors que le film est en place.
        for s in HANDLED_SIGNALS:
            signal.signal(s, signal.SIG_IGN)
        os.link(rendered,output)
    return {"status":"PASS","output":str(output),"sha256":digest(output)}

def main():
    parser=argparse.ArgumentParser()
    for name in ("project","baseline","candidate","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(run(args)))
    except (ValueError,OSError,RuntimeError,subprocess.SubprocessError,KeyboardInterrupt) as exc:
        print(json.dumps({"status":"BLOCKED_OR_INTERRUPTED","reason":str(exc)}))
        return 2
    return 0

if __name__=="__main__":
    sys.exit(main())
