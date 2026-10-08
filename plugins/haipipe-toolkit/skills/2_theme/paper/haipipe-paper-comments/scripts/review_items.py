#!/usr/bin/env python3
"""review_items.py · a paper version's comments reports and their Review Items (haipipe-paper-comments, b16 Q05).

    python review_items.py <board> add <batch folder> --to <version>    a review batch into the version's reports/
    python review_items.py <board> route <report> <item> --to "<stem> ¶N · C2" [--work <run> | --decline]
    python review_items.py <board> reply <report> <item> --reply P3 [--state answered|applied|declined|deferred]
    python review_items.py <board> rollback                            undo the newest add, route or reply
    (add --dry-run to add, route or reply: print what it would do; change nothing)

add: a review batch is a report of type comments (JL 261007), in the version that answers it:
    <version>/reports/qNN_<kind>-<MMDD>/, its face page-type: comments, a row in that version's ## Questions
    (group: comments). Its folder keeps feedback/, meeting/ and sent/ unchanged. Every source text that names it
    or links to it follows. (Was version_paper.py comments.)

Every rewritten file's old text is kept in <board>/.paper-version-N/<path>.orig with its record
.paper-version-N.yaml, the records haipipe-paper/scripts/paper_ladder.py keeps, so rollback restores it exactly.
route: one Review Item's row in the report's ## Review Items table gets where it lands (`lands on`: the owning
    Page stem, ¶N, claim ids), its work (`run-revise-<slug>` by default, the Run its Section opens; `declined` with
    --decline) and state routed (declined). The report never writes into the Section's folder: it declares the
    reopening, and the command printed after it lands it (feedback.py collect; page.py open-run).
reply: the row gets the Response Package paragraph that answers it and its state (answered by default). An item
    is answered only when every point it cites is; the skill's G5 check stays the judge.
Nothing is committed.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("paper_ladder", HERE.parents[1] / "haipipe-paper" / "scripts" /
                                               "paper_ladder.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)
T, M, read, header = L.T, L.M, L.read, L.header


def add(run, batch, to):
    b = run.board
    src = b / batch
    if not src.is_dir() or not (src / (src.name + ".md")).is_file():
        sys.exit(f"stop: {batch} is not a Page folder")
    if not (b / to).is_dir() and f"{to}/{to}.md" not in run.create:
        sys.exit(f"stop: {to} is not a version folder")
    old = src.name
    rest = re.sub(r"^(t\d{2}_|RD\d+[-_]|CM\d+[-_])", "", old)
    have = [int(p.name[1:3]) for p in (b / to / "reports").glob("q[0-9][0-9]_*")] + \
           [int(Path(r).parts[2][1:3]) for r in run.create if r.startswith(f"{to}/reports/q")]
    stem = f"q{(max(have) if have else 0) + 1:02d}_{rest}"
    target = f"{to}/reports/{stem}"
    run.moves += [(batch, target), (f"{target}/{old}.md", f"{target}/{stem}.md")]
    run.moves += [(f"{target}/draft/{f.name}", f"{target}/draft/{f.name.replace(old, stem, 1)}")
                  for f in sorted((src / "draft").glob(f"{old}-*")) if f.is_file()]
    mapping = [(f"{batch}/{old}.md", f"{target}/{stem}.md"), (batch, target)]
    face = read(src / (old + ".md"))           # its face: the type, its name
    face = re.sub(r"(?m)\A# +%s\b" % re.escape(old), "# " + stem, face, count=1)
    face = header(header(face, "page-type", "comments"), "folder-kind", "comments")
    title = re.sub(r"^#\s+\S+\s*·?\s*", "", face.splitlines()[0]).strip() or rest
    first = re.search(r"(?ms)^## Opening\s*\n+(.*?)(?:\n\n|\Z)", face)          # its Opening's first paragraph
    opening = first.group(1).strip() if first else title
    vface = f"{to}/{to}.md"                    # a row in the version's ## Questions (group: comments)
    vt = run.text(vface)
    reg = re.search(r"(?ms)^## Questions.*?```ya?ml\n(.*?)```", vt)
    ids = [int(x) for x in re.findall(r"(?m)^- id: Q(\d+)", reg.group(1))] if reg else []
    qid = f"Q{(max(ids) if ids else 0) + 1:02d}"
    # a report names the Question it answers, and its walk starts open (haipipe-report)
    face = header(face, "answers", qid)
    if not re.search(r"(?m)^answer-status:", face):
        face = header(face, "answer-status", "open")
    run.rewrite[f"{target}/{stem}.md"] = T.fix_links(face.replace(old, stem), f"{batch}/{old}.md",
                                                    f"{target}/{stem}.md", b, mapping)
    row = (f"- id: {qid}\n  title: {T.yaml_s(title)}\n  question: {T.yaml_s(opening)}\n  group: comments\n"
           f"  report: reports/{stem}/{stem}.md\n")
    if reg:
        body = reg.group(1).replace("questions: []", "questions:\n")
        vt = vt[:reg.start(1)] + body.rstrip("\n") + "\n" + row + vt[reg.end(1):]
    else:
        vt = vt.rstrip("\n") + f"\n\n## Questions\n\n```yaml\nquestions:\n{row}```\n"
    # the version responds to it; `answers:` on a Job face is for the Block's Question ids (haipipe-report)
    run.set(vface, header(vt, "responds-to", f"reports/{stem}/{stem}.md"))
    for f in sorted(b.rglob("*")):             # every other source text that names it or links to it
        rel = f.relative_to(b).as_posix()
        if (not f.is_file() or f.suffix not in L.TEXT or rel.startswith(".") or rel.startswith(batch + "/")
                or M.skipped(rel) and not rel.endswith("paper-build.toml")):
            continue
        t = run.text(rel)
        nt = T.fix_links(t, rel, rel, b, mapping).replace(batch + "/", target + "/").replace(old, stem)
        if rel == "board.md":                   # no longer a Page of the version it judged
            nt = re.sub(r"(?m)^%s\.md\n" % re.escape(stem), "", nt)
        if nt != t:
            run.set(rel, nt)
    return stem


ITEMS = re.compile(r"(?ms)^## Review Items\s*\n(?:.*?\n)??(\|[^\n]*\|\n\|[-| :]+\|\n(?:\|[^\n]*\|\n?)*)")
STATES = ("open", "routed", "applied", "answered", "declined", "deferred")


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def set_item(run, report, item, **cells):
    """Set cells of one row of a report's ## Review Items table, the row named by its item; returns the row."""
    b = run.board
    face = b / report / (Path(report).name + ".md")
    if not face.is_file():
        sys.exit(f"stop: {report} has no face {face.name}")
    rel_ = face.relative_to(b).as_posix()
    text = run.text(rel_)
    m = ITEMS.search(text)
    if not m:
        sys.exit(f"stop: {face.name} has no ## Review Items table")
    lines = m.group(1).rstrip("\n").split("\n")
    head = _cells(lines[0])
    for need in ("item", *cells):
        if need.replace("_", " ") not in head:
            sys.exit(f"stop: the Review Items table has no {need.replace('_', ' ')!r} column")
    for k, line in enumerate(lines[2:], 2):
        row = _cells(line)
        if row and row[0] == item:
            row += [""] * (len(head) - len(row))
            for key, value in cells.items():
                row[head.index(key.replace("_", " "))] = value
            lines[k] = "| " + " | ".join(row) + " |"
            break
    else:
        sys.exit(f"stop: no Review Item {item} in {face.name}")
    run.set(rel_, text[:m.start(1)] + "\n".join(lines) + "\n" + text[m.end(1):])
    return dict(zip(head, row))


