#!/usr/bin/env python3
"""review_items.py · a paper's review Jobs and their Review Items (hai-paper-comments, b16 Q05).

    python review_items.py <board> add <batch folder> --to <version>    a review batch into a review Job on the Board
    python review_items.py <board> route <report> <item> --to "<stem> ¶N · C2" [--work <run> | --decline]
    python review_items.py <board> reply <report> <item> --reply P3 [--state answered|applied|declined|deferred]
    python review_items.py <board> rollback                            undo the newest add, route or reply
    (add --dry-run to add, route or reply: print what it would do; change nothing)

add: a review batch is a review Job on the Board (JL 261110; a report in <version>/reports/ before):
    jNN_review_<kind>_v<MMDD>/t01_<kind>_comments/, its Job face `for: <version>`, the version's face
    `responds-to: <the Job>`. Its folder keeps feedback/, meeting/ and sent/ unchanged. Every source text that
    names it or links to it follows. (Was version_paper.py comments.)

Every rewritten file's old text is kept in <board>/.paper-version-N/<path>.orig with its record
.paper-version-N.yaml, the records hai-paper/scripts/paper_ladder.py keeps, so rollback restores it exactly.
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
_spec = importlib.util.spec_from_file_location("paper_ladder", HERE.parents[1] / "hai-paper" / "scripts" /
                                               "paper_ladder.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)
T, M, read, header = L.T, L.M, L.read, L.header


KIND_WORD = {"review": "reviewers"}             # a Job's kind word: j31_review_reviewers_v0110, not review_review


def add(run, batch, to):
    """A review batch becomes a review Job on the Board (JL 261110: "we will no longer use the reports/, please use the
    job or studio"): jNN_review_<kind>_v<MMDD>/, its face `for: <the version>`, the batch Page its first Task
    t01_<kind>_comments/; the version's face says `responds-to: <the Job>`."""
    b = run.board
    src = b / batch
    if not src.is_dir() or not (src / (src.name + ".md")).is_file():
        sys.exit(f"stop: {batch} is not a Page folder")
    if not (b / to).is_dir() and f"{to}/{to}.md" not in run.create:
        sys.exit(f"stop: {to} is not a version folder")
    old = src.name
    rest = re.sub(r"^(t\d{2}_|q\d{2}_|RD\d+[-_]|CM\d+[-_])", "", old)
    m = re.match(r"(?i)(.+?)[-_](\d{4})$", rest)
    kind, mmdd = (m.group(1), m.group(2)) if m else (rest, "")
    kind = re.sub(r"[^a-z0-9]+", "_", KIND_WORD.get(kind.lower(), kind.lower())).strip("_") or "comments"
    have = [int(p.name[1:3]) for p in b.glob("j3[0-9]_*") if p.is_dir()] + \
           [int(r[1:3]) for r in run.create if re.match(r"j3\d_", r)]
    job = f"j{(max(have) if have else 30) + 1:02d}_review_{kind}" + (f"_v{mmdd}" if mmdd else "")
    stem = f"t01_{kind}_comments"
    target = f"{job}/{stem}"
    run.moves += [(batch, target), (f"{target}/{old}.md", f"{target}/{stem}.md")]
    run.moves += [(f"{target}/draft/{f.name}", f"{target}/draft/{f.name.replace(old, stem, 1)}")
                  for f in sorted((src / "draft").glob(f"{old}-*")) if f.is_file()]
    mapping = [(f"{batch}/{old}.md", f"{target}/{stem}.md"), (batch, target)]
    face = read(src / (old + ".md"))           # its face: the type, its name
    face = re.sub(r"(?m)\A# +%s\b" % re.escape(old), "# " + stem, face, count=1)
    face = header(header(face, "page-type", "comments"), "folder-kind", "comments")
    face = header(face, "use-case", "Reviewer response")
    title = re.sub(r"^#\s+\S+\s*·?\s*", "", face.splitlines()[0]).strip() or rest
    run.rewrite[f"{target}/{stem}.md"] = T.fix_links(face.replace(old, stem), f"{batch}/{old}.md",
                                                    f"{target}/{stem}.md", b, mapping)
    run.create[f"{job}/{job}.md"] = (
        f"# {job} · {title}\nuse-case: Feedback revision\nlayer: review\nfor: {to}\nfolder-kind: job\n"
        f"state: open · no reply yet\ngoal: every point in this batch answered once, in {to}\n"
        f"close: each Review Item is routed to its Section in {to} and answered in its response letter\n\n"
        f"## Tasks\n\n1. [{stem}]({stem}/{stem}.md) · {title}: what came back, its Review Items, and where each "
        f"is answered\n")
    vface = f"{to}/{to}.md"                    # the version responds to the Job
    run.set(vface, header(run.text(vface), "responds-to", job))
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
    return job

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
        print(f"then: python hai-draft/cli/feedback.py collect --all <board> · "
              f"python hai-draft/cli/page.py open-run <{stem}> --kind revise --slug {slug}")
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
