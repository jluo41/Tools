#!/usr/bin/env python3
"""paper_ladder.py · make the paper ladder's folders (haipipe-paper/ref/paper-ladder.md): a Board, a version, a
Task, a Run, as the design theme's design_ladder.py makes its own (b16 Q05).

    python paper_ladder.py board   <paper/>Paper-<Slug>  [--title "<paper>"]             a new paper Board
    python paper_ladder.py version <board> --desk <desk> --date MMDD [--venue "<venue>"]  the first (or a fresh) version
    python paper_ladder.py next    <board> --from <version> --date MMDD                   the next version, from an earlier one
    python paper_ladder.py spaces  <board> <version>                                      give a version studio/ reports/ runs/
    python paper_ladder.py task    <version folder> tNN_<title>                           a Section, the Abstract or a letter
    python paper_ladder.py run     <Board or version folder> <type> <target>              a soft Run: runs/run-<type>-<target>/
    python paper_ladder.py rollback <board>                                               undo the newest version, next, spaces
                                                                                          or task (also version_paper.py's records)
    (add --dry-run to version, next, spaces, task or run: print what it would do; change nothing)

board writes only the face and needs no record: it makes a new folder. A Space folder (studio/, reports/, runs/,
venues/, related/, delivery/) comes with its first item, never ahead of it (haipipe-board); `spaces` makes a
version's three only when asked. version, next, spaces and task also edit board.md's ## Pages, so each keeps the old text of what it rewrites in <board>/.paper-version-N/ with its
record .paper-version-N.yaml, the same records the retired version_paper.py wrote, and rollback undoes the newest.
A Section's Runs are the Page workflow's (page.py open-run); `run` is for the Board's and a version's own Runs, written
by the shared writer (haipipe-run scripts/soft_run.py new): runs/run-<type>-<target>/ with its run.yaml card (skill,
agent and signs from the paper's run card whose pattern names it) and its ticket; `soft_run.py pass` adds its passes.

next: the next version starts from the one it follows (JL 261007: "j02 will make a copy of it and we will modify
    based on that"). Each Section's own writing is copied: its face, draft/ (not draft/records/ or draft/previous/)
    and studio/. Its results/, runs/, delivery/ and notebooks/ are generated or receipts and are not copied; the new
    version rebuilds them. The build's inputs (paper-build.toml, preamble.tex, build.py) are copied, its order
    pointed at the new face. The face says from: and tells:, and keeps the Narrative it follows.
A review batch into a version's reports/ is haipipe-paper-comments' (scripts/review_items.py add).

Placeholders only: a person or an agent fills them through the paper skills. The file helpers (move, links, yaml)
are carry_over/migrate_paper.py's and carry_over/topics_paper.py's until the carry-over retires. Nothing is
committed.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("topics_paper", HERE / "carry_over" / "topics_paper.py")
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)
M = T.M
_spec = importlib.util.spec_from_file_location("soft_run", HERE.parents[3] / "1_base" / "project" / "haipipe-run" /
                                               "scripts" / "soft_run.py")
SOFT = importlib.util.module_from_spec(_spec)        # the shared soft-Run writer (haipipe-run)
_spec.loader.exec_module(SOFT)

VERSION = re.compile(r"^j(\d{2})_v([^_]+)_(.+)$")
SECTION = re.compile(r"^t[0-2]\d_")
TASK = re.compile(r"^t(\d)(\d)_([a-z0-9][a-z0-9-]*)$")
RUN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
WRITTEN = ("draft", "studio")                 # a Section's own writing, besides its face
NOT_COPIED = {"records", "previous", "_archive", "__pycache__", ".DS_Store"}
DELIVERY_INPUTS = ("paper-build.toml", "preamble.tex", "build.py")
TEXT = {".md", ".toml", ".yaml", ".yml"}
# what each level's runs/README.md says; the cards are haipipe-paper-workflow/ref/run-cards.md
RUN_TYPES = {"Board": "update-board · add-venue · check-venue · add-resource · add-related · open-version · "
                      "generate-ideas · test-idea · revise-story · review-audience · ask-question · write-report · "
                      "review-report · update-status · build-bib",
             "version": "update-version · check-venue · draw-papermap · ask-question · write-report · "
                        "review-report · release-section · add-review · route-item · reply-item · write-letter · "
                        "check-letter · write-response · add-section · build-version · check-submission · "
                        "send-version"}
README = {"studio": "Idea Studio of this {level}: one topic per folder, sNN-<topic>/ (its drawings and a face: "
                    "decided · open · feeds).\n",
          "reports": "Audience Report of this {level}: one Question per folder, qNN_<topic>/, registered in the "
                     "face's ## Questions. A comments batch is a report with page-type: comments.\n",
          "runs": "Runs of this {level}: one soft Run per folder, run-<type>-<target>/ (no date in the name), "
                  "with its run.yaml card, its ticket run-<type>-<target>.md and passes/pNN-<MMDD>/, one per "
                  "execution.\n\nrun types: {types}\n"}
CARDS = HERE.parents[1] / "haipipe-paper-workflow" / "ref" / "run-cards.md"


def read(p):
    return M.read(p)


def readme(name, level):
    return README[name].format(level=level, types=RUN_TYPES.get(level, "the Page workflow's (page.py open-run)"))


def records(board):
    found = [f for f in board.glob(".paper-version-*.yaml") if re.fullmatch(r"\.paper-version-\d+\.yaml", f.name)]
    return sorted(found, key=lambda f: int(re.findall(r"\d+", f.name)[-1]))         # a rolled-back record is not one


class Run:
    """What one run does: moves, rewrites ({path: new text}, old text kept), and created files."""

    def __init__(self, board):
        self.board, self.moves, self.rewrite, self.create = board, [], {}, {}

    def text(self, rel):                       # the text as this run leaves it so far
        return self.rewrite.get(rel, self.create.get(rel, read(self.board / rel)))

    def set(self, rel, text):
        if rel in self.create:
            self.create[rel] = text
        elif text != read(self.board / rel):
            self.rewrite[rel] = text

    def show(self):
        for o, n in self.moves:
            print(f"  move    {o} -> {n}")
        for rel, text in self.rewrite.items():
            print(f"  rewrite {rel} ({len(read(self.board / rel).splitlines())} → {len(text.splitlines())} lines)")
        for rel in self.create:
            print(f"  create  {rel}")
        print(f"{len(self.moves)} moves · {len(self.rewrite)} rewritten · {len(self.create)} created")

    def apply(self, what):
        b = self.board
        k = 1 + max([int(re.match(r"\.paper-version-(\d+)", f.name).group(1)) for f in b.glob(".paper-version-*")] or [0])
        keep = b / f".paper-version-{k}"
        keep.mkdir()
        done = []
        for o, n in self.moves:
            done.append({"old": o, "new": n, "how": M.move(b, o, n)})
        for rel, text in self.rewrite.items():   # rel is the path after the moves
            dst = keep / (rel + ".orig")
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(read(b / rel), encoding="utf-8")
            (b / rel).write_text(text, encoding="utf-8")
        for rel, text in self.create.items():
            (b / rel).parent.mkdir(parents=True, exist_ok=True)
            if isinstance(text, Path):
                shutil.copy2(text, b / rel)
            else:
                (b / rel).write_text(text, encoding="utf-8")
        rec = {"run": date.today().isoformat(), "what": what, "tool": "haipipe-paper/scripts/paper_ladder.py",
               "moves": done, "rewritten": sorted(self.rewrite), "created": sorted(self.create), "kept": keep.name,
               "roll_back_first": "any record newer than this one"}
        (b / f".paper-version-{k}.yaml").write_text(M.dump(rec), encoding="utf-8")
        print(f"{what}: {len(done)} moves · {len(self.rewrite)} rewritten · {len(self.create)} created · "
              f"record .paper-version-{k}.yaml; nothing committed")


def header(text, key, value):
    """Set (or add, after the H1's header lines) a `key: value` line of a face."""
    if re.search(r"(?m)^%s:" % re.escape(key), text):
        return re.sub(r"(?m)^%s:.*$" % re.escape(key), f"{key}: {value}", text, count=1)
    head, sep, rest = text.partition("\n## ")
    return head.rstrip("\n") + f"\n{key}: {value}\n" + (("\n## " + rest) if sep else "")


def pages_add(text, version, lines, title=None):
    """Add lines under board.md's ### block for a version (made after the last version's block when missing)."""
    block = re.search(r"(?ms)^### +[^\n]*·\s*%s\b[^\n]*\n.*?(?=^### |^## |\Z)" % re.escape(version), text)
    if block:
        body = block.group(0).rstrip("\n") + "\n" + "".join(f"{x}\n" for x in lines) + "\n"
        return text[:block.start()] + body + text[block.end():]
    add = f"### J{version[1:3]} · {version}\n\n{title or ''}\n\n" + "".join(f"{x}\n" for x in lines) + "\n"
    pages = re.search(r"(?ms)^## Pages\s*\n.*?(?=^## |\Z)", text)
    if pages:
        return text[:pages.end()].rstrip("\n") + "\n\n" + add + text[pages.end():]
    return text.rstrip("\n") + "\n\n## Pages\n\n" + add


# ── board ─────────────────────────────────────────────────────────────────────────────────────────
def _write(path: Path, text: str, made: list) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    made.append(path)


def board(path: Path, title: str, dry: bool) -> list:
    if not re.match(r"^Paper-[A-Za-z0-9-]+$", path.name):
        sys.exit(f"stop: a paper Board folder is Paper-<Slug>: {path.name}")
    files = {                                   # the face only: a Space folder comes with its first item
        "board.md": f"# {title or '<paper>'}\n\nboard-kind: paper-board\ndialect: paper\npaper-root: .\n"
                    "story-current: none yet\nspine: <the question the paper answers, in one sentence>\n"
                    "close: <what makes this paper done: sent, answered, accepted>\n\n## Topic\n\n"
                    "<what the paper argues and for whom>\n\n## Pages\n\n## Questions\n\n```yaml\nquestions: []\n```\n",
    }
    made = []
    if dry:
        return [path / r for r in files if not (path / r).exists()]
    for rel, text in files.items():
        _write(path / rel, text, made)
    return made


# ── version · spaces ──────────────────────────────────────────────────────────────────────────────
def spaces(run, version):
    for d in README:
        if not (run.board / version / d).is_dir() and not any(r.startswith(f"{version}/{d}/") for r in run.create):
            run.create[f"{version}/{d}/README.md"] = readme(d, "version")


def version(run, desk, mmdd, venue):
    b = run.board
    if not re.fullmatch(r"\d{4}", mmdd) or not re.fullmatch(r"[a-z0-9-]+", desk):
        sys.exit("stop: --date is MMDD and --desk is lowercase (mansci, jama-im)")
    used = [int(VERSION.match(p.name).group(1)) for p in b.iterdir() if p.is_dir() and VERSION.match(p.name)]
    to = f"j{max(used, default=0) + 1:02d}_v{mmdd}_{desk}"
    run.create[f"{to}/{to}.md"] = (
        f"# {to} · version {max(used, default=0) + 1} of the paper\n\nsend: {to}\ndesk: {desk}\n"
        f"venue: {venue or '<venue>'}\nstate: drafting\ntells: studio/sNN-story-<telling>\nfrom: none (the first send)\n"
        f"goal: <the paper this send puts before {venue or '<venue>'}>\nclose: <sent, and every comment it drew answered>\n\n"
        "## Tasks\n\n## Narrative\n\nHow this version tells the story, in reading order: one row per Section (its job, the claims "
        "it carries, its release).\n\n<!-- haipipe:compile-order:start -->\n<!-- haipipe:compile-order:end -->\n\n"
        "## Questions\n\n```yaml\nquestions: []\n```\n")
    run.set("board.md", pages_add(run.text("board.md"), to, [], f"Version {to}: {venue or '<venue>'}."))
    return to


# ── next ──────────────────────────────────────────────────────────────────────────────────────────
def next_version(run, frm, mmdd):
    b = run.board
    m = VERSION.match(frm)
    if not m or not (b / frm).is_dir():
        sys.exit(f"stop: {frm} is not a version folder (jNN_v<…>_<desk>)")
    used = sorted(int(VERSION.match(p.name).group(1)) for p in b.iterdir() if p.is_dir() and VERSION.match(p.name))
    empty = next((p.name for p in b.iterdir() if p.is_dir() and VERSION.match(p.name) and p.name.endswith(f"_v{mmdd}_{m.group(3)}")
                  and not any(x for x in p.iterdir() if x.name not in (".DS_Store",))), None)
    to = empty or f"j{used[-1] + 1:02d}_v{mmdd}_{m.group(3)}"
    if (b / to).exists() and not empty:
        sys.exit(f"stop: {to} exists and is not empty")
    stems = []                                 # each Section's own writing
    for sec in sorted(p for p in (b / frm).iterdir() if p.is_dir() and SECTION.match(p.name)):
        stems.append(sec.name)
        files = [sec / (sec.name + ".md")] + [f for w in WRITTEN for f in sorted((sec / w).rglob("*")) if f.is_file()]
        for f in files:
            rel = f.relative_to(b / frm)
            if f.is_file() and not (NOT_COPIED & set(rel.parts)):
                run.create[f"{to}/{rel.as_posix()}"] = f
    # links in the copied text: a copied target is its copy; anything else stays the original (the earlier version's)
    copied = {f.relative_to(b).as_posix(): rel for rel, f in run.create.items() if isinstance(f, Path)}
    for rel, f in list(run.create.items()):
        if isinstance(f, Path) and f.suffix == ".md":
            t = read(f)
            nt = rebase(t, f, rel, b, copied)
            if nt != t:
                run.create[rel] = nt
    for name in DELIVERY_INPUTS:               # the build's inputs, its order pointed at the new face
        f = b / frm / "delivery" / name
        if f.is_file():
            run.create[f"{to}/delivery/{name}"] = f
    toml = b / frm / "delivery" / "paper-build.toml"
    if toml.is_file():
        t = re.sub(r'(?m)^(order\s*=\s*")[^"]*(")', lambda x: x.group(1) + f"../{to}.md" + x.group(2), read(toml))
        run.create[f"{to}/delivery/paper-build.toml"] = t.replace(frm + "/", to + "/")
    old = read(b / frm / (frm + ".md"))        # the face: from, tells, the Narrative it follows; its own Questions
    face = re.sub(r"(?m)\A# .*$", f"# {to} · the next version of the paper, from {frm}", old, count=1)
    for k, v in (("send", to), ("state", "drafting"), ("from", frm)):
        face = header(face, k, v)
    face = re.sub(r"(?ms)^## Questions.*?(?=^## |\Z)", "", face).rstrip("\n")
    face += "\n\n## Questions\n\n```yaml\nquestions: []\n```\n"
    run.create[f"{to}/{to}.md"] = face
    text = run.text("board.md")                # board.md: the version's Pages, after the one it follows
    block = re.search(r"(?ms)^### +[^\n]*·\s*%s\b[^\n]*\n.*?(?=^### |^## |\Z)" % re.escape(frm), text)
    add = f"### J{to[1:3]} · {to}\n\nFrom {frm}: each Section's own writing, to be revised.\n\n" + \
          "".join(f"{s}.md\n" for s in stems) + "\n"
    text = (text[:block.end()] + add + text[block.end():]) if block else text
    run.set("board.md", text)
    return to


def rebase(text, src, dst, board, copied):
    """A copied file's relative links: to a copied file, its copy; to anything else, the original."""
    root = board.resolve()

    def fix(m):
        pre, link, post = (m.group(1), m.group(2), m.group(3)) if m.group(1) else (m.group(4), m.group(5), "")
        if re.match(r"^([a-z][\w+.-]*:|#|/|<)", link) or "{" in link:
            return m.group(0)
        path, sep, frag = link.partition("#")
        t = (src.parent / path).resolve() if path else None
        if t is None or not t.exists():
            return m.group(0)
        rel = t.relative_to(root).as_posix() if t.is_relative_to(root) else None
        goal = board / copied[rel] if rel in copied else t
        new = Path(os.path.relpath(goal, (board / dst).parent)).as_posix()
        return m.group(0) if new == path else pre + new + sep + frag + post
    return M.LINK.sub(fix, text)


# ── task ──────────────────────────────────────────────────────────────────────────────────────────
def task(run, ver, stem):
    """A Page Task in a version: t00_abstract, t0N_ Main (t01-t19), t2N_ Appendix (A = t21), t3N_ a letter."""
    m = TASK.match(stem)
    if not m:
        sys.exit(f"stop: a Task is tNN_<title>, lowercase-kebab: {stem}")
    if not VERSION.match(ver) or not (run.board / ver).is_dir():
        sys.exit(f"stop: {ver} is not a version folder of this Board")
    if (run.board / ver / stem).exists():
        sys.exit(f"stop: {ver}/{stem} exists")
    band = int(m.group(1))
    kind = "letter" if band == 3 else "abstract" if stem == "t00_abstract" else m.group(3)
    part = {0: "Main", 1: "Main", 2: "Appendix", 3: "Letters"}[band]
    title = m.group(3).replace("-", " ").capitalize()
    run.create[f"{ver}/{stem}/{stem}.md"] = (
        f"# {stem} · {title}\n\ntask-kind: page\npage-type: section\nfolder-kind: section\nsection_kind: {kind}\n"
        f"structure-source: paper/haipipe-paper-section/ref/generic-template.md\nstate: ⬜ OPEN · plan to write\n"
        f"story-row: {ver} ## Narrative / {stem}\nreader-question: <what the reader asks here>\n"
        "entry-state: <what the reader holds coming in>\nexit-state: <what the reader holds going out>\n"
        "must-establish: <the claim this Section must land>\nmust-refuse: <what it must not overstate>\n"
        "transition-out: <what the next Section picks up>\n\n## Opening\n\n<the reader question, answered in one "
        "paragraph>\n\n## Content\n\n<the Section's prose, adopted from its Draft>\n\n## Aims\n\n- Target: <what "
        "the reader holds on exit> · Done when: <the check that says so> · Now: not started\n\n## Questions\n\n"
        "```yaml\nquestions: []\n```\n")
    run.set("board.md", pages_add(run.text("board.md"), ver, [f"{stem}.md"]))
    vface = f"{ver}/{Path(ver).name}.md"           # its line in the version face's ## Tasks (haipipe-job)
    if (run.board / vface).is_file() or vface in run.create:
        vt = run.text(vface)
        tasks = re.search(r"(?ms)^## Tasks[ \t]*\n(.*?)(?=^## |\Z)", vt)
        line = f"{stem} · {title}"
        if tasks is None:
            vt = vt.rstrip("\n") + f"\n\n## Tasks\n\n1. {line}\n"
        elif line not in tasks.group(1):
            n = len(re.findall(r"(?m)^\d+\. ", tasks.group(1))) + 1
            body = tasks.group(1).rstrip("\n")
            vt = vt[:tasks.start(1)] + (body + "\n" if body.strip() else "\n") + f"{n}. {line}\n\n" + vt[tasks.end(1):]
        run.set(vface, vt)
    return f"{ver}/{stem} ({part})"


# ── run ───────────────────────────────────────────────────────────────────────────────────────────
def card_of(name: str) -> dict:
    """The run card whose ticket pattern names this Run: {skill, agent, signs}; empty when none does."""
    card, out = None, {}
    for line in read(CARDS).splitlines() if CARDS.is_file() else ():
        if line.startswith("🔘 BUTTON"):
            parts = line.split(None, 2)[2].split(" · ")
            pat = parts[2].strip() if len(parts) > 2 else "-"
            card = None if out or pat == "-" or not re.match(pat, name) else {}
        elif card is not None and line.startswith(("🧩 SKILL", "🤖 AGENT", "✍️ SIGNS")):
            card[line.split()[1].lower()] = line.split(None, 2)[2].strip()
            if len(card) == 3:
                out, card = card, None
    return out


def soft_run(folder: Path, kind: str, target: str, dry: bool) -> Path:
    """A Board's or a version's soft Run through the shared writer, haipipe-run's soft_run.new: runs/run-<type>-<target>/
    with its run.yaml card (skill, agent and signs from the paper's run card whose pattern names it) and its ticket;
    its passes are added by `soft_run.py pass`."""
    if TASK.match(folder.name):
        sys.exit("stop: a Section's Runs are the Page workflow's: page.py open-run <page> --kind <kind>")
    name = f"run-{kind}-{target}"
    if dry:
        return folder / "runs" / name
    c = card_of(name)
    try:
        return SOFT.new(folder, kind, target, skill=c.get("skill", ""), agent=c.get("agent", ""),
                        signs=[c["signs"]] if c.get("signs") not in (None, "", "none") else None)
    except ValueError as e:
        sys.exit(f"stop: {e}")


# ── rollback ──────────────────────────────────────────────────────────────────────────────────────
def rollback(board):
    if not records(board):
        sys.exit("stop: no .paper-version-N.yaml at this Board")
    path = records(board)[-1]
    rec = M.load(read(path))
    keep = board / rec["kept"]
    for rel in rec.get("rewritten") or []:
        shutil.copy2(keep / (rel + ".orig"), board / rel)
    for rel in sorted(rec.get("created") or [], key=lambda r: -r.count("/")):
        f = board / rel
        if f.is_file():
            f.unlink()
        for d in f.parents:
            if d == board or not d.is_dir() or any(d.iterdir()):
                break
            d.rmdir()
    for m in reversed(rec.get("moves") or []):
        M.move(board, m["new"], m["old"])
    for m in rec.get("moves") or []:
        for d in (board / m["new"]).parents:
            if d == board or not d.is_dir() or any(d.iterdir()):
                break
            d.rmdir()
    shutil.rmtree(keep)
    path.rename(board / f"{path.stem}.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {rec['what']}: {len(rec.get('moves') or [])} moves, {len(rec.get('rewritten') or [])} rewrites, "
          f"{len(rec.get('created') or [])} created")


def find_board(folder: Path) -> Path:
    for d in [folder, *folder.parents]:
        if (d / "board.md").is_file():
            return d
    sys.exit(f"stop: no board.md at or above {folder}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    bo = sub.add_parser("board")
    bo.add_argument("path", type=Path)
    bo.add_argument("--title", default="")
    v = sub.add_parser("version")
    v.add_argument("board", type=Path)
    v.add_argument("--desk", required=True)
    v.add_argument("--date", required=True)
    v.add_argument("--venue", default="")
    n = sub.add_parser("next")
    n.add_argument("board", type=Path)
    n.add_argument("--from", dest="frm", required=True)
    n.add_argument("--date", required=True)
    s = sub.add_parser("spaces")
    s.add_argument("board", type=Path)
    s.add_argument("version")
    t = sub.add_parser("task")
    t.add_argument("version", type=Path)
    t.add_argument("stem")
    r = sub.add_parser("run")
    r.add_argument("folder", type=Path)
    r.add_argument("type")
    r.add_argument("target")
    rb = sub.add_parser("rollback")
    rb.add_argument("board", type=Path)
    for p in (bo, v, n, s, t, r):
        p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "board":
        made = board(a.path.resolve(), a.title, a.dry_run)
        for p in made:
            print(("would make " if a.dry_run else "made ") + str(p))
        return made
    if a.cmd == "run":
        p = soft_run(a.folder.resolve(), a.type, a.target, a.dry_run)
        print(("would make " if a.dry_run else "made ") + str(p))
        return p
    root = find_board(a.version.resolve()) if a.cmd == "task" else a.board.resolve()
    if not (root / "board.md").is_file():
        sys.exit(f"stop: {root.name} has no board.md")
    if a.cmd == "rollback":
        return rollback(root)
    run = Run(root)
    if a.cmd == "version":
        what = f"version {version(run, a.desk, a.date, a.venue)}"
    elif a.cmd == "next":
        what = f"next {next_version(run, a.frm, a.date)} from {a.frm}"
    elif a.cmd == "spaces":
        spaces(run, a.version)
        what = f"spaces {a.version}"
    else:
        what = f"task {task(run, a.version.resolve().relative_to(root).as_posix(), a.stem)}"
    if a.dry_run:
        print(what)
        run.show()
    else:
        run.apply(what)
    return run


if __name__ == "__main__":
    main()
