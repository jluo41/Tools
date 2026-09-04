"""Read the non-secret hosting settings owned by a repository root."""

from __future__ import annotations

import os
import re
from pathlib import Path

SERVER_CONFIG_KEYS = frozenset({
    "JJLUO_SPACE_NAME",
    "JJLUO_PUBLIC_URL",
    "JJLUO_TAILSCALE_URL",
    "JJLUO_BIND_HOST",
    "JJLUO_TAILSCALE_ADDRESS",
    "JJLUO_LOCAL_PORT",
    "JJLUO_TAILSCALE_PORT",
    "JJLUO_AUTH_FILE",
    "JJLUO_ACCESS_MODE",
})


def server_config_dir(root: str | Path) -> Path:
    return Path(root).resolve() / ".server_config"


def _value(raw: str) -> str:
    value = raw.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def load_server_config(root: str | Path) -> dict[str, str]:
    """Load known settings without executing the repository's shell file."""
    path = server_config_dir(root) / "settings.env"
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return values
    for raw in lines:
        match = re.match(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$", raw)
        if not match or match.group(1) not in SERVER_CONFIG_KEYS:
            continue
        key, value = match.groups()
        values[key] = _value(value)
    if values.get("JJLUO_AUTH_FILE"):
        values["JJLUO_AUTH_FILE"] = os.path.expanduser(
            os.path.expandvars(values["JJLUO_AUTH_FILE"])
        )
    return values
