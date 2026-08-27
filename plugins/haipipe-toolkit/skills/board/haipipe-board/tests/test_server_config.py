import os
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from src.server_config import load_server_config  # noqa: E402


class ServerConfigTest(unittest.TestCase):
    def test_reads_only_known_values_without_executing_shell(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".server_config").mkdir()
            (root / ".server_config" / "settings.env").write_text(
                'JJLUO_PUBLIC_URL="http://tailnet.example.test:5601" # reader link\n'
                "export JJLUO_LOCAL_PORT=5601\n"
                "JJLUO_AUTH_FILE=~/Library/Application Support/jjluo/auth\n"
                "SECRET_PASSWORD=do-not-load\n"
                "JJLUO_IGNORED='do-not-load'\n",
                encoding="utf-8",
            )

            values = load_server_config(root)

        self.assertEqual(values["JJLUO_PUBLIC_URL"], "http://tailnet.example.test:5601")
        self.assertEqual(values["JJLUO_LOCAL_PORT"], "5601")
        self.assertEqual(
            values["JJLUO_AUTH_FILE"],
            os.path.expanduser("~/Library/Application Support/jjluo/auth"),
        )
        self.assertNotIn("SECRET_PASSWORD", values)
        self.assertNotIn("JJLUO_IGNORED", values)

    def test_missing_settings_file_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_server_config(directory), {})


if __name__ == "__main__":
    unittest.main()
