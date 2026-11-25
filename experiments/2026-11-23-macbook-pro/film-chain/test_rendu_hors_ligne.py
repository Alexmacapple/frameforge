"""Le rendu gardé et le brouillon témoin tournent sans réseau sortant (ticket 65).

HyperFrames 0.8.33 demande la police Inter à Google Fonts dès qu'une composition nomme Arial.
Mesure du 25 novembre 2026 : le film 47 rendu sans réseau ni cache redonne son empreinte
approuvée, la police téléchargée n'entre donc pas dans l'image. Le rendu est désormais enfermé
dans un bac à sable qui refuse toute connexion sortante, sauf vers la machine elle-même (serveur
local de HyperFrames) : un rendu qui aurait besoin du réseau échoue au lieu de télécharger.
"""

import importlib
import socket
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
sys.path.insert(0, str(CHAIN.parent / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")
witness = importlib.import_module("witness_reference")

# Adresse de documentation (RFC 5737) : jamais routée, aucun trafic réel ne part.
OUTSIDE = ("192.0.2.1", 80)
PROBE = (
    "import socket, sys\n"
    "host, port = sys.argv[1], int(sys.argv[2])\n"
    "s = socket.socket()\n"
    "s.settimeout(2)\n"
    "try:\n"
    "    s.connect((host, port))\n"
    "    print('connecte')\n"
    "except OSError as exc:\n"
    "    print(type(exc).__name__, exc.errno)\n"
)


def probe(prefix, host, port):
    out = subprocess.run(
        [*prefix, sys.executable, "-c", PROBE, host, str(port)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return out.stdout.strip()


def sandbox_prefix():
    """Ce qui précède « npx » dans la commande du garde."""
    cmd = wrapper.render_command(Path("/projet"), Path("/sortie.mp4"))
    return cmd[: cmd.index("npx")]


class RenderCommand(unittest.TestCase):
    def test_la_commande_du_garde_rend_hyperframes_0_8_33_dans_le_bac_a_sable(self):
        cmd = wrapper.render_command(Path("/projet"), Path("/sortie.mp4"))
        self.assertTrue(cmd[0].endswith("sandbox-exec"))
        self.assertEqual(
            cmd[cmd.index("npx") :],
            [
                "npx",
                "--yes",
                "hyperframes@0.8.33",
                "render",
                "/projet",
                "--output=/sortie.mp4",
                "--workers=2",
                "--no-best-effort",
            ],
        )

    def test_le_temoin_utilise_la_meme_commande(self):
        self.assertEqual(
            witness.render_command(Path("/projet"), Path("/sortie.mp4")),
            wrapper.render_command(Path("/projet"), Path("/sortie.mp4")),
        )

    def test_sans_bac_a_sable_le_rendu_est_refuse(self):
        with (
            mock.patch.object(wrapper.shutil, "which", return_value=None),
            self.assertRaisesRegex(ValueError, "no_network_sandbox"),
        ):
            wrapper.render_command(Path("/projet"), Path("/sortie.mp4"))


class NetworkBehaviour(unittest.TestCase):
    def test_connexion_exterieure_refusee_par_le_systeme(self):
        # Hors du bac à sable, la même tentative ne reçoit pas « Operation not permitted ».
        self.assertNotIn("PermissionError 1", probe([], *OUTSIDE))
        self.assertIn("PermissionError 1", probe(sandbox_prefix(), *OUTSIDE))

    def test_connexion_locale_permise(self):
        server = socket.socket()
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        self.addCleanup(server.close)
        port = server.getsockname()[1]
        self.assertEqual(probe(sandbox_prefix(), "127.0.0.1", port), "connecte")


if __name__ == "__main__":
    unittest.main()
