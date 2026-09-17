"""Optional HTTP Basic Auth for a private Board server."""

from __future__ import annotations

import base64
import binascii
import hmac
import ipaddress
from pathlib import Path
from urllib.parse import unquote, urlsplit


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
    public_read = False
    auth_realm = "JJ-LUO SPACE"
    # Domain presenters that are explicitly read-only may opt into the same
    # anonymous-read boundary as generated Board pages.  Keep this allowlist
    # narrow: POST twins, chat, writes, and every other workspace route remain
    # authenticated when --public-read is enabled.
    public_read_live_routes = {"/_board/design", "/_board/design-board", "/_board/design-bundle",
                               "/_board/insight-board", "/_board/insight"}

    @classmethod
    def configure_auth(cls, path: Path | None) -> None:
        cls.auth_users = load_users(path) if path else None

    def is_public_board_read_request(self) -> bool:
        """Allow anonymous GET/HEAD for generated pages and safe projections."""
        if not self.public_read or self.command not in {"GET", "HEAD"}:
            return False
        clean = unquote(urlsplit(self.path).path)
        if clean in self.public_read_live_routes:
            return True
        if clean.startswith("/b/"):
            return True
        try:
            root = Path(self.root).resolve()
            target = (root / clean.lstrip("/")).resolve()
            target.relative_to(root)
        except (AttributeError, OSError, ValueError):
            return False
        probe = target if target.is_dir() else target.parent
        while probe != root and root in probe.parents:
            if probe.name == "board" and (probe.parent / "board.md").is_file():
                return True
            probe = probe.parent
        return False

    def require_request_auth(self) -> bool:
        if self.is_public_board_read_request():
            return True
        return self.require_auth(challenge=not self.public_read)

    def require_auth(self, *, challenge: bool = True) -> bool:
        if credentials_match(self.headers.get("Authorization"), self.auth_users):
            return True
        body = b"Authentication required for interactive Board tools.\n"
        if self.command == "POST":
            # The caller has not consumed the request body yet.  Keeping this
            # HTTP/1.1 connection alive would make BaseHTTPRequestHandler read
            # that JSON body as the next request line (for example
            # ``{"path": ...}GET``), producing a browser-visible 400/501.
            self.close_connection = True
        self.send_response(401 if challenge else 403)
        if challenge:
            self.send_header(
                "WWW-Authenticate",
                f'Basic realm="{self.auth_realm}", charset="UTF-8"',
            )
        if self.command == "POST":
            self.send_header("Connection", "close")
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return False
