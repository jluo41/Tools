"""Optional HTTP Basic Auth for a private Board server."""

from __future__ import annotations

import base64
import binascii
import hmac
import ipaddress
from pathlib import Path


class AuthConfigError(ValueError):
    """Raised when an auth file cannot safely configure the server."""


def load_users(path: Path) -> dict[str, str]:
    """Load one ``username:password`` account per non-empty line."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AuthConfigError(f"cannot read auth file {path}: {exc}") from exc

    users: dict[str, str] = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise AuthConfigError(f"auth file line {number} must be username:password")
        username, password = line.split(":", 1)
        if not username or not password:
            raise AuthConfigError(f"auth file line {number} has an empty username or password")
        users[username] = password
    if not users:
        raise AuthConfigError(f"auth file {path} has no accounts")
    return users


def parse_basic_header(header: str | None) -> tuple[str, str] | None:
    """Decode a UTF-8 Basic Authorization header without raising to callers."""
    if not header or not header.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError, binascii.Error):
        return None
    if ":" not in decoded:
        return None
    return decoded.split(":", 1)


def credentials_match(header: str | None, users: dict[str, str] | None) -> bool:
    """Return true when auth is disabled or the header matches an account."""
    if users is None:
        return True
    credentials = parse_basic_header(header)
    if credentials is None:
        return False
    username, password = credentials
    expected = users.get(username)
    return expected is not None and hmac.compare_digest(expected, password)


def host_is_loopback(host: str) -> bool:
    """Return whether a bind host is local-only for the auth safety check."""
    if host.strip().lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


class AuthMixin:
    """Gate every handler method that can read, write, or open a WebSocket."""

    auth_users: dict[str, str] | None = None
    auth_realm = "JJ-LUO SPACE"

    @classmethod
    def configure_auth(cls, path: Path | None) -> None:
        cls.auth_users = load_users(path) if path else None

    def require_auth(self) -> bool:
        if credentials_match(self.headers.get("Authorization"), self.auth_users):
            return True
        body = b"Authentication required.\n"
        self.send_response(401)
        self.send_header(
            "WWW-Authenticate",
            f'Basic realm="{self.auth_realm}", charset="UTF-8"',
        )
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return False
