#!/usr/bin/env python3
"""Tests for the optional private SPACE server authentication."""
import tempfile
import unittest
from pathlib import Path

from live.auth import AuthConfigError, credentials_match, host_is_loopback, load_users


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


if __name__ == "__main__":
    unittest.main()
