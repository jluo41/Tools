"""Optional HTTP Basic Auth for a private Board server."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import ipaddress
import time
from email.utils import formatdate
from http.cookies import SimpleCookie
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
    auth_cookie_name = "jjluo_board_session"
    auth_cookie_days = 0
    auth_cookie_key: bytes | None = None

    @classmethod
    def configure_auth(cls, path: Path | None, remember_days: int = 0) -> None:
        if remember_days < 0 or remember_days > 365:
            raise AuthConfigError("auth remember days must be between 0 and 365")
        cls.auth_users = load_users(path) if path else None
        cls.auth_cookie_days = remember_days if cls.auth_users else 0
        if cls.auth_users and cls.auth_cookie_days:
            material = "\n".join(
                f"{username}:{password}"
                for username, password in sorted(cls.auth_users.items())
            ).encode("utf-8")
            cls.auth_cookie_key = hashlib.sha256(
                b"jjluo-board-cookie-v1\0" + material
            ).digest()
        else:
            cls.auth_cookie_key = None

    def _cookie_token(self, username: str, expires: int) -> str:
        payload = f"{username}\n{expires}".encode("utf-8")
        encoded = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
        signature = hmac.new(
            self.auth_cookie_key, encoded.encode("ascii"), hashlib.sha256
        ).hexdigest()
        return f"{encoded}.{signature}"

    def _cookie_user(self) -> str | None:
        if not self.auth_cookie_key or not self.auth_users:
            return None
        try:
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            morsel = cookie.get(self.auth_cookie_name)
            if morsel is None:
                return None
            encoded, signature = morsel.value.rsplit(".", 1)
            expected = hmac.new(
                self.auth_cookie_key, encoded.encode("ascii"), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(expected, signature):
                return None
            padded = encoded + "=" * (-len(encoded) % 4)
            username, expires_text = base64.urlsafe_b64decode(padded).decode("utf-8").split("\n", 1)
            if int(expires_text) <= int(time.time()):
                return None
            return username if username in self.auth_users else None
        except (ValueError, UnicodeDecodeError, binascii.Error):
            return None

    def send_auth_cookie_if_pending(self) -> None:
        username = getattr(self, "_auth_cookie_user", None)
        expires = getattr(self, "_auth_cookie_expires", None)
        if not username or not expires:
            return
        max_age = max(0, expires - int(time.time()))
        secure = (
            self.headers.get("X-Forwarded-Proto", "").lower() == "https"
            or getattr(self, "public_url", "").startswith("https://")
        )
        parts = [
            f"{self.auth_cookie_name}={self._cookie_token(username, expires)}",
            "Path=/",
            f"Max-Age={max_age}",
            f"Expires={formatdate(expires, usegmt=True)}",
            "HttpOnly",
            "SameSite=Lax",
        ]
        if secure:
            parts.append("Secure")
        self.send_header("Set-Cookie", "; ".join(parts))
        self._auth_cookie_user = None
        self._auth_cookie_expires = None

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
        if self.auth_users is None or self._cookie_user() is not None:
            return True
        header = self.headers.get("Authorization")
        if credentials_match(header, self.auth_users):
            if self.auth_cookie_days:
                username, _password = parse_basic_header(header)
                self._auth_cookie_user = username
                self._auth_cookie_expires = int(time.time()) + self.auth_cookie_days * 86400
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
