#!/usr/bin/env python3
"""Pull one file out of the task folder into a probe card's proof/.

    python3 pull-proof.py <card-dir> <source-file> --why "<one line>" [--kind table]

The copy and its manifest block are written by the SAME run, so `sha256`,
`rows` and `bytes` describe the bytes that actually landed. Hand-copying was
how it was done until 260817, and a hand-typed hash proves nothing.

Refuses, rather than warns:
  · a file over ~200 rows or ~50 KB          (§🧾 rule ②)
  · a name already in proof/ with different bytes, unless --replace
  · --aggregate false                        (🚨 PHI, §🧾 rule ③)
"""
import argparse
import hashlib
import pathlib
import re
import shutil
import sys

MAX_ROWS, MAX_BYTES = 200, 50 * 1024
KINDS = {"table": ".csv", "numbers": ".json", "excerpt": ".txt"}


def guess_kind(path):
    for k, suf in KINDS.items():
        if path.suffix == suf:
            return k
    return None


def block(name, kind, source, run, rows, size, digest, why):
    return (
        "  - name: %s\n"
        "    kind: %s\n"
        "    source: %s\n"
        "    run: %s\n"
        "    pulled: %s\n"
        "    rows: %d\n"
        "    bytes: %d\n"
        "    sha256: %s\n"
        "    why: %s\n"
        "    aggregate: true\n"
        % (name, kind, source, run, TODAY, rows, size, digest, why)
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card", help="the PP<NN>-<slug>/ folder")
    ap.add_argument("source", help="the file inside the task folder")
    ap.add_argument("--why", required=True, help="why this card needs this file")
    ap.add_argument("--kind", choices=sorted(KINDS), default=None)
    ap.add_argument("--run", default=None, help="run directory; inferred if omitted")
    ap.add_argument("--date", required=True, help="today, YYYY-MM-DD (no clock here)")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--repo-root", default=".")
    a = ap.parse_args()

    global TODAY
    TODAY = a.date

    src = pathlib.Path(a.source)
    if not src.is_file():
        sys.exit("no such file: %s" % src)
    raw = src.read_bytes()
    rows = raw.count(b"\n")
    if rows > MAX_ROWS or len(raw) > MAX_BYTES:
        sys.exit("🚨 %d rows / %d bytes exceeds %d / %d — leave it in the task "
                 "folder and cite it by source: alone (§🧾 rule ②)"
                 % (rows, len(raw), MAX_ROWS, MAX_BYTES))

    kind = a.kind or guess_kind(src)
    if not kind:
        sys.exit("cannot tell the kind of %s; pass --kind table|numbers|excerpt"
                 % src.suffix)

    card = pathlib.Path(a.card)
    proof = card / "proof"
    proof.mkdir(parents=True, exist_ok=True)
    dst = proof / src.name
    if dst.is_file() and dst.read_bytes() != raw and not a.replace:
        sys.exit("proof/%s exists with different bytes; --replace to move the "
                 "old proof/ into versions/ and pull again" % src.name)

    if a.replace and dst.is_file():
        keep = proof / "versions" / TODAY.replace("-", "")[2:]
        keep.mkdir(parents=True, exist_ok=True)
        for old in proof.iterdir():
            if old.is_file():
                shutil.copy2(old, keep / old.name)

    shutil.copy2(src, dst)
    digest = hashlib.sha256(raw).hexdigest()

    root = pathlib.Path(a.repo_root).resolve()
    try:
        rel = src.resolve().relative_to(root)
    except ValueError:
        rel = src.resolve()
    run = a.run or next((p for p in src.parts if p.startswith("run_")), "?")

    man = proof / "manifest.yaml"
    text = man.read_text() if man.is_file() else "card: %s\n" % card.name
    text = re.sub(r"^(pending|why_empty):.*(\n[ \t]+.*)*\n?", "", text, flags=re.M)
    entry = block(src.name, kind, rel, run, rows, len(raw), digest, a.why)
    if re.search(r"^files:\s*\[\s*\]\s*$", text, re.M):
        text = re.sub(r"^files:\s*\[\s*\]\s*$", "files:\n" + entry.rstrip(),
                      text, flags=re.M)
    elif re.search(r"^files:\s*$", text, re.M):
        text = text.rstrip() + "\n" + entry
    else:
        text = text.rstrip() + "\nfiles:\n" + entry
    man.write_text(text if text.endswith("\n") else text + "\n")

    print("pulled  %s  →  %s" % (rel, dst))
    print("        %s · %d rows · %d bytes" % (kind, rows, len(raw)))
    print("        sha256 %s" % digest)


if __name__ == "__main__":
    main()
