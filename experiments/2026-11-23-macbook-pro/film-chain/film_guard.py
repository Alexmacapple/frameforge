"""Garde de rendu commun aux films produits depuis une fiche.

Chaque film garde son propre render_guarded.py, réduit à ses paramètres : dossier, fichiers,
empreintes, film de sortie. Ce module porte la logique, identique pour tous.

Les empreintes figent une fixture technique : elles ne valent ni approbation éditoriale
ni autorisation de diffusion. Modifier le code et les références ensemble n'est pas une
approbation indépendante.

PDG-LARGE-FILE-JUSTIFICATION: une seule responsabilité, garder un rendu ; précontrôle et validation
de sortie partagent les mêmes références et se lisent ensemble.
"""

import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

CHAIN = Path(__file__).resolve().parent
# Le wrapper V2 est réutilisé tel quel ; il importe lui-même son voisin guarded_hyperframes.
sys.path.insert(0, str(CHAIN.parent / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")
sys.path.insert(0, str(CHAIN))
fiche_check = importlib.import_module("check_manifest")
fiche_build = importlib.import_module("build_from_fiche")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def video_stream_hash(path):
    out = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-map",
            "0:v:0",
            "-c",
            "copy",
            "-f",
            "streamhash",
            "-hash",
            "sha256",
            "-",
        ]
    )
    return out.decode().strip().split("=")[-1]


def packets_hash(path):
    """Empreinte de tous les paquets de tous les flux, avec leurs horodatages et l'en-tête des flux.

    Complète l'empreinte du flux vidéo, qui ne porte que le contenu des paquets : un film dont les
    images sont décalées dans le temps, ou qui porte un flux de plus, change cette empreinte-ci.
    """
    out = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-map",
            "0",
            "-c",
            "copy",
            "-f",
            "framemd5",
            "-",
        ]
    )
    return hashlib.sha256(out).hexdigest()


def receipt_path(output):
    """Reçu de rendu, posé à côté du film : de quelles entrées ce fichier-là est sorti."""
    return Path(str(output) + ".receipt.json")


def write_receipt(output, inputs_sha256):
    """Écrit le reçu en une fois : un reçu à moitié écrit ne doit pas pouvoir être lu."""
    target = receipt_path(output)
    text = (
        json.dumps(
            {"output_sha256": sha(output), "inputs_sha256": inputs_sha256}, indent=2
        )
        + "\n"
    )
    # Fichier temporaire neuf, au nom imprévisible : un lien posé d'avance à un nom connu ferait
    # écrire le reçu ailleurs, jusque dans le film lui-même.
    handle, partial = tempfile.mkstemp(dir=target.parent, prefix=target.name + ".")
    try:
        with os.fdopen(handle, "w") as stream:
            stream.write(text)
        # Le remplacement porte sur le nom : un lien au nom du reçu est remplacé, pas suivi.
        os.replace(partial, target)
    except BaseException:
        Path(partial).unlink(missing_ok=True)
        raise


REFERENCE_KEYS = (
    "expected_duration_s",
    "expected_fps",
    "expected_video_stream_sha256",
    "expected_pcm_sha256",
    "expected_packets_sha256",
    "expected_format_tags",
)


