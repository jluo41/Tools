#!/usr/bin/env python3
"""write_answer_page — lay one answering page out in the haipipe-page shape, from a spec.

The writer authors a YAML spec: the title, the Opening, and one Content
division per evidence need, each with its paragraphs and Bullets, every Bullet
carrying its Draft sentence and either its Evidence Item or the judge need it
makes. This tool only formats what the writer wrote (ref/report.md § The flow,
steps 2 and 3):

    draft/<stem>-draft-v<G>.<S>.md     the plan: Structure · Scratch · Draft
    draft/<stem>-evidence-items.md     one Evidence Item per compute or cite need
    <stem>.md                          header, Opening, Content skeleton whose
                                       tagged lines `page.py adopt` then fills

A page written before this shape is archived whole to
`draft/_archive/<stem>-page-before-<YYMMDD>.md`, and its `## Log` entries are
appended to `draft/records/<stem>-log.md`. A current plan is moved to
`draft/previous/` before the new one is written. Run `page.py adopt <page>`
and `page.py health <page>` afterwards.

    write_answer_page.py <page folder> <spec.yaml> [--version v0.1]

An Instance question page (ref/prototype-contract.md: the question folder in an
Instance board, one run per partition) needs no answers:, state: or ticket: keys:
its header carries question: and partitions: from the folder and no state: line
(status is computed). It has one division per partition the question is asked
on, in partitions.md order, each naming its `partition:`. Each item and figure
names its `partition:`, and reads results/<partition>/<file> unless it names
another `artifact:`.

Spec (YAML):

    title: "<subject>: <deliverable>"          # three to five words
    folder-kind: information | knowledge | data | wisdom
    answers: [QI4]
    strength: MODERATE                          # Knowledge only
    state: "🟡 CHECK pending"
    arc: <the argument the divisions make, one sentence>
    opening: [<sentence>, <sentence>, ...]      # the visible paragraph, one sentence per line
    sits: <Where this Page sits>
    matters: <Why it matters>
    covered: <Covered elsewhere>
    items:
      - {id: E01-VALUE-<slug>, target: C1.P1.B1, name: <what it supplies>, need: QI4.E1,
         ticket: <page ticket stem>, file: <result file>, columns: <columns read>,
         expected: <the need's pass>, accept: <the observable check>, supporting: b51j21t01r01}
    divisions:
      - title: <subject in plain words>
        map: <division map caption>
        diagram: <one or two lines of text>
        figure: {caption: <caption>, ticket: <page ticket stem>, file: fig_<name>.png}   # optional
        paragraphs:
          - label: <paragraph label>
            job: <the job this paragraph performs>
            bullets:
              - {role: <Role>, point: <4-11 words>, note: <constraint>, item: E01-VALUE-<slug>,
                 accept: <check>, draft: <one sentence>}
              - {role: <Role>, point: ..., note: ..., judge: QK2.E2, from: "E1", draft: ...}
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

import yaml


KEYS = {
    "spec": {"title", "folder-kind", "answers", "strength", "state", "arc", "opening", "sits",
             "matters", "covered", "items", "divisions"},
    "item": {"id", "target", "name", "need", "ticket", "file", "artifact", "columns", "expected", "accept",
             "supporting", "partition"},
    "division": {"title", "map", "diagram", "figure", "paragraphs", "partition"},
    "figure": {"caption", "ticket", "file", "partition"},
    "paragraph": {"label", "job", "bullets"},
    "bullet": {"role", "point", "note", "item", "accept", "judge", "from", "none", "draft"},
}


def validate(spec: dict) -> None:
    """Refuse a key the format does not know. In a YAML flow mapping an unquoted comma
    splits one value into stray keys, so `{note: a, b}` silently becomes note: "a";
    quote any value that holds a comma or a colon."""
    def check(obj, kind, where):
        bad = [k for k in obj if k not in KEYS[kind]] if isinstance(obj, dict) else ["(not a mapping)"]
        if bad:
            raise SystemExit(f"{where}: unknown key(s) {bad}; quote values that contain commas or colons")
        for k, v in obj.items():
            if v is None and k not in ("covered", "strength"):
                raise SystemExit(f"{where}.{k}: empty value (an unquoted comma or colon?)")
    check(spec, "spec", "spec")
    for i, it in enumerate(spec.get("items", [])):
        check(it, "item", f"items[{i}]")
    for c, div in enumerate(spec["divisions"], 1):
        check(div, "division", f"division {c}")
        for m, para in enumerate(div["paragraphs"], 1):
            check(para, "paragraph", f"division {c} paragraph {m}")
            for k, b in enumerate(para["bullets"], 1):
                check(b, "bullet", f"division {c} paragraph {m} bullet {k}")


def _bound_tickets(page):
    """The page's runs the header lists: the tickets its answers.yaml binds, not every file in runs/."""
    amap = yaml.safe_load((page / "answers.yaml").read_text(encoding="utf-8")) if (page / "answers.yaml").is_file() else {}
    found = set()
    for needs in (amap or {}).values():
        for b in (needs or {}).values():
            if isinstance(b, dict):
                found.update([b["ticket"]] if b.get("ticket") else [])
                found.update(b.get("tickets") or [])
    return {t for t in found if (page / "runs" / f"{t}.sh").is_file()}


