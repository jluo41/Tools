"""Read the non-secret hosting settings owned by a repository root.

`<root>/.server_config/settings.env` is a shell-style file the SPACE owns. The
host reads these keys and nothing else; the file is never executed and secrets
never load:

    SPACE_NAME          display name of the SPACE Home
    DOMAIN              reader-facing origin, e.g. http://100.64.0.9:5599
    BIND_HOST           listener address; TAILSCALE_ADDRESS is the fallback
    TAILSCALE_ADDRESS   this machine's tailnet IP, when the SPACE pins it
    PORT                listener port
    AUTH_FILE           username:password file for a non-loopback host
    ACCESS_MODE         free text shown by status
    NO_AUTH             1/true/yes: the network boundary is the only gate

Aliases still read: PUBLIC_URL and TAILSCALE_URL mean DOMAIN; LOCAL_PORT and
TAILSCALE_PORT mean PORT. A deployment may namespace every key with its own
`<PREFIX>_` (`MYLAB_DOMAIN=...`); the prefix is stripped. Nothing here names one
person or one SPACE: the same host serves any repository that carries the file.

DOMAIN is a variable on purpose. Every link body the host prints or redirects
to (`/b/<board>/<page>`, `/w/<board>/<page>/<tab>`, `/_board/...`) is
origin-relative, so the same body is reached through `http://127.0.0.1:<port>`
on this machine and through the Tailscale IP or a configured public origin from
another device. `domains()` lists the origins one listener answers at.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

CANONICAL_KEYS = ("SPACE_NAME", "DOMAIN", "BIND_HOST", "TAILSCALE_ADDRESS", "PORT",
                  "AUTH_FILE", "ACCESS_MODE", "NO_AUTH")
# alias -> (canonical, rank): a lower rank wins when several aliases are present
ALIAS_KEYS = {"PUBLIC_URL": ("DOMAIN", 1), "TAILSCALE_URL": ("DOMAIN", 2),
              "LOCAL_PORT": ("PORT", 1), "TAILSCALE_PORT": ("PORT", 2)}
SERVER_CONFIG_KEYS = frozenset(CANONICAL_KEYS) | frozenset(ALIAS_KEYS)
_LINE = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$")


def server_config_dir(root: str | Path) -> Path:
    return Path(root).resolve() / ".server_config"


def _value(raw: str) -> str:
    value = raw.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def _known(key: str) -> str:
    """`DOMAIN`, `PUBLIC_URL`, or `ANYPREFIX_DOMAIN` -> the known key; "" otherwise."""
    if key in SERVER_CONFIG_KEYS:
        return key
    # longest suffix first: `X_TAILSCALE_PORT` is the alias, not a prefixed `PORT`
    for known in sorted(SERVER_CONFIG_KEYS, key=len, reverse=True):
        if key.endswith("_" + known):
            return known
    return ""


def load_server_config(root: str | Path) -> dict[str, str]:
    """Load known settings without executing the repository's shell file.

    The result uses canonical keys only: aliases and prefixes are resolved here,
    so callers read `config.get("DOMAIN")` and never see how the file spelt it.
    """
    path = server_config_dir(root) / "settings.env"
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    alias_rank: dict[str, int] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return values
    for raw in lines:
        match = _LINE.match(raw)
        if not match:
            continue
        key = _known(match.group(1))
        if not key:
            continue
        value = _value(match.group(2))
        if key in ALIAS_KEYS:
            canonical, rank = ALIAS_KEYS[key]
            if canonical in values and alias_rank.get(canonical, 0) == 0:
                continue                       # a canonical line already won
            if canonical in values and alias_rank.get(canonical, 9) <= rank:
                continue                       # a better alias already won
            values[canonical] = value
            alias_rank[canonical] = rank
        else:
            values[key] = value
            alias_rank[key] = 0
    if values.get("AUTH_FILE"):
        values["AUTH_FILE"] = os.path.expanduser(os.path.expandvars(values["AUTH_FILE"]))
    return values


def configured_domain(explicit: str, config: dict[str, str]) -> str:
    """The configured DOMAIN, or "": `--public-url`, env HAIPIPE_DOMAIN, settings DOMAIN."""
    for value in (explicit, os.environ.get("HAIPIPE_DOMAIN", ""), config.get("DOMAIN", "")):
        value = (value or "").strip().rstrip("/")
        if value:
            return value
    return ""


def tailscale_ip() -> str:
    """This machine's Tailscale IPv4, or "" when tailscale is absent or down.

    Best effort and fast: one `tailscale ip -4` call with a short timeout, so a
    laptop without Tailscale pays nothing but a `which`.
    """
    import shutil
    import subprocess
    exe = shutil.which("tailscale") or (
        "/Applications/Tailscale.app/Contents/MacOS/Tailscale"
        if os.path.exists("/Applications/Tailscale.app/Contents/MacOS/Tailscale") else "")
    if not exe:
        return ""
    try:
        out = subprocess.run([exe, "ip", "-4"], capture_output=True, text=True, timeout=2)
    except (OSError, subprocess.SubprocessError):
        return ""
    for line in out.stdout.splitlines():
        line = line.strip()
        if re.match(r"^100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+$", line):
            return line
    return ""


def domains(config: dict[str, str], host: str, port: int, public_url: str = "") -> list[tuple[str, str]]:
    """Every origin this server answers at, as (DOMAIN, why) pairs, best first.

    A configured origin (`--public-url`, env `HAIPIPE_DOMAIN`, the `DOMAIN`
    line of settings.env) comes first; then the Tailscale IP when the bind
    reaches it; then loopback, which is always served.
    """
    out: list[tuple[str, str]] = []
    configured = configured_domain(public_url, config)
    if configured:
        out.append((configured, "configured"))
    ts = tailscale_ip() or config.get("TAILSCALE_ADDRESS", "").strip()
    if ts and host in {"0.0.0.0", "::", ts}:
        candidate = f"http://{ts}:{port}"
        if candidate != configured:
            out.append((candidate, "tailscale"))
    loop = f"http://127.0.0.1:{port}"
    if loop != configured:
        out.append((loop, "loopback"))
    return out
