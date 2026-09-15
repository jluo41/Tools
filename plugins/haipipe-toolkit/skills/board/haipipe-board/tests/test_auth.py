#!/usr/bin/env python3
"""Tests for the optional private SPACE server authentication."""
import tempfile
import unittest
from pathlib import Path

from live.auth import AuthConfigError, AuthMixin, credentials_match, host_is_loopback, load_users


class PublicReadProbe(AuthMixin):
    command = "GET"
    path = "/"

    def __init__(self, root: Path, path: str, command: str = "GET"):
        self.root = root
        self.path = path
        self.command = command


class RejectedPostProbe(AuthMixin):
    command = "POST"
    path = "/_board/sessions"
    public_read = True
    auth_users = {"owner": "secret"}
    headers = {}
    close_connection = False

    def __init__(self):
        self.response = None
        self.sent_headers = []
        self.wfile = type("Sink", (), {"write": lambda self, value: None})()

    def send_response(self, code):
        self.response = code

    def send_header(self, name, value):
        self.sent_headers.append((name, value))

    def end_headers(self):
        pass


class AuthTest(unittest.TestCase):
    def test_loads_multiple_accounts_and_colons_in_passwords(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "users.auth"
            path.write_text("# owner\nalice:one:two\nbob:secret\n")
            users = load_users(path)
            self.assertEqual(users, {"alice": "one:two", "bob": "secret"})
            self.assertTrue(credentials_match("Basic YWxpY2U6b25lOnR3bw==", users))
            self.assertFalse(credentials_match("Basic Ym9iOndyb25n", users))

    def test_disabled_auth_accepts_everything(self):
        self.assertTrue(credentials_match(None, None))

    def test_only_loopback_hosts_are_local_only(self):
        self.assertTrue(host_is_loopback("127.0.0.1"))
        self.assertTrue(host_is_loopback("::1"))
        self.assertTrue(host_is_loopback("localhost"))
        self.assertFalse(host_is_loopback("0.0.0.0"))
        self.assertFalse(host_is_loopback("100.64.0.1"))

    def test_malformed_auth_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "users.auth"
            path.write_text("not-an-account\n")
            with self.assertRaises(AuthConfigError):
                load_users(path)

    def test_public_read_accepts_only_generated_board_tree_and_short_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "discoveries" / "b01_topic"
            generated = board / "board"
            generated.mkdir(parents=True)
            (board / "board.md").write_text("# Board\n")
            (generated / "index.html").write_text("ok")
            probe = PublicReadProbe(root, "/discoveries/b01_topic/board/index.html")
            probe.public_read = True
            self.assertTrue(probe.is_public_board_read_request())
            probe.path = "/b/b01_topic"
            self.assertTrue(probe.is_public_board_read_request())
            probe.path = "/discoveries/b01_topic/board.md"
            self.assertFalse(probe.is_public_board_read_request())
            probe.path = "/_term/0123456789ab"
            self.assertFalse(probe.is_public_board_read_request())
            probe.command = "POST"
            probe.path = "/discoveries/b01_topic/board/index.html"
            self.assertFalse(probe.is_public_board_read_request())

    def test_rejected_post_closes_connection_before_body_can_be_reparsed(self):
        probe = RejectedPostProbe()
        self.assertFalse(probe.require_request_auth())
        self.assertEqual(probe.response, 403)
        self.assertTrue(probe.close_connection)
        self.assertIn(("Connection", "close"), probe.sent_headers)


if __name__ == "__main__":
    unittest.main()
