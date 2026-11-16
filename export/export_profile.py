#!/usr/bin/env python3
"""export_profile.py · write a profile's part of this repository, at one commit, into a target repository.

    python export/export_profile.py <target>              export HEAD into <target> (its export.yaml names the profile)
    python export/export_profile.py <target> --rev <rev>  export another commit
    python export/export_profile.py <target> --dry-run    list what would change; write nothing
    python export/export_profile.py <target> --check      list references to skills and paths left out; write nothing
    python export/export_profile.py <target> --commit     export, then commit in <target> naming the source commit

Only committed content travels: a file is read from the commit (`git archive`), never from the working tree, so
another session's unfinished edit stays here and `.export/source.yaml` names exactly what was exported. The target
keeps its own files (its export.yaml `keep:`, and always export.yaml itself): its README, AGENTS.md, marketplace and
remote say who it is for; this repository never does. Every other file is the profile's: written fresh on each
export, and removed when the profile no longer takes it (the previous export's list is `.export/files.txt`).
Standard library and PyYAML only. export/README.md says how a profile is written.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import io
import re
import subprocess
import sys
import tarfile
from pathlib import Path

import yaml

SOURCE = Path(__file__).resolve().parents[1]
PROFILES = SOURCE / "export" / "profiles"
MANIFEST = Path(".export") / "files.txt"
SKILL_NAME = re.compile(r"\b((?:haipipe|workbench|excalidraw)-[a-z0-9-]+)\b")
TEXT = {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".ps1", ".txt", ".js", ".mjs", ".css", ".html", ".toml"}


def _git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(SOURCE), *args], capture_output=True, check=True).stdout


def _under(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(prefix.rstrip("/") + "/")


def _excluded(path: str, globs: list[str]) -> bool:
    """fnmatch's * crosses /, so `**/x/**` matches x at any depth; the leading / lets it match at the top too."""
    return any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch("/" + path, g) for g in globs)


class Snapshot:
    """Every file of the profile's folders at one commit: {path: (bytes, mode)}, read in one `git archive`."""

    def __init__(self, rev: str, profile: dict):
        self.rev = _git("rev-parse", rev).decode().strip()
        roots = sorted({*(profile.get("include") or []), *(profile.get("agents_from") or []), *(profile.get("map") or {})})
        names = _git("ls-tree", "-r", "-z", "--name-only", self.rev, "--", *roots).decode().split("\0")
        self.files: dict[str, tuple[bytes, int]] = {}
        if not [n for n in names if n]:
            return
        tar = tarfile.open(fileobj=io.BytesIO(_git("archive", "--format=tar", self.rev, "--", *roots)))
        for m in tar.getmembers():
            if m.isfile():
                self.files[m.name] = (tar.extractfile(m).read(), m.mode)
            elif m.issym():                                    # a link travels as a link (mode -1: its target)
                self.files[m.name] = (m.linkname.encode(), -1)

    def text(self, path: str) -> str:
        data, mode = self.files.get(path, (b"", 0))
        return data.decode("utf-8", "replace") if mode != -1 and Path(path).suffix in TEXT else ""


def plan(snap: Snapshot, profile: dict) -> dict[str, str]:
    """{target path: source path} for every file the profile takes."""
    excl = profile.get("exclude") or []
    files = sorted(snap.files)
    take = {p: p for p in files if any(_under(p, i) for i in profile.get("include") or []) and not _excluded(p, excl)}
    named = "\n".join(snap.text(p) for p in take)
    for folder in profile.get("agents_from") or []:
        for p in files:
            if _under(p, folder) and p.endswith(".md") and re.search(rf"\b{re.escape(Path(p).stem)}\b", named):
                take[p] = p
    for src, dst in (profile.get("map") or {}).items():
        if src in snap.files:
            take[dst] = src
    return take


