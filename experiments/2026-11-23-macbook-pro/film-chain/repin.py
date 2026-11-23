"""Refige les empreintes d'un film après un changement voulu de ses entrées.

Usage, depuis n'importe où :
  python3 repin.py DOSSIER_DU_FILM --check           rien n'est écrit ; code 1 si une empreinte est périmée
  python3 repin.py DOSSIER_DU_FILM                   recalcule le fichier d'empreintes et le garde du film
  python3 repin.py DOSSIER_DU_FILM --record-output   reporte d'abord l'empreinte du film rendu dans la fiche
                                                     (le film doit d'abord passer le garde ; sinon rien n'est écrit)

Un film neuf demande deux rendus : rendre, lancer --record-output, rendre de nouveau.
Refiger n'est pas approuver : cet outil affiche chaque empreinte qu'il change, à relire avant commit.
La liste des fichiers figés n'est jamais modifiée ici ; elle se décide dans le fichier d'empreintes.
"""

import hashlib
import importlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
inputs_fingerprint = importlib.import_module("check_manifest").inputs_fingerprint

CONSTANT = r'({name} = \(?\s*")([0-9a-f]{{64}})(")'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def settings(film):
    """Noms déclarés dans le garde du film : fichier d'empreintes, référence de sortie, film."""
    text = (film / "render_guarded.py").read_text()
    out, missing = {}, []
    for key in ("pins_ref", "reference_ref", "output"):
        match = re.search(rf'{key}="([^"]+)"', text)
        if match:
            out[key] = match.group(1)
        else:
            missing.append(key)
    if missing:
        raise ValueError("paramètre introuvable dans render_guarded.py : " + ", ".join(missing))
    return out


def expected(film, pins_text=None):
    """Valeur attendue de chaque constante du garde, d'après les fichiers présents."""
    names = settings(film)
    manifest = (
        hashlib.sha256(pins_text.encode()).hexdigest()
        if pins_text
        else sha(film / names["pins_ref"])
    )
    return {
        "PIN_MANIFEST_SHA256": manifest,
        "PIN_HTML_SHA256": sha(film / "index.html"),
        "PIN_OUTPUT_REFERENCE_SHA256": sha(film / names["reference_ref"]),
    }


def fresh_pins(film):
    names = settings(film)
    pins = json.loads((film / names["pins_ref"]).read_text())
    for name in pins:
        if not (film / name).is_file():
            raise ValueError("fichier figé absent : " + name)
    return names["pins_ref"], pins, {name: sha(film / name) for name in pins}


def stale(film):
    """Empreintes périmées, sans rien écrire."""
    film = Path(film)
    pins_ref, pins, fresh = fresh_pins(film)
    out = [f"{pins_ref}:{name}" for name in pins if pins[name] != fresh[name]]
    guard = (film / "render_guarded.py").read_text()
    pins_text = json.dumps(fresh, indent=2) + "\n" if out else None
    for name, value in expected(film, pins_text).items():
        match = re.search(CONSTANT.format(name=name), guard)
        if not match or match.group(2) != value:
            out.append(name)
    return sorted(out)


def require_constants(film):
    """Refuse tôt un garde où une constante manque : aucune écriture ne doit précéder ce refus."""
    guard = (film / "render_guarded.py").read_text()
    for name in ("PIN_MANIFEST_SHA256", "PIN_HTML_SHA256", "PIN_OUTPUT_REFERENCE_SHA256"):
        if len(re.findall(CONSTANT.format(name=name), guard)) != 1:
            raise ValueError("constante introuvable dans render_guarded.py : " + name)


def refresh(film):
    """Recalcule le fichier d'empreintes puis les constantes du garde ; rend ce qui a changé."""
    film = Path(film)
    require_constants(film)
    changed = stale(film)
    pins_ref, _, fresh = fresh_pins(film)
    (film / pins_ref).write_text(json.dumps(fresh, indent=2) + "\n")
    guard_path = film / "render_guarded.py"
    guard = guard_path.read_text()
    for name, value in expected(film).items():
        guard, count = re.subn(CONSTANT.format(name=name), rf"\g<1>{value}\g<3>", guard)
        if count != 1:
            raise ValueError("constante introuvable dans render_guarded.py : " + name)
    guard_path.write_text(guard)
    return changed


def guard_validator(film):
    """Fonction validate_output du garde du film, chargée depuis son render_guarded.py."""
    spec = importlib.util.spec_from_file_location(f"render_guarded_{abs(hash(str(film)))}", film / "render_guarded.py")
    if spec is None or spec.loader is None:
        raise ValueError("garde du film introuvable : render_guarded.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    validate = getattr(module, "validate_output", None)
    if validate is None:
        raise ValueError("garde du film sans validate_output")
    return validate


def record_output(film, validate=None):
    """Reporte l'empreinte du film rendu dans la fiche, puis refige.

    Le film est d'abord soumis au garde : on n'inscrit pas l'empreinte d'un fichier que le garde
    refuserait. Tout est contrôlé avant la première écriture ; en cas de refus, rien n'est modifié.
    """
    film = Path(film)
    output = film / settings(film)["output"]
    if not output.is_file():
        raise ValueError("film absent : " + str(output))
    fresh_pins(film)
    require_constants(film)
    validate = validate or guard_validator(film)
    try:
        validate(output)
    except subprocess.CalledProcessError as exc:
        raise ValueError("film refusé par le garde : fichier illisible par ffprobe ou ffmpeg") from exc
    except ValueError as exc:
        raise ValueError("film refusé par le garde : " + str(exc)) from exc
    path = film / "provenance-manifest.json"
    fiche = json.loads(path.read_text())
    fiche["film"]["output_sha256"] = sha(output)
    # Le film vient d'être validé contre ces entrées : on note desquelles il est sorti.
    fiche["film"]["inputs_sha256"] = inputs_fingerprint(fresh_pins(film)[2])
    path.write_text(json.dumps(fiche, indent=2, ensure_ascii=False) + "\n")
    return refresh(film)


def main():
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(paths) != 1:
        print(__doc__)
        return 2
    film = Path(paths[0]).resolve()
    try:
        if "--check" in sys.argv[1:]:
            out = stale(film)
            print(
                json.dumps(
                    {"status": "FAIL" if out else "PASS", "stale": out},
                    ensure_ascii=False,
                )
            )
            return 1 if out else 0
        changed = (
            record_output(film) if "--record-output" in sys.argv[1:] else refresh(film)
        )
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "PASS", "refrozen": changed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
