#!/usr/bin/env python3
"""import_fragments.py · carry each Section's words from its old LaTeX fragment into its Draft (haipipe-paper).

    python import_fragments.py <board> --dry-run     print what each Section gets; change nothing
    python import_fragments.py <board> --apply       write the Drafts and the face lines; keep old text for rollback
    python import_fragments.py <board> --verify      does each Page's LaTeX lane print its fragment again?
    python import_fragments.py <board> --retire      after --verify passes: the old Page-local delivery/ leaves
    python import_fragments.py <board> --rollback    undo the newest run (retire first, then apply)

A Board carved from a manuscript before the draft steps keeps each Section's words only in its Page-local
`delivery/latex/<stem>.tex`, a file with no `% GENERATED from` mark. The Page export refuses to build the
Block's Delivery while that file stands ("move its words into the Page and adopt"). This script moves the
words line for line, so `page.py adopt` and `page.py export` can take over:

    no Draft yet           -> draft/<stem>-draft-v0.1.md: a division per \\section or \\subsection, a paragraph
                              per LaTeX paragraph (a blank line ends it), a Bullet per source line; § 3 holds
                              the line as written (content-format: latex), § 1 a short point, § 2 is empty
    a planned Draft whose  -> its § 3 filled: the n-th sentence goes to the n-th Bullet, and a line that is no
    § 3 is empty              sentence (a comment, \\begin, \\noindent) rides with the next one as its first
                              line; refused unless the sentences and the Bullets agree in number
    the face               -> task-type: draft · content-format: latex; the Opening's paragraph that called
                              the fragment the only copy of the words now names the Draft

Then, per Section: `page.py adopt <page>` (Content from § 3); `--verify` (the LaTeX lane's text, by md2tex's own
reader, equals the fragment line for line, leading spaces aside); `--retire` moves each verified Page-local
delivery/ into this run's keep folder, so `page.py export <page>` writes the Block's Delivery. Tracked files
leave the index with the move; nothing is committed. Generated and history files are never edited.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
MD2TEX = next(p for p in HERE.parents if p.name == "skills").parent / \
    "servers/workbench/workbench-task-draft/exporters/md2tex.py"
RECORD = ".paper-fragments.yaml"
KEEP = ".paper-fragments"
GENERATED = "% GENERATED from"
SECTIONING = re.compile(r"^\\(section|subsection)\*?\{(.*)\}")
CARRIER = re.compile(r"^(%|\\(begin|end)\{|\\noindent\b|\\label\{|\\centering\b|\\small\b)")
FACE_HEAD_KEYS = ("task-type", "content-format")
ONLY_COPY = re.compile(r"(?m)^This page owns that unit's words\. Its body is .*$")


# ── reading ───────────────────────────────────────────────────────────────────────────────────────
def sections(board: Path):
    """[(folder, stem)] for each Section Page in a version: a face with page-type: section."""
    out = []
    for face in sorted(board.glob("j[0-9][0-9]_*/*/*.md")):
        if face.stem == face.parent.name and re.search(r"(?m)^page-type:\s*section\b", face.read_text(encoding="utf-8")):
            out.append((face.parent, face.stem))
    return out


def old_fragment(folder: Path, stem: str) -> Path | None:
    f = folder / "delivery" / "latex" / f"{stem}.tex"
    if f.is_file() and not f.read_text(encoding="utf-8").startswith(GENERATED):
        return f
    return None


def paragraphs(text: str) -> list:
    """The fragment's LaTeX paragraphs: runs of non-blank lines, each line right-stripped."""
    out, cur = [], []
    for line in text.splitlines():
        if line.strip():
            cur.append(line.rstrip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def words(line: str, n: int = 8) -> str:
    """A few plain words of a LaTeX line, for a point or a title."""
    s = re.sub(r"(?<!\\)%.*$", "", line)
    s = re.sub(r"\\(?:begin|end)\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z@]+\*?", " ", s)
    s = re.sub(r"[{}$\\&_^~]", " ", s)
    w = s.split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")


def point(line: str) -> str:
    s = line.strip()
    if s.startswith("%"):
        return "[Source] " + (s[:70] + " …" if len(s) > 70 else s)
    m = SECTIONING.match(s)
    if m:
        return "[Heading] " + m.group(2)
    if s.startswith("\\") and not words(s, 3):
        return "[LaTeX] " + s[:60]
    return "[Line] " + (words(s) or s[:60])


def face_value(text: str, key: str) -> str:
    m = re.search(r"(?m)^%s:\s*(.*)$" % re.escape(key), text.split("\n## ", 1)[0])
    return m.group(1).strip() if m else ""


# ── a Draft from a fragment ───────────────────────────────────────────────────────────────────────
def new_draft(stem: str, face: str, fragment: str, rel: str) -> str:
    title = (re.search(r"(?m)^# +(.+)$", face) or [None, stem])[1].strip()
    divisions, plan, sn = [], [], 0
    for para in paragraphs(fragment):
        head = SECTIONING.match(para[0].strip())
        if head and (head.group(1) == "subsection" or not divisions):
            divisions.append([head.group(2), 0])
        elif not divisions:
            divisions.append([title, 0])
        div = divisions[-1]
        div[1] += 1
        first = sn + 1
        sn += len(para)
        name = ("Heading: " + head.group(2)) if head and len(para) == 1 else \
            (words(next((l for l in para if not CARRIER.match(l.strip()) and not SECTIONING.match(l.strip())), para[0]), 7)
             or "LaTeX block")
        plan.append((len(divisions), name.replace("·", "-"), para, first, sn))
    lines = sum(len(p[2]) for p in plan)
    out = [f"# {stem} · draft v0.1",
           "draft-version: v0.1",
           "supersedes: none",
           f"date: {date.today().strftime('%y%m%d')}",
           "approved: ⬜",
           f"status: v0.1 carried over line for line from {rel} (no Draft existed); one Bullet per source line; "
           "the structure is not planned yet",
           f"story-row: {face_value(face, 'story-row')}",
           f"structure-source: {face_value(face, 'structure-source') or 'none'}",
           f"arc: not planned yet; the reader question is: {face_value(face, 'reader-question')}",
           "",
           "## 1 · Structure · Bullet Point Table",
           "",
           "### Structure Overview",
           ""]
    for c, (dtitle, count) in enumerate(divisions, 1):
        out.append(f"- C{c} · {dtitle.replace('·', '-')} · {count} paragraph(s), carried over")
        for pn, (cn, name, para, a, b) in enumerate(plan, 1):
            if cn == c:
                out += [f"- C{c}.P{pn} · {name}", f"  → S{a} to S{b} · {len(para)} source line(s), as written"]
    out.append("")
    heads = [f"### C{cn}.P{pn} · {name} · S{a} to S{b}" for pn, (cn, name, para, a, b) in enumerate(plan, 1)]
    for h, (cn, name, para, a, b) in zip(heads, plan):
        out.append(h)
        out += [f"- B{k} · S{a + k - 1} · {point(l)}" for k, l in enumerate(para, 1)]
        out.append("")
    out += ["## 2 · Scratch · What to write here", ""]
    for h in heads:
        out += [h, ""]
    out += ["## 3 · Draft · Reading and Revise", "",
            f"Carried over from `{rel}`, {lines} lines: each Bullet holds one source line, LaTeX as written "
            "(content-format: latex).", ""]
    for h, (cn, name, para, a, b) in zip(heads, plan):
        out.append(h)
        out += [f"- B{k} · S{a + k - 1} · {l.strip()}" for k, l in enumerate(para, 1)]
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def fill_draft(plan_text: str, fragment: str) -> tuple[str | None, str]:
    """A planned Draft (its § 1 Bullets, an empty § 3) with its § 3 filled from the fragment, or (None, why)."""
    s3 = re.search(r"(?m)^## 3 · Draft\b.*$", plan_text)
    if not s3:
        return None, "the Draft has no `## 3 · Draft` section"
    body3 = re.split(r"(?m)^## ", plan_text[s3.end():], maxsplit=1)[0]
    if re.search(r"(?m)^- (?:\[[ xX]\]\s*)?B\d+\s*·", body3):
        return None, "its § 3 already holds sentences"
    s1 = re.search(r"(?m)^## 1 · Structure\b.*$", plan_text)
    body1 = re.split(r"(?m)^## ", plan_text[s1.end():], maxsplit=1)[0] if s1 else ""
    heads = re.findall(r"(?m)^(### C\d+\.P\d+\b.*)$", body1)
    bullets = []                                   # [(paragraph heading, B number)]
    current = None
    for line in body1.splitlines():
        if re.match(r"^### C\d+\.P\d+\b", line):
            current = line
        m = re.match(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·", line)
        if m and current:
            bullets.append((current, int(m.group(1))))
    units, carry = [], []
    for line in fragment.splitlines():
        s = line.strip()
        if not s:
            continue
        if CARRIER.match(s):
            carry.append(s)
        else:
            units.append(carry + [s])
            carry = []
    if carry and units:
        units[-1] += carry
    if len(units) != len(bullets):
        return None, f"{len(units)} sentence(s) in the fragment, {len(bullets)} Bullet(s) in the plan"
    out3 = [""]
    sn = 0
    for h in heads:
        out3.append(h)
        for (bh, k), unit in zip(bullets, units):
            if bh == h:
                sn += 1
                out3.append(f"- B{k} · S{sn} · {unit[0]}")
                out3 += ["  " + x for x in unit[1:]]
        out3.append("")
    rest = re.split(r"(?m)^(?=## )", plan_text[s3.end():], maxsplit=1)
    tail = rest[1] if len(rest) > 1 else ""
    return plan_text[:s3.end()] + "\n" + "\n".join(out3) + "\n" + tail, ""


def new_face(face: str, stem: str, draft_name: str) -> str:
    head, sep, body = face.partition("\n## ")
    for key, value in (("task-type", "draft"), ("content-format", "latex")):
        if not re.search(r"(?m)^%s:" % key, head):
            m = re.search(r"(?m)^page-type:.*$", head)
            head = head[:m.end()] + f"\n{key}: {value}" + head[m.end():] if m else head + f"\n{key}: {value}"
    body = ONLY_COPY.sub(
        f"Its words are the Draft's `## 3 · Draft` (`draft/{draft_name}`), carried over line for line from the "
        "fragment carved from the manuscript at commit `cd0af57`; `## Content` is adopted from the Draft and the "
        "LaTeX lane prints it again.", body, count=1)
    return head + sep + body


# ── the plan, and the modes ───────────────────────────────────────────────────────────────────────
def plan(board: Path) -> list:
    out = []
    for folder, stem in sections(board):
        frag = old_fragment(folder, stem)
        rel = f"delivery/latex/{stem}.tex"
        item = {"page": folder.relative_to(board).as_posix(), "stem": stem}
        if frag is None:
            item["skip"] = "no unmarked Page-local fragment"
            out.append(item)
            continue
        fragment = frag.read_text(encoding="utf-8")
        face = (folder / f"{stem}.md").read_text(encoding="utf-8")
        drafts = sorted((folder / "draft").glob(f"{stem}-draft-v*.md"))
        if drafts:
            text, why = fill_draft(drafts[-1].read_text(encoding="utf-8"), fragment)
            if text is None:
                item["skip"] = f"{drafts[-1].name}: {why}"
                out.append(item)
                continue
            item.update(draft=drafts[-1].name, how="filled § 3", text=text)
        else:
            item.update(draft=f"{stem}-draft-v0.1.md", how="new", text=new_draft(stem, face, fragment, rel))
        item["face"] = new_face(face, stem, item["draft"])
        out.append(item)
    return out


def dry_run(board: Path) -> None:
    for item in plan(board):
        if "skip" in item:
            print(f"  ·  {item['stem']:58} skip: {item['skip']}")
            continue
        bullets = len(re.findall(r"(?m)^- B\d+ · S\d+ · ", item["text"].split("## 3 · Draft", 1)[1]))
        print(f"  ✎  {item['stem']:58} {item['how']:12} draft/{item['draft']}  ({bullets} Bullets in § 3)")
    print("\nnothing changed (dry run)")


def runs(board: Path) -> list:
    return sorted(board.glob(f"{KEEP}-*.yaml"), key=lambda f: int(re.findall(r"\d+", f.name)[-1]))


def apply(board: Path) -> None:
    items = [i for i in plan(board) if "skip" not in i]
    k = 1 + max([int(re.findall(r"\d+", f.name)[-1]) for f in board.glob(f"{KEEP}-*")] or [0])
    keep = board / f"{KEEP}-{k}"
    rec = {"run": date.today().isoformat(), "tool": "haipipe-paper/scripts/carry_over/import_fragments.py",
           "created": [], "rewritten": [], "retired": [], "kept": keep.name}
    for item in items:
        folder = board / item["page"]
        draft = folder / "draft" / item["draft"]
        face = folder / f"{item['stem']}.md"
        for f in ([draft] if draft.is_file() else []) + [face]:
            rel = f.relative_to(board).as_posix()
            (keep / (rel + ".orig")).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, keep / (rel + ".orig"))
            rec["rewritten"].append(rel)
        if not draft.is_file():
            rec["created"].append(draft.relative_to(board).as_posix())
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_text(item["text"], encoding="utf-8")
        face.write_text(item["face"], encoding="utf-8")
    (board / f"{KEEP}-{k}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"{len(rec['created'])} Draft(s) written · {len(items) - len(rec['created'])} filled · record {KEEP}-{k}.yaml; "
          "next: page.py adopt on each, then --verify")


def _md2tex():
    spec = importlib.util.spec_from_file_location("md2tex", MD2TEX)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(text: str) -> list:
    """Paragraphs as compared: each line stripped of its leading spaces (a Bullet cannot keep them)."""
    return ["\n".join(line.strip() for line in para) for para in paragraphs(text)]


def verify(board: Path, quiet: bool = False) -> list:
    """[(folder, stem)] whose Page prints its old fragment again; prints the first difference of the others."""
    md2tex, good = _md2tex(), []
    for folder, stem in sections(board):
        frag = old_fragment(folder, stem)
        if frag is None:
            continue
        built = md2tex.build_latex_section(str(folder / f"{stem}.md"))
        want, got = norm(frag.read_text(encoding="utf-8")), norm(built)
        if want == got:
            good.append((folder, stem))
            quiet or print(f"  ✅ {stem:58} {sum(len(p.splitlines()) for p in want)} lines, {len(want)} paragraphs")
            continue
        at = next((i for i, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
        quiet or print(f"  ❌ {stem:58} paragraph {at + 1}: fragment {len(want)}, Page {len(got)} paragraphs\n"
                       f"     fragment: {(want[at] if at < len(want) else '')[:110]!r}\n"
                       f"     Page:     {(got[at] if at < len(got) else '')[:110]!r}")
    return good


def retire(board: Path) -> None:
    if not runs(board):
        sys.exit("stop: run --apply first")
    path = runs(board)[-1]
    rec = yaml.safe_load(path.read_text(encoding="utf-8"))
    keep = board / rec["kept"]
    for folder, stem in verify(board, quiet=True):
        local = folder / "delivery"
        rel = local.relative_to(board).as_posix()
        dst = keep / "retired" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        tracked = subprocess.run(["git", "-C", str(board), "ls-files", rel], capture_output=True, text=True).stdout.split()
        shutil.move(str(local), str(dst))
        if tracked:
            subprocess.run(["git", "-C", str(board), "rm", "-r", "-q", "--cached", rel], check=True)
        rec["retired"].append(rel)
        print(f"  ↪ {rel} → {rec['kept']}/retired/")
    path.write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"{len(rec['retired'])} Page-local delivery/ folder(s) retired; next: page.py export on each")


def rollback(board: Path) -> None:
    if not runs(board):
        sys.exit("stop: no import record at this Board")
    path = runs(board)[-1]
    rec = yaml.safe_load(path.read_text(encoding="utf-8"))
    keep = board / rec["kept"]
    for rel in reversed(rec.get("retired") or []):
        if not (board / rel).exists():
            shutil.move(str(keep / "retired" / rel), str(board / rel))
            subprocess.run(["git", "-C", str(board), "add", rel], check=False)
    for rel in rec.get("created") or []:
        (board / rel).unlink(missing_ok=True)
    for rel in rec.get("rewritten") or []:
        if (keep / (rel + ".orig")).is_file():
            shutil.copy2(keep / (rel + ".orig"), board / rel)
    shutil.rmtree(keep, ignore_errors=True)
    path.rename(board / f"{path.stem}.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {len(rec.get('retired') or [])} retired, {len(rec.get('created') or [])} created, "
          f"{len(rec.get('rewritten') or [])} rewritten (each face as it was before the import, Content included)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board", type=Path)
    mode = ap.add_mutually_exclusive_group(required=True)
    for m in ("dry-run", "apply", "verify", "retire", "rollback"):
        mode.add_argument("--" + m, action="store_true")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        sys.exit(f"stop: {board.name} has no board.md")
    if a.verify:
        good = verify(board)
        print(f"\n{len(good)} Page(s) print their fragment again")
    else:
        (rollback if a.rollback else retire if a.retire else apply if a.apply else dry_run)(board)


if __name__ == "__main__":
    main()