def route(run, report, item, to, work, decline):
    slug = re.sub(r"^Review-", "", item)
    row = set_item(run, report, item, lands_on=to, work="declined" if decline else (work or f"run-revise-{slug}"),
                   state="declined" if decline else "routed")
    if not decline:
        stem = to.split()[0]
        print(f"then: python haipipe-page/cli/feedback.py collect --all <board> · "
              f"python haipipe-page/cli/page.py open-run <{stem}> --kind revise --slug {slug}")
    return row


def reply(run, report, item, para, state):
    if state not in STATES:
        sys.exit(f"stop: --state is one of {', '.join(STATES)}")
    return set_item(run, report, item, reply=para, state=state)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board", type=Path)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("batch")
    a_.add_argument("--to", required=True)
    a_.add_argument("--dry-run", action="store_true")
    r_ = sub.add_parser("route")
    r_.add_argument("report")
    r_.add_argument("item")
    r_.add_argument("--to", required=True)
    r_.add_argument("--work", default="")
    r_.add_argument("--decline", action="store_true")
    p_ = sub.add_parser("reply")
    p_.add_argument("report")
    p_.add_argument("item")
    p_.add_argument("--reply", required=True)
    p_.add_argument("--state", default="answered")
    for x in (r_, p_):
        x.add_argument("--dry-run", action="store_true")
    sub.add_parser("rollback")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        sys.exit(f"stop: {board.name} has no board.md")
    if a.cmd == "rollback":
        return L.rollback(board)
    run = L.Run(board)
    if a.cmd == "route":
        row = route(run, a.report.rstrip("/"), a.item, a.to, a.work, a.decline)
        what = f"route {a.item} → {row['lands on']} ({row['work']})"
    elif a.cmd == "reply":
        row = reply(run, a.report.rstrip("/"), a.item, a.reply, a.state)
        what = f"reply {a.item} → {row['reply']} ({row['state']})"
    else:
        what = f"comments {add(run, a.batch.rstrip('/'), a.to)} into {a.to}"
    if a.dry_run:
        print(what)
        run.show()
    else:
        run.apply(what)


if __name__ == "__main__":
    main()
