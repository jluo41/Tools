import os
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from server_config import configured_domain, load_server_config  # noqa: E402


def _write(root: Path, text: str) -> dict:
    (root / ".server_config").mkdir(exist_ok=True)
    (root / ".server_config" / "settings.env").write_text(text, encoding="utf-8")
    return load_server_config(root)


class ServerConfigTest(unittest.TestCase):
    def test_reads_only_known_values_without_executing_shell(self):
        with tempfile.TemporaryDirectory() as directory:
            values = _write(Path(directory),
                'DOMAIN="http://tailnet.example.test:5601" # reader link\n'
                "export PORT=5601\n"
                "AUTH_FILE=~/Library/Application Support/spaces/auth\n"
                "SECRET_PASSWORD=do-not-load\n"
                "IGNORED='do-not-load'\n")
        self.assertEqual(values["DOMAIN"], "http://tailnet.example.test:5601")
        self.assertEqual(values["PORT"], "5601")
        self.assertEqual(values["AUTH_FILE"],
                         os.path.expanduser("~/Library/Application Support/spaces/auth"))
        self.assertNotIn("SECRET_PASSWORD", values)
        self.assertNotIn("IGNORED", values)

    def test_any_prefix_and_the_old_aliases_resolve_to_canonical_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            values = _write(Path(directory),
                "MYLAB_SPACE_NAME=Lab Space\n"
                "MYLAB_PUBLIC_URL=http://lab.example:5601\n"
                "MYLAB_LOCAL_PORT=5601\n"
                "MYLAB_TAILSCALE_PORT=5602\n"
                "MYLAB_BIND_HOST=0.0.0.0\n"
                "MYLAB_NO_AUTH=1\n")
        self.assertEqual(values, {"SPACE_NAME": "Lab Space", "DOMAIN": "http://lab.example:5601",
                                  "PORT": "5601", "BIND_HOST": "0.0.0.0", "NO_AUTH": "1"})

    def test_a_canonical_line_beats_an_alias_whatever_the_order(self):
        with tempfile.TemporaryDirectory() as directory:
            values = _write(Path(directory),
                "PUBLIC_URL=http://alias.example\nDOMAIN=http://canon.example\n"
                "TAILSCALE_URL=http://later-alias.example\n")
        self.assertEqual(values["DOMAIN"], "http://canon.example")

    def test_configured_domain_order(self):
        with tempfile.TemporaryDirectory() as directory:
            values = _write(Path(directory), "DOMAIN=http://file.example/\n")
        self.assertEqual(configured_domain("", values), "http://file.example")
        self.assertEqual(configured_domain("http://flag.example/", values), "http://flag.example")
        self.assertEqual(configured_domain("", {}), "")

    def test_missing_settings_file_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_server_config(directory), {})


if __name__ == "__main__":
    unittest.main()