def _instance_page(page):
    """An Instance question folder: its board.md two levels up says board-kind: insight-instance."""
    board = page.parents[1] / "board.md"
    return board.is_file() and re.search(r"(?m)^board-kind:\s*insight-instance\s*$", board.read_text(encoding="utf-8"))


def _partition_runs(page):
    """The page's partition runs, in the Prototype's 0-Meta/partitions.md order."""
    runs = {t.stem for t in (page / "runs").glob("*.sh") if not t.stem.startswith("run-")}
    board = (page.parents[1] / "board.md").read_text(encoding="utf-8")
    proto = re.search(r"(?m)^prototype:\s*(\S+)", board)
    order = []
    if proto:
        parts = (page.parents[1] / proto.group(1) / "0-Meta" / "partitions.md")
        if parts.is_file():
            order = re.findall(r"name:\s*([a-z]+)", parts.read_text(encoding="utf-8"))
    return [n for n in order if n in runs] + sorted(runs - set(order))


def _item_rows(items):
    rows = []
    for i in items:
        if i.get("partition"):
            i.setdefault("ticket", i["partition"])
        i.setdefault("supporting", i.get("ticket", "cited page"))
        art = i.get("artifact") or f"results/{i['ticket']}/{i['file']}"
        rows += [f"### {i['id']} · {i['target']} · {i['name']}", "",
                 f"- **Need**: {i['need']}", f"- **Artifact**: `{art}` · {i['columns']}",
                 f"- **Expected**: {i['expected']}", f"- **Accept**: {i['accept']}",
                 f"- **Supporting Runs**: Execution · reuse · {i['supporting']}",
                 f"- **Local Run**: Page · Evidence Item · reuse · {i.get('ticket', 'cited page')} → {art}",
                 "- **Status**: landed", ""]
    return rows