def check(snap: Snapshot, take: dict[str, str]) -> dict[str, list[str]]:
    """The skills, agents and repository paths an exported file names that the export leaves out."""
    every = set(_git("ls-tree", "-r", "-z", "--name-only", snap.rev).decode().split("\0")) - {""}
    have = set(take)
    skills = lambda fs: {p.split("/")[-2] for p in fs if p.endswith("/SKILL.md")}  # noqa: E731
    agents = lambda fs: {Path(p).stem for p in fs if "/agents/" in p and p.endswith(".md")}  # noqa: E731
    gone_names = (skills(every) - skills(have)) | (agents(every) - agents(have))
    paths = re.compile(r"\b((?:plugins/haipipe-toolkit/)?(?:skills|servers)/[A-Za-z0-9_./-]+|blueprints/[A-Za-z0-9_./-]+)")
    missing: dict[str, list[str]] = {}
    for dst, src in take.items():
        text = snap.text(src)
        for name in set(SKILL_NAME.findall(text)) & gone_names:
            missing.setdefault(f"skill {name}", []).append(dst)
        for ref in set(paths.findall(text)):
            ref = ref.rstrip(".,:;)/")
            full = ref if ref.startswith(("plugins/", "blueprints/")) else "plugins/haipipe-toolkit/" + ref
            if any(_under(f, full) for f in every) and not any(_under(f, full) for f in have):
                missing.setdefault(f"path {full}", []).append(dst)
    return missing


def export(target: Path, rev: str, dry: bool) -> tuple[dict[str, str], list[str], dict, Snapshot]:
    cfg = yaml.safe_load((target / "export.yaml").read_text(encoding="utf-8")) or {}
    profile = yaml.safe_load((PROFILES / f"{cfg['profile']}.yaml").read_text(encoding="utf-8"))
    snap = Snapshot(rev, profile)
    keep = set(cfg.get("keep") or []) | {"export.yaml"}
    take = {d: s for d, s in plan(snap, profile).items() if d not in keep}
    old = (target / MANIFEST).read_text(encoding="utf-8").split() if (target / MANIFEST).is_file() else []
    gone = [p for p in old if p not in take and p not in keep]
    if not dry:
        for p in gone:
            (target / p).unlink(missing_ok=True)
        for dst, src in take.items():
            data, mode = snap.files[src]
            out = target / dst
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.is_symlink() or out.exists():
                out.unlink()
            if mode == -1:
                out.symlink_to(data.decode())
            else:
                out.write_bytes(data)
                out.chmod(0o755 if mode & 0o111 else 0o644)
        (target / MANIFEST).parent.mkdir(exist_ok=True)
        (target / MANIFEST).write_text("\n".join(sorted(take)) + "\n", encoding="utf-8")
        (target / ".export" / "source.yaml").write_text(yaml.safe_dump(
            {"profile": cfg["profile"], "source_commit": snap.rev,
             "exported": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}, sort_keys=False), encoding="utf-8")
    return take, gone, cfg, snap


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", type=Path)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args(argv)
    target = a.target.resolve()
    if not (target / "export.yaml").is_file():
        sys.exit(f"{target}/export.yaml: name the profile there first (export/README.md)")
    if target == SOURCE or SOURCE in target.parents:
        sys.exit("the target is a separate repository, outside this one")
    if a.check:
        cfg = yaml.safe_load((target / "export.yaml").read_text(encoding="utf-8"))
        profile = yaml.safe_load((PROFILES / f"{cfg['profile']}.yaml").read_text(encoding="utf-8"))
        snap = Snapshot(a.rev, profile)
        take = plan(snap, profile)
        missing = check(snap, take)
        for what, where in sorted(missing.items()):
            print(f"{what:<70} named in {len(where)} file(s), e.g. {where[0]}")
        print(f"{len(take)} files at {snap.rev[:9]}; {len(missing)} references left out")
        return 0
    files, gone, cfg, snap = export(target, a.rev, a.dry_run)
    print(f"{'would write' if a.dry_run else 'wrote'} {len(files)} files · "
          f"{'would remove' if a.dry_run else 'removed'} {len(gone)} · profile {cfg['profile']} at {snap.rev[:9]}")
    changed = _git("status", "--porcelain", "--", *sorted(set(files.values()))).decode().splitlines() if files else []
    if changed:
        print(f"note: {len(changed)} file(s) of the profile differ from the working tree; commit them to export them")
    if a.commit and not a.dry_run:
        subprocess.run(["git", "-C", str(target), "add", "-A"], check=True)
        msg = f"Export {cfg['profile']} from Tools {snap.rev[:9]}"
        subprocess.run(["git", "-C", str(target), "commit", "-q", "-m", msg], check=False)
        print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
