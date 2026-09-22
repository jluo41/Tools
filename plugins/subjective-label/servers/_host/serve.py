#!/usr/bin/env python3
"""subjective-label's own host: the 🏷 Labeling workbench on its own process.

    python plugins/subjective-label/servers/_host/serve.py --root <folder> \
        [--port N] [--host IP --auth-file FILE] [--public-url DOMAIN]

This process has its own port, DOMAIN, and auth file, so annotators on a
tailnet reach `<DOMAIN>/w/<board>` (every labeling job on a Board) and
`<DOMAIN>/w/<board>/<page>/labeling` (one job, five Spaces, one write door)
without the terminal, the chat, or any Board write route: those answer 404.

It does not copy the host. It runs the shared haipipe host library,
`plugins/haipipe-toolkit/servers/_host/serve.py`, with `--only labeling`, so
`plugins/haipipe-toolkit` must be checked out beside this plugin. Every other
flag of that host applies unchanged (`--host`, `--port`, `--auth-file`,
`--no-auth`, `--public-url`, `--daemon`); `<root>/.server_config/settings.env`
supplies DOMAIN, BIND_HOST, PORT, AUTH_FILE and SPACE_NAME when omitted.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # plugins/subjective-label/servers/_host
PLUGINS = HERE.parents[2]                                 # plugins/
TOOLKIT_HOST = PLUGINS / "haipipe-toolkit" / "servers" / "_host"
WORKBENCH = "labeling"


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    serve = TOOLKIT_HOST / "serve.py"
    if not serve.is_file():
        sys.exit("subjective-label's host runs the shared haipipe host, which is missing: "
                 f"{serve}\nCheck out plugins/haipipe-toolkit beside plugins/subjective-label.")
    if not any(arg == "--only" or arg.startswith("--only=") for arg in argv):
        argv = ["--only", WORKBENCH] + argv
    if not any(arg == "--space-name" or arg.startswith("--space-name=") for arg in argv):
        argv = ["--space-name", "Labeling"] + argv
    sys.argv = [str(serve)] + argv
    if str(TOOLKIT_HOST) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_HOST))
    runpy.run_path(str(serve), run_name="__main__")


if __name__ == "__main__":
    main()