def build(page: Path, spec: dict, version: str) -> None:
    validate(spec)
    stem = page.name
    draft = page / "draft"
    (draft / "records").mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().strftime("%y%m%d")
    md = page / f"{stem}.md"

    # an old page is kept whole, and its log carries over
    if md.is_file() and "<!-- realizes:" not in md.read_text(encoding="utf-8"):
        old = md.read_text(encoding="utf-8")
        (draft / "_archive").mkdir(exist_ok=True)
        (draft / "_archive" / f"{stem}-page-before-{today}.md").write_text(old, encoding="utf-8")
        log = re.search(r"(?ms)^## Log\s*\n(.*?)(?=^## |\Z)", old)
        if log and log.group(1).strip():
            rec = draft / "records" / f"{stem}-log.md"
            prev = rec.read_text(encoding="utf-8") if rec.is_file() else f"# {stem} · log\n"
            rec.write_text(prev.rstrip() + "\n\n" + log.group(1).strip() + "\n", encoding="utf-8")
    supersedes = "none"
    for current in sorted(draft.glob(f"{stem}-draft-v*.md")):
        (draft / "previous").mkdir(exist_ok=True)
        target = draft / "previous" / current.name
        if not target.exists():
            current.rename(target)
        supersedes = current.stem.rsplit("-draft-", 1)[1]

    items = {i["id"]: i for i in spec.get("items", [])}
    overview, structure, scratch, drafts, content = [], [], [], [], []
    p = figures = 0
    for c, div in enumerate(spec["divisions"], 1):
        overview.append(f"- C{c} · {div['title']}")
        content += [f"### {c} · {div['title']}", "", f"**Division map**: {div['map']}", "",
                    "```text", div["diagram"].rstrip(), "```", ""]
        fig = div.get("figure")
        if fig and fig.get("partition"):
            fig.setdefault("ticket", fig.pop("partition"))
        if fig:
            figures += 1                                   # figures are numbered in reading order, not by division
            content += [f"Figure {figures} · {fig['caption'].rstrip('.')}.", "",
                        f"![{fig['caption'].rstrip('.')}](results/{fig.get('ticket', 'compute')}/{fig['file']})", ""]
        for m, para in enumerate(div["paragraphs"], 1):
            p += 1
            addr = f"C{c}.P{p}"
            overview.append(f"- {addr} · {para['label']}")
            structure.append(f"### {addr} · {para['label']}")
            scratch.append(f"### {addr} · {para['label']}\n")
            drafts.append(f"### {addr} · {para['label']}")
            content += [f"#### {c}.{m} · {para['label']}", f"({para['job']})"]
            for k, b in enumerate(para["bullets"], 1):
                structure += [f"- B{k} · [{b['role']}] {b['point']}", f"  Note: {b['note']}"]
                if b.get("item"):
                    if b["item"] not in items:
                        raise SystemExit(f"{addr}.B{k}: item {b['item']} is not declared under items:")
                    structure += [f"  Evidence: {b['item']} · {items[b['item']]['name']}",
                                  f"  Accept: {b.get('accept') or items[b['item']]['accept']}"]
                elif b.get("judge"):
                    structure.append(f"  Evidence: none · judge {b['judge']} from {b.get('from', 'the needs above')}")
                else:
                    structure.append(f"  Evidence: none · {b.get('none', 'orientation, asserts no value')}")
                drafts.append(f"- B{k} · {b['draft'].strip()}")
                content.append(f"pending <!-- realizes: {addr}.B{k} -->")
            structure.append("")
            drafts.append("")
            content.append("")

    plan = [f"# {stem} · draft {version}", f"draft-version: {version}", f"supersedes: {supersedes}", f"date: {today}",
            "approved: ⬜", "status: ⬜", f"arc: {spec['arc']}", "",
            "## 1 · Structure · Bullet Point Table", "", "### Structure Overview", "", *overview, "", *structure,
            "## 2 · Scratch · What to write here", "", "", *scratch, "## 3 · Draft · Reading and Revise", "", *drafts]
    (draft / f"{stem}-draft-{version}.md").write_text("\n".join(plan).rstrip() + "\n", encoding="utf-8")

    rows = [f"# {stem} · Evidence Items", "", f"page: {stem}", f"plan: draft/{stem}-draft-{version}.md · {version}",
            "state: ✅ every item landed from a bound task result", "",
            "One item per bound file of a compute or cite need; a judge need has no item. Each item's Need",
            "line names the need it answers; its Artifact is a file the need's run wrote.", "",
            "## Citations", ""]
    cites = [i for i in spec.get("items", []) if "←" in str(i["need"])]      # a cite need's item reads another page
    values = [i for i in spec.get("items", []) if i not in cites]
    for section, group in (("Citations", cites), ("Values", values)):
        if section == "Values":
            rows += ["", "## Displays", "", "", "## Values", ""]
        rows += _item_rows(group)
    (draft / f"{stem}-evidence-items.md").write_text("\n".join(rows).rstrip() + "\n", encoding="utf-8")

    read = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if _instance_page(page):
        tickets = _partition_runs(page)
        named = [d.get("partition") for d in spec["divisions"]]
        if named != tickets:
            raise SystemExit(f"an Instance page has one division per partition, in order: {tickets}; "
                             f"the spec's divisions name {named}")
        head = [f"# {spec['title']}", "", f"folder-kind: {spec['folder-kind']}",
                f"question: {stem[:3]}", f"partitions: {', '.join(tickets)}"]
    else:
        tickets = sorted(_bound_tickets(page))
        head = [f"# {spec['title']}", "", f"state: {spec.get('state', '🟡 CHECK pending')}",
                f"folder-kind: {spec['folder-kind']}",
                f"answers: {', '.join(spec['answers'])}"]
    if spec.get("strength"):
        head.append(f"strength: {spec['strength']}")
    if tickets:
        head.append(f"runs: {', '.join(tickets)}")
    head += [f"results-read: {read}", "", "## Opening", "", *spec["opening"], "",
             f"**Where this Page sits:** {spec['sits']}", "", f"**Why it matters:** {spec['matters']}", ""]
    if spec.get("covered"):
        head += [f"**Covered elsewhere:** {spec['covered']}", ""]
    md.write_text("\n".join(head + ["## Content", ""] + content).rstrip() + "\n", encoding="utf-8")
    print(f"{stem}: {len(spec['divisions'])} divisions, {p} paragraphs, {len(items)} items · now run page.py adopt")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("page", type=Path)
    ap.add_argument("spec", type=Path)
    ap.add_argument("--version", default="v0.1")
    a = ap.parse_args(argv)
    if not a.page.is_dir():
        print(f"{a.page}: not a page folder", file=sys.stderr)
        return 2
    build(a.page.resolve(), yaml.safe_load(a.spec.read_text(encoding="utf-8")), a.version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
