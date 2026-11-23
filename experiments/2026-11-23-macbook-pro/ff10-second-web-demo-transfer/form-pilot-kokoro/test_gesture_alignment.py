"""Recette mesurée des gestes sur le brouillon témoin : pointeur visible et envoi annoncé à temps.

Ces contrôles portent sur des pixels et des repères ; ils ne remplacent pas la revue humaine.
"""

import subprocess
import unittest
from pathlib import Path

D = Path(__file__).resolve().parent
FILM = D / "media/form-kokoro-pointeur-draft.mp4"
# Première partie de la phrase 3 (« Le formulaire est envoyé. »), mesurée sur la piste rendue.
THIRD_SENTENCE_FIRST_PART = (10.375, 11.641)
# Zone du message de confirmation dans l'image 1920×1080.
RESULT_ZONE = "crop=400:30:800:775"
SMALL = (480, 270)


def confirmation_time(film):
    """Instant, en secondes, où le fond vert du message de confirmation apparaît."""
    out = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(film),
            "-vf",
            RESULT_ZONE
            + ",signalstats,metadata=print:key=lavfi.signalstats.SATAVG:file=-",
            "-f",
            "null",
            "-",
        ],
        text=True,
    )
    time = None
    for line in out.splitlines():
        if "pts_time:" in line:
            time = float(line.split("pts_time:")[1].split()[0])
        elif "SATAVG=" in line and float(line.split("=")[1]) > 5:
            return time
    return None


def pointer_pixels(film, at):
    """Nombre de pixels orange du pointeur dans l'image réduite prise à l'instant donné."""
    raw = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{at:.3f}",
            "-i",
            str(film),
            "-frames:v",
            "1",
            "-vf",
            f"scale={SMALL[0]}:{SMALL[1]}:flags=area",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ]
    )
    count = 0
    for i in range(0, len(raw), 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        if r > 200 and 60 < g < 170 and b < 90:
            count += 1
    return count


class GestureAlignmentTests(unittest.TestCase):
    def test_confirmation_appears_while_sending_is_announced(self):
        shown = confirmation_time(FILM)
        assert shown is not None, "message de confirmation jamais affiché"
        start, end = THIRD_SENTENCE_FIRST_PART
        self.assertTrue(
            start <= shown <= end,
            f"confirmation à {shown} s, attendue entre {start} et {end} s",
        )

    def test_pointer_visible_at_each_gesture(self):
        shown = confirmation_time(FILM)
        assert shown is not None, "message de confirmation jamais affiché"
        for label, at in (("nom", 1.7), ("adresse", 5.45), ("envoi", shown - 0.1)):
            self.assertGreater(
                pointer_pixels(FILM, at),
                8,
                f"pointeur absent au geste : {label} ({at:.2f} s)",
            )


if __name__ == "__main__":
    unittest.main()
