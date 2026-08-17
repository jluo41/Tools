#!/usr/bin/env python3
"""Check one page's probe/ folder against haipipe-plugin-probe.

    python3 check-probe.py <page-dir> [--task-folder <path>]

Every rule this file enforces is written in SKILL.md; nothing is invented here.
Exit 0 when every card conforms, 1 otherwise. No writes, ever.
"""
import argparse
import hashlib
import pathlib
import re
import sys

STATES = {
    "planned", "commissioned", "answered", "read",
    "answered-local", "deferred", "failed", "concern",
}
ANSWERED = {"answered", "answered-local"}
QUESTION_WORDS = {"which", "what", "why", "how", "whether", "is", "does"}
PLAIN = {"n", "coef", "sample", "script", "run", "table", "log", "gap",
         "commit", "spec", "ols", "did", "iv"}
KINDS = {"table", "numbers", "excerpt"}
# Any id a consumer uses to address ITSELF. The bank has never seen a board,
# so a page id in a dispatched question is both a leak and an unanswerable
# reference. `Q[A-Z]\d` covers QA2, QB3, QC1; `C\d.P\d.B\d` the outline address.
STAKE = re.compile(
    r"\b(our|this paper|we claim|the paper|PP\d\d|CD\d\d|Aim ?\d|A\d+\.\d+"
    r"|Q[A-Z]\d+|C\d+\.P\d+\.B\d+)\b", re.I)
MAX_ROWS, MAX_BYTES = 200, 50 * 1024


def head_fields(text):
    """`key: value` lines above the first blank-line-terminated block."""
    out = {}
    for ln in text.splitlines():
        m = re.match(r"^([a-z_-]+):\s*(.*)$", ln)
        if m:
            out.setdefault(m.group(1), m.group(2).strip())
        elif ln.startswith("## "):
            break
    return out


def yaml_lite(text):
    """Enough of manifest.yaml to check it: the `files:` blocks and the two
    empty-forms. Deliberately not a yaml parser — this must run with no deps."""
    files, cur = [], None
    in_files = False
    for ln in text.splitlines():
        if re.match(r"^files:\s*\[\s*\]\s*$", ln):
            in_files = False
            continue
        if re.match(r"^files:\s*$", ln):
            in_files = True
            continue
        if in_files and re.match(r"^\s*-\s+\w+:", ln):
            cur = {}
            files.append(cur)
        if in_files and cur is not None:
            m = re.match(r"^\s*-?\s*([a-z_0-9]+):\s*(.*)$", ln)
            if m and m.group(1) != "files":
                cur[m.group(1)] = m.group(2).strip()
        if re.match(r"^(why_empty|pending|card):", ln):
            in_files = False
    top = dict(re.findall(r"^(why_empty|pending|card):\s*(.*)$", text, re.M))
    return files, top


def check_name(slug, task_folder, bad):
    words = slug.split("-")[1:] if re.match(r"^PP\d+-", slug) else slug.split("-")
    for w in words:
        if w.lower() in QUESTION_WORDS:
            bad(f"name: `{w}` is a question word; a folder NAMES, a card ASKS")
        if w.lower() in PLAIN or w.isdigit() or re.match(r"^spec\d", w.lower()):
            continue
        if task_folder and task_folder.is_dir():
            hit = any(w.lower() in p.name.lower() or
                      (p.is_file() and p.stat().st_size < 2_000_000 and
                       w.lower() in p.read_text(errors="ignore").lower())
                      for p in task_folder.rglob("*") if p.is_file())
            if not hit:
                bad(f"name: `{w}` greps to zero in the task folder")


def check_card(d, task_folder):
    errs = []
    def bad(m):
        errs.append(m)

    card = d / "card.md"
    if not card.is_file():
        return [f"{d.name}: no card.md"]
    f = head_fields(card.read_text())
    state = f.get("state", "")
    if state not in STATES:
        bad(f"state: `{state}` is not one of haipipe-probe's states")
    for k in ("question", "read"):
        if k not in f:
            bad(f"card.md has no `{k}:` line")
    check_name(d.name, task_folder, bad)

    for rel in ("consumer/q-consumer.md", "executor/q-executor.md"):
        if not (d / rel).is_file():
            bad(f"missing {rel}")

    for p in (d / "executor").rglob("*.md"):
        if p.name == "a-executor.md":
            continue
        for i, ln in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = STAKE.search(ln)
            if m:
                bad(f"stake wall: executor/{p.name}:{i} carries `{m.group(0)}`")

    a = d / "executor" / "a-executor.md"
    if state in ANSWERED and not (a.is_file() and a.read_text().strip()):
        bad(f"state `{state}` with no a-executor.md")

    man = d / "proof" / "manifest.yaml"
    if not man.is_file():
        bad("proof/manifest.yaml is missing (it exists from the moment the "
            "card is raised)")
        return [f"{d.name}: {e}" for e in errs]

    files, top = yaml_lite(man.read_text())
    if not files:
        if state in ANSWERED and not top.get("why_empty") and not top.get("pending"):
            bad("answered with an empty proof/ and neither why_empty nor pending")
    for blk in files:
        nm = blk.get("name", "")
        for key in ("name", "kind", "source", "run", "pulled", "sha256",
                    "why", "aggregate"):
            if key not in blk:
                bad(f"proof/{nm or '?'}: manifest block has no `{key}:`")
        if blk.get("kind") not in KINDS:
            bad(f"proof/{nm}: kind `{blk.get('kind')}` is not table|numbers|excerpt")
        if blk.get("aggregate") != "true":
            bad(f"proof/{nm}: 🚨 aggregate is not true; it may not be committed")
        fp = d / "proof" / nm
        if not fp.is_file():
            bad(f"proof/{nm}: named in the manifest, not on disk")
            continue
        raw = fp.read_bytes()
        rows = raw.count(b"\n")
        if rows > MAX_ROWS or len(raw) > MAX_BYTES:
            bad(f"proof/{nm}: {rows} rows / {len(raw)} bytes exceeds 200 / 50 KB")
        if blk.get("rows") and blk["rows"].isdigit() and int(blk["rows"]) != rows:
            bad(f"proof/{nm}: manifest says rows {blk['rows']}, file has {rows}")
        got = hashlib.sha256(raw).hexdigest()
        if blk.get("sha256") not in ("", "<of the file as pulled>", got):
            bad(f"proof/{nm}: sha256 does not match the file as it sits here")
    return [f"{d.name}: {e}" for e in errs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--task-folder", default=None)
    a = ap.parse_args()
    probe = pathlib.Path(a.page) / "probe"
    tf = pathlib.Path(a.task_folder) if a.task_folder else None
    if not probe.is_dir():
        print(f"no probe/ under {a.page}")
        return 0
    cards = sorted(d for d in probe.iterdir() if d.is_dir())
    errs = [e for d in cards for e in check_card(d, tf)]
    for e in errs:
        print("🚨", e)
    counts = {s: 0 for s in STATES}
    for d in cards:
        st = head_fields((d / "card.md").read_text()).get("state", "")
        counts[st] = counts.get(st, 0) + 1
    read = sum(1 for d in cards
               if head_fields((d / "card.md").read_text())
               .get("read", "").startswith("✅"))
    print(f"{len(cards)} cards · " +
          " · ".join(f"{k} {v}" for k, v in counts.items() if v) +
          f" · {read} / {len(cards)} read")
    print("✅ every card conforms" if not errs else f"{len(errs)} defects")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
