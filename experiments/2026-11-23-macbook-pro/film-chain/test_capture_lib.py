"""Dépôt d'une capture : rien n'est écrasé, rien n'est écrit hors du dossier visé.

Le navigateur est remplacé par un faux module Playwright (FF_PLAYWRIGHT) qui dépose une courte
vidéo ; ffmpeg et capture_lib.cjs sont les vrais. Né du soupçon de l'issue 15 : un lien
symbolique cassé au nom de la capture passait le contrôle d'existence.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent

FAKE_PLAYWRIGHT = """
const fs = require('fs');
const path = require('path');
const chromium = {
  launch: async () => ({
    close: async () => {},
    newContext: async ({ recordVideo }) => ({
      addInitScript: async () => {},
      close: async () => {},
      newPage: async () => ({
        goto: async () => {},
        waitForTimeout: async () => {},
        mouse: { move: async () => {}, click: async () => {} },
        video: () => ({
          path: async () => {
            const taken = path.join(recordVideo.dir, 'prise.webm');
            fs.copyFileSync(process.env.FF_TEST_CLIP, taken);
            return taken;
          },
        }),
      }),
    }),
  }),
};
module.exports = { chromium };
"""

DRIVER = """
const { record } = require(process.argv[2]);
record({
  filmDir: process.argv[3],
  url: 'about:blank',
  durationS: 1,
  mediaRef: 'capture.mp4',
  eventsRef: 'capture-events.json',
  play: async () => ({ observed: { done: true } }),
});
"""


@unittest.skipUnless(
    shutil.which("node") and shutil.which("ffmpeg"), "node et ffmpeg requis"
)
class CaptureDepositTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.shared.cleanup)
        shared = Path(cls.shared.name)
        cls.clip = shared / "clip.webm"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i"]
            + ["color=c=gray:s=320x180:r=30:d=1", str(cls.clip)],
            check=True,
        )
        (shared / "playwright").mkdir()
        (shared / "playwright" / "index.js").write_text(FAKE_PLAYWRIGHT)
        cls.driver = shared / "drive.cjs"
        cls.driver.write_text(DRIVER)

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.film = Path(tmp.name) / "film"
        self.film.mkdir()
        self.outside = Path(tmp.name) / "ailleurs"
        self.outside.mkdir()

    def capture(self):
        shared = Path(self.shared.name)
        return subprocess.run(
            ["node", self.driver, CHAIN / "capture_lib.cjs", self.film],
            env={
                "PATH": os.environ["PATH"],
                "FF_PLAYWRIGHT": str(shared / "playwright"),
                "FF_TEST_CLIP": str(self.clip),
            },
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def left_in_film(self):
        return sorted(
            str(p.relative_to(self.film)) for p in self.film.rglob("*") if p.is_file()
        )

    def test_capture_is_deposited_with_its_journal_and_raw_take(self):
        done = self.capture()
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(
            self.left_in_film(),
            ["capture-events.json", "capture.mp4", "media/capture-pointer.webm"],
        )
        journal = json.loads((self.film / "capture-events.json").read_text())
        self.assertEqual(journal["observed"], {"done": True})

    def test_second_capture_is_refused_and_the_first_is_kept(self):
        self.assertEqual(self.capture().returncode, 0)
        first = (self.film / "capture.mp4").read_bytes()
        again = self.capture()
        self.assertEqual(again.returncode, 1)
        self.assertIn("capture existante, non écrasée", again.stderr)
        self.assertEqual((self.film / "capture.mp4").read_bytes(), first)

    def test_dangling_link_at_a_deposit_name_is_refused_before_anything_is_written(
        self,
    ):
        for name in ("capture.mp4", "capture-events.json"):
            with self.subTest(name=name):
                link = self.film / name
                link.symlink_to(self.outside / name)
                refused = self.capture()
                self.assertEqual(refused.returncode, 1)
                self.assertIn("capture existante, non écrasée", refused.stderr)
                self.assertEqual(list(self.outside.iterdir()), [])
                self.assertEqual(self.left_in_film(), [])
                link.unlink()

    def test_raw_take_never_goes_through_a_link(self):
        (self.film / "media").mkdir()
        (self.film / "media" / "capture-pointer.webm").symlink_to(
            self.outside / "prise.webm"
        )
        done = self.capture()
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(list(self.outside.iterdir()), [])
        self.assertTrue((self.film / "media" / "capture-pointer-2.webm").is_file())

    def test_media_folder_that_is_a_link_is_refused(self):
        (self.film / "media").symlink_to(self.outside, target_is_directory=True)
        refused = self.capture()
        self.assertEqual(refused.returncode, 1)
        self.assertIn("media est un lien", refused.stderr)
        self.assertEqual(list(self.outside.iterdir()), [])
        self.assertEqual(self.left_in_film(), [])


if __name__ == "__main__":
    unittest.main()