class FilmGuard:
    """Précontrôle des entrées et validation de la sortie d'un film.

    prefix nomme les motifs de refus (« film », « kokoro ») ; pins sont les trois empreintes
    figées dans le fichier du film : manifeste d'entrées, composition, référence de sortie.
    """

    def __init__(
        self, root, prefix, media, config, pins_ref, reference_ref, output, pins
    ):
        self.root = Path(root)
        self.prefix = prefix
        self.media = tuple(media)
        self.config = tuple(config)
        self.pins_ref = pins_ref
        self.reference_ref = reference_ref
        self.output = self.root / output
        self.pin_manifest, self.pin_html, self.pin_reference = pins

    def refuse(self, reason, detail=""):
        return ValueError(
            f"{self.prefix}_{reason}" + (f" : {detail}" if detail else "")
        )

    def load_fiche(self):
        return json.loads((self.root / "provenance-manifest.json").read_text())

    def fiche_failures(self, fiche=None):
        """Noms des contrôles en échec ; les UNVERIFIED déclarés ne bloquent pas le rendu."""
        results = fiche_check.check_data(fiche or self.load_fiche(), self.root)
        return sorted({r["check"] for r in results if r["status"] == "FAIL"})

    def differs_from_fiche(self, fiche):
        """Ce que le garde déclare autrement que la fiche : empreintes, film de sortie, médias."""
        cited = (
            {fiche["capture"]["media_ref"]}
            | {scene["narration"]["audio_ref"] for scene in fiche["scenes"]}
            # Le fichier d'un insert est une entrée du rendu, comme la capture et les voix.
            | {s["insert_ref"] for s in fiche["scenes"] if s["shot_type"] == "insert"}
        )
        checks = (
            ("pins_ref", fiche["pins_ref"] != self.pins_ref),
            ("output", self.root / fiche["film"]["output_ref"] != self.output),
            ("media", cited != set(self.media)),
        )
        return [name for name, differs in checks if differs]

    def preflight(self, reference, candidate, load_fiche=None, fiche_failures=None):
        """load_fiche et fiche_failures permettent au fichier du film de fournir les siens."""
        load_fiche = load_fiche or self.load_fiche
        fiche_failures = fiche_failures or self.fiche_failures
        if sha(reference) != self.pin_html or sha(candidate) != self.pin_html:
            raise self.refuse("reference_or_candidate_changed")
        root = Path(candidate).parent
        manifest = root / self.pins_ref
        if sha(manifest) != self.pin_manifest:
            raise self.refuse("manifest_changed")
        for name, expected in json.loads(manifest.read_text()).items():
            asset = root / name
            if not asset.is_file() or sha(asset) != expected:
                raise self.refuse("asset_changed:" + name)
        if sha(root / self.reference_ref) != self.pin_reference:
            raise self.refuse("output_reference_changed")
        # La fiche du projet doit être cohérente avec les fichiers qu'elle cite. Elle est lue dans
        # le projet d'origine, y compris quand ce précontrôle est rejoué sur la copie isolée : la
        # fiche renvoie à des documents voisins que la copie n'embarque pas, et les empreintes
        # ci-dessus garantissent déjà que la copie porte la même fiche.
        failures = fiche_failures()
        if failures:
            raise self.refuse("fiche_incoherent:" + ",".join(failures))
        # La fiche est la seule source des fichiers texte : ceux du projet doivent être ceux
        # qu'elle génère.
        stale = fiche_build.stale_files(load_fiche(), self.root)
        if stale:
            raise self.refuse("files_not_generated_from_fiche:" + ",".join(stale))
        fiche = load_fiche()
        # Le garde et la fiche doivent parler des mêmes fichiers : sinon la fiche peut être
        # contrôlée contre d'autres empreintes, ou décrire un autre film que celui qui est rendu.
        mismatch = self.differs_from_fiche(fiche)
        if mismatch:
            raise self.refuse("guard_differs_from_fiche:" + ",".join(mismatch))
        status = fiche["film"]["approval"]["status"]
        # Un film dont l'approbation a été retirée ne se rend pas sous ce statut.
        if status == "REVOKED":
            raise self.refuse("fiche_revoked")
        # Une approbation qui ne dit pas de quelles entrées le film est sorti ne permet pas de
        # voir qu'elles ont changé : effacer ce champ ne doit pas rouvrir le rendu.
        if status != "DRAFT" and fiche["film"]["inputs_sha256"] is None:
            raise self.refuse("approval_not_tied_to_inputs")
        return True

    def validate_output(self, path, load_fiche=None):
        """load_fiche permet au fichier du film de fournir sa fiche, comme pour le précontrôle."""
        try:
            return self.validate_probed_output(path, load_fiche)
        except (KeyError, IndexError, TypeError) as exc:
            # Sortie de ffprobe ou référence de forme inattendue : un refus nommé, pas une trace.
            raise self.refuse("output_unreadable") from exc

    def validate_probed_output(self, path, load_fiche=None):
        reference = json.loads((self.root / self.reference_ref).read_text())
        # Une référence incomplète ne vaut pas « contrôle non demandé » : elle est refusée.
        if any(key not in reference for key in REFERENCE_KEYS):
            raise self.refuse("output_reference_incomplete")
        duration, fps = reference["expected_duration_s"], reference["expected_fps"]
        data = json.loads(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration:format_tags:stream=codec_type,codec_name,width,height,nb_frames,avg_frame_rate,"
                    "duration,sample_aspect_ratio,display_aspect_ratio:stream_side_data=side_data_type",
                    "-of",
                    "json",
                    str(path),
                ]
            )
        )
        if abs(float(data["format"]["duration"]) - duration) > 0.08:
            raise self.refuse("output_duration_invalid")
        video = [s for s in data["streams"] if s["codec_type"] == "video"]
        audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
        # Une vidéo et un son, rien d'autre : ni sous-titres ajoutés, ni piste de données.
        if len(data["streams"]) != 2 or len(video) != 1 or len(audio) != 1:
            raise self.refuse("output_streams_invalid")
        if video[0].get("codec_name") != "h264" or (
            video[0].get("width"),
            video[0].get("height"),
        ) != (1920, 1080):
            raise self.refuse("output_video_invalid")
        # Le fichier ne doit rien dire au lecteur qui change l'affichage des images : ni rotation
        # ou miroir (données annexes du flux), ni format d'affichage différent de celui des images.
        if (
            any(s.get("side_data_list") for s in data["streams"])
            or video[0].get("sample_aspect_ratio") != "1:1"
            or video[0].get("display_aspect_ratio") != "16:9"
        ):
            raise self.refuse("output_display_altered")
        num, den = map(int, video[0].get("avg_frame_rate", "0/0").split("/"))
        if (
            den == 0
            or abs(num / den - fps) > 0.01
            or int(video[0].get("nb_frames") or 0) < duration * fps
        ):
            raise self.refuse("output_framerate_invalid")
        if (
            audio[0].get("codec_name") != "aac"
            or float(audio[0].get("duration") or 0) < duration - 0.1
        ):
            raise self.refuse("output_audio_invalid")
        # Les images doivent être exactement celles du brouillon témoin de référence.
        if video_stream_hash(path) != reference["expected_video_stream_sha256"]:
            raise self.refuse("output_video_changed")
        pcm = subprocess.check_output(
            [
                "ffmpeg",
                "-v",
                "error",
                "-i",
                str(path),
                "-map",
                "0:a:0",
                "-f",
                "s16le",
                "-ac",
                "2",
                "-ar",
                "48000",
                "-",
            ]
        )
        if hashlib.sha256(pcm).hexdigest() != reference["expected_pcm_sha256"]:
            raise self.refuse("output_audio_changed")
        # Mêmes images et même son ne suffisent pas : chaque paquet doit aussi tomber au même instant.
        if packets_hash(path) != reference["expected_packets_sha256"]:
            raise self.refuse("output_packets_changed")
        if data["format"].get("tags", {}) != reference["expected_format_tags"]:
            raise self.refuse("output_tags_changed")
        # Quand la fiche porte l'empreinte d'un film, le rendu doit redonner ce film-là, fichier
        # entier. Un brouillon jamais rendu n'a pas d'empreinte : rien à comparer.
        approved = (load_fiche or self.load_fiche)()["film"]["output_sha256"]
        if approved and sha(path) != approved:
            raise self.refuse("output_differs_from_approved_film")
        return True

    def main(self, preflight, validate_output):
        """Lance le rendu gardé ; les deux fonctions viennent du fichier du film."""
        args = SimpleNamespace(
            project=self.root,
            baseline=self.root / "baseline.html",
            candidate=self.root / "index.html",
            output=self.output,
        )
        try:
            # Un film présent sans son reçu vient d'un rendu arrêté entre le dépôt et le reçu :
            # le dire, plutôt que laisser le lanceur répondre seulement que le film existe.
            if self.output.exists() and not receipt_path(self.output).is_file():
                raise self.refuse(
                    "output_without_receipt",
                    "film présent sans reçu de rendu (rendu interrompu ?) : "
                    "le déplacer ailleurs, puis rendre de nouveau",
                )
            # Relevé avant le rendu : le précontrôle refuse si ce fichier ou une entrée a changé.
            inputs = fiche_check.inputs_fingerprint(
                json.loads((self.root / self.pins_ref).read_text())
            )
            result = wrapper.run(
                args,
                preflight_fn=preflight,
                media=self.media,
                config=self.config,
                output_validator=validate_output,
            )
            # Le film est en place : on note de quelles entrées il sort, pour repin.py.
            write_receipt(self.output, inputs)
        except (
            ValueError,
            OSError,
            RuntimeError,
            # Recouvre un outil en échec et un outil qui dépasse son délai.
            subprocess.SubprocessError,
            KeyboardInterrupt,
        ) as exc:
            print(json.dumps({"status": "BLOCKED_OR_INTERRUPTED", "reason": str(exc)}))
            return 2
        print(json.dumps(result))
        return 0
