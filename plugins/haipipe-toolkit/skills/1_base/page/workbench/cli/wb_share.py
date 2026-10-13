#!/usr/bin/env python3
"""/wb share <folder> <email>: give one person (or a group) a Block, Job, Task or whole Project on the share host
(b10 s52; JL 261012: "How could i share one block to others? For example, for the b10.").

    wb.py share <folder> <email|group:name> [--level view] [--share-root DIR]
    wb.py share <folder> --people <name>     a list file you keep: .server_config/people/<name>.txt, one email a line
    wb.py share <folder>                     who can open it now, and its link; nothing written
    wb.py <folder> share <email>             the same, folder first (JL 261012: "/wb xxxx to share")
    wb.py share --list [--share-root DIR]
    wb.py share --serve [<folder>]           start this SPACE's door: serve.py --share on its table's port

It writes one grant into the share root's `.server_config/access.yaml` (live/share.py add_grant) and prints the
link to send. The share host (`serve.py --share`) reads the table again on its next request, so nothing restarts.
The person opens the link, types that email, and signs in with the code it receives (mail: share.env).

The share root is the folder the share host serves: the nearest folder above the shared one that holds
`.server_config/access.yaml`, else this SPACE's root; `--share-root` names it outright. The folder must sit inside
it. One door per SPACE (JL 261012: "physician.jjluo.com, welldoc.jjluo.com, drfirst.jjluo.com, reach.jjluo.com,
jluo41.jjluo.com, knowledge.jjluo.com"; Tools-SPACE's block.jjluo.com was dropped the same day): each SPACE's table
names its door, `public_url:` and `port:` (127.0.0.1 only; the tunnel reaches it), and `--serve` starts it. A SPACE
with no table has no door, so nothing is shared there and nothing is written.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode

import wb

sys.path.insert(0, str(wb.SERVERS / "_host"))
from live import share as S  # noqa: E402


def share_root(arg: str | None, here: Path) -> Path:
    """--share-root, else the nearest folder above `here` whose .server_config holds access.yaml (a SPACE's own,
    one door per SPACE since 261012), else the SPACE root."""
    if arg:
        return Path(arg).expanduser().resolve()
    for p in (here, *here.parents):
        if (p / ".server_config" / "access.yaml").is_file():
            return p.resolve()
    root = wb.space_root(here)
    if root is None:
        raise SystemExit("wb share: no share root above this folder; pass --share-root")
    return root.resolve()


def link(root: Path, rel: str) -> str:
    cfg = S.ShareConfig.load(root)
    base = cfg.public_url or "https://<the share host>"
    return f"{base.rstrip('/')}/_board/workbench?" + urlencode({"path": rel, "studio": "1"}, safe="/")


def who_has(root: Path, rel: str) -> int:
    """`wb.py share <folder>` with nobody named: who can open it now (a grant on it or a folder above it, owners
    aside) and its link. Nothing is written."""
    cfg = S.ShareConfig.load(root)
    rows = [(who, what, lvl) for who, what, lvl in cfg.grants if rel == what or rel.startswith(what + "/")]
    names = {v: k for k, v in S.LEVELS.items()}
    print(f"{'🔗' if rows else '🔒'} {rel}  on {cfg.public_url or '-'}: "
          + (f"{len(rows)} grant{'s' if len(rows) != 1 else ''}" if rows else "shared with nobody yet"))
    for who, what, lvl in rows:
        k = len(cfg.groups.get(who[6:], ()))
        n = f"  ({k} {'person' if k == 1 else 'people'})" if who.startswith("group:") else ""
        print(f"  {who:<32} {names[lvl]:<7} {what if what != rel else '(this folder)'}{n}")
    print(f"link    {link(root, rel)}")
    if not rows:
        print("share   wb.py share <folder> <email>   or   --people <list>")
    return 0


def serve(root: Path) -> int:
    """Start the share root's door: serve.py --share on 127.0.0.1:<port>, named by its table's public_url. A door
    already up on that port is left running."""
    cfg = S.ShareConfig.load(root)
    if not (cfg.port and cfg.public_url):
        raise SystemExit(f"wb share: {root.name}/.server_config/access.yaml needs port: and public_url: to serve")
    up = [s for s in wb.servers(root, share=True) if s.port == cfg.port]
    if up:
        print(f"✅ {cfg.public_url} already up: 127.0.0.1:{cfg.port}, pid {up[0].pid}")
        return 0
    if not wb._port_free(cfg.port):
        raise SystemExit(f"wb share: port {cfg.port} is held by another process; see lsof -nP -iTCP:{cfg.port}")
    name = re.sub(r"[^a-z0-9]+", "-", root.name.lower()).strip("-")
    log = f"/tmp/{name}-share-{cfg.port}.log"
    args = ["--root", str(root), "--host", "127.0.0.1", "--port", str(cfg.port), "--share", "--no-terminal",
            "--space-name", root.name, "--public-url", cfg.public_url, "--daemon", log]
    subprocess.Popen([wb._python(root), str(wb.SERVERS / "_host" / "serve.py"), *args], cwd=root,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    if not wb._until(lambda: wb._answers(f"http://127.0.0.1:{cfg.port}"), 40):
        raise SystemExit(f"wb share: the door on {cfg.port} did not answer; see {log}")
    print(f"✅ {cfg.public_url} → 127.0.0.1:{cfg.port}  root {root.name}  log {log}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="wb.py share", description=__doc__.split("\n\n")[0])
    ap.add_argument("folder", nargs="?")
    ap.add_argument("who", nargs="?", help="a JHU email (jhu.edu, jh.edu, jhmi.edu), group:<name>, or anyone@jhu (every JHU email)")
    ap.add_argument("--level", default="view", choices=["view", "comment", "edit"])
    ap.add_argument("--share-root")
    ap.add_argument("--list", action="store_true", help="print the grants, one per line")
    ap.add_argument("--serve", action="store_true", help="start this SPACE's door (its table's port and public_url)")
    ap.add_argument("--people", metavar="NAME", help="share with everyone in .server_config/people/NAME.txt "
                    "(made if missing): one JHU email per line, edits apply at the next click")
    a = ap.parse_args(argv)
    start = Path(a.folder).expanduser().resolve() if a.folder else Path.cwd().resolve()
    root = share_root(a.share_root, start)
    if not (root / ".server_config" / "access.yaml").is_file():
        raise SystemExit(f"wb share: {root.name} has no share door (no .server_config/access.yaml naming port: and "
                         f"public_url:), so nothing would serve the link; nothing written")
    if a.serve:
        return serve(root)
    if a.list:
        cfg = S.ShareConfig.load(root)
        print(f"share root {root}  door {cfg.public_url or '-'} (127.0.0.1:{cfg.port or '-'})  "
              f"owners: {', '.join(sorted(cfg.owners)) or '-'}")
        for who, what, lvl in cfg.grants:
            name = {v: k for k, v in S.LEVELS.items()}[lvl]
            print(f"  {who:<32} {name:<7} {what}")
        return 0
    if not a.folder:
        ap.error("give a folder and an email, or a folder and --people <name> (or --list)")
    folder = Path(a.folder).expanduser()
    folder = (folder if folder.is_absolute() else Path.cwd() / folder).resolve()
    if not folder.is_dir():
        raise SystemExit(f"wb share: {a.folder} is not a folder")
    try:
        rel = folder.relative_to(root).as_posix()
    except ValueError:
        raise SystemExit(f"wb share: {folder} is not inside the share root {root}; pass --share-root")
    if not (a.who or a.people):
        return who_has(root, rel)
    listed = None
    try:
        if a.people:
            listed = S.people_group(root, a.people)
        grant = S.add_grant(root, f"group:{a.people}" if a.people else a.who, rel, a.level)
    except ValueError as exc:
        raise SystemExit(f"wb share: {exc}")
    cfg = S.ShareConfig.load(root)
    print(f"✅ shared {grant['what']} with {grant['who']} ({grant['level']})")
    print(f"link    {link(root, rel)}")
    if listed:
        n = len([e for e in (S.canonical_email(x) for x in S.people(listed)) if e])
        print(f"people  {listed}  ({n} email{'s' if n != 1 else ''} now; one per line, saved edits apply at once)")
    print("sign-in " + ("a code is emailed from " + cfg.mail_from if cfg.acs else
                        "❗ mail is not set up (share.env): only owners can get a code yet"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
