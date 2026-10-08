"""carry_over.py <old board> <block> --dataset <name>=<parquet> [--thresholds <yaml>] [--report <md>] [--check] · make an Insight Block from a register board, word for word.

An InsightBoard made the register way (ref/board-contract.md: 0-MT-meta/MT00-meta and the
four question registers MT01-MT04) already holds the meaning of every question: its short
Queue wording, its name, its ask, why it is asked now, what would answer it, its live and
retired evidence needs, and its agreed mark. This script moves that meaning into an
Insight Block, a task Block (ref/block-contract.md), without rewriting a word of it:

    board.md                       board-kind: task-block · workbench: insight · datasets:
                                   (from --dataset); the old board's title and purpose sections
    meta/meta.md                   the meta page's Opening, Diagram and Content
    meta/partitions.md             the partition register, parsed into filters; its division verbatim
    meta/thresholds.yaml           the shared thresholds file the meta page names, values verbatim
    jNN_<level>/level.md           each register's Opening, Queue and Law, verbatim
    jNN_<level>/tNN_<name>/question.md   one question file v2 per register division

Ids are renamed by one rule, Q<L><n> -> <L><NN> (QI3 -> I03), in the question's id and in
every need's `from:`; the task folder is t<NN>_<name> in its level's Job; no other text changes. A cell the register refused for a LOGIC
reason (full-only, defer) is not asked on that partition; a cell refused for a DATA reason
(thin, no measure) is asked, and the run refuses it again or answers it.

--check re-reads the old board and compares every carried field with the Block's files
(the evaluation's fidelity test): exit 1 on any difference. A second run on a fresh folder
writes the same bytes. Nothing is written over an existing Block.
"""
import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

import yaml

LEVEL_JOB = {"D": ("data", "j01_data"), "I": ("information", "j02_information"),
           "K": ("knowledge", "j03_knowledge"), "W": ("wisdom", "j04_wisdom")}
LOGIC_REFUSALS = {"full-only", "defer"}          # the question does not mean the same inside a partition
FIELD = re.compile(r"^\*\*([^*]+)\*\*: ?(.*)$")
NEED = re.compile(r"^- (E\d+) · (compute|cite|judge) · (.*?)(?: · pass: (.*?))?(?: · from: (.*?))?"
                  r"(?: · retired: (.*))?$")
SPEC_LINE = re.compile(r"^    ([a-z_]+): (.*)$")
SPEC_KEYS = ("cut", "unit", "measure", "by", "uncertainty", "rivals", "output")
DIVISION = re.compile(r"^#### \d+ · (Q([DIKW])(\d+)) · (.+?)\s*$")
OLD_REF = re.compile(r"\bQ([DIKW])(\d+)\.(E\d+)\b")
NEW_REF = re.compile(r"\b([DIKW])(\d{2})\.(E\d+)\b")
MARK = re.compile(r"^(·|[🟡✅🚫⬜] \S.*)$")
NAMED = {"The ask": "ask", "Why now": "why", "What would answer it": "answer",
         "Needs agreed": "agreed", "Where it stands": "stood"}


class CarryError(Exception):
    pass


# ── markdown, fence-aware ────────────────────────────────────────────────────
def blocks(text):
    """[(heading line or '', lines)] split at headings outside ``` fences."""
    out, cur, head, fence = [], [], "", False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,4} ", line):
            out.append((head, cur))
            head, cur = line, []
        else:
            cur.append(line)
    out.append((head, cur))
    return out


def section(text, title, level):
    """The text of the heading `title` at `level` (# count), up to the next heading of that level or higher."""
    keep, on = [], False
    for head, lines in blocks(text):
        depth = len(head) - len(head.lstrip("#")) if head else 0
        if on and head and depth <= level:
            break
        if head and depth == level and head[depth + 1:].strip() == title:
            on = True
        if on:
            keep += ([head] if head else []) + lines
    return "\n".join(keep).strip("\n")


def title_of(text):
    m = re.search(r"(?m)^# (.+?)\s*$", text)
    return m.group(1) if m else ""


def from_heading(text, heading):
    """The text from the first `heading` line on (the page header above it dropped)."""
    i = text.find("\n" + heading + "\n")
    if i < 0:
        raise CarryError(f"no '{heading}' heading")
    return text[i + 1:]


def until_heading(text, heading):
    i = text.find("\n" + heading + "\n")
    return text if i < 0 else text[:i + 1]


# ── ids and names ────────────────────────────────────────────────────────────
def new_id(letter, n):
    return f"{letter}{int(n):02d}"


def map_refs(s):
    return OLD_REF.sub(lambda m: f"{new_id(m.group(1), m.group(2))}.{m.group(3)}", s)


def unmap_refs(s):
    return NEW_REF.sub(lambda m: f"Q{m.group(1)}{int(m.group(2))}.{m.group(3)}", s)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ── the registers ────────────────────────────────────────────────────────────
def queue_rows(register):
    """{old id: {"question", "gen1", "cells": {partition: mark}}} from the register's Queue block."""
    q = section(register, "1 · Queue", 3)
    m = re.search(r"```text\n(.*?)\n```", q, re.S)
    if not m:
        raise CarryError("the Queue division has no text block")
    lines = m.group(1).split("\n")
    header = lines[0]
    cols = [(x.start(), x.group(0)) for x in re.finditer(r"\S+(?: \S+)*", header)]
    labels = [c[1] for c in cols]
    if labels[:2] != ["id", "question"]:
        raise CarryError(f"Queue header {labels[:2]} is not id, question")

    def cut(line):
        """The line's cells by display column (a wide character, an emoji, takes two)."""
        at, pos = [], 0
        for ch in line:
            at.append(pos)
            pos += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        out = []
        for i, (start, _) in enumerate(cols):
            end = cols[i + 1][0] if i + 1 < len(cols) else pos + 1
            out.append("".join(ch for ch, x in zip(line, at) if start <= x < end).strip())
        return out

    rows, cur, transposed = {}, None, "partition" in labels
    for line in lines[1:]:
        if line.startswith("─") or line.startswith("──"):
            continue
        if not line.strip():
            break
        cells = cut(line)
        qid = cells[0]
        if qid:
            if not re.fullmatch(r"Q[DIKW]\d+", qid):
                raise CarryError(f"Queue row id {qid!r}")
            cur = rows.setdefault(qid, {"question": "", "gen1": "", "cells": {}})
            cur["gen1"] = cur["gen1"] or cells[2]
        if cells[1] and cur is not None:
            target = rows[qid] if qid else cur
            target["question"] = (target["question"] + " " + cells[1]).strip()
        if transposed:
            part = cells[labels.index("partition")]
            for j, label in enumerate(labels):
                if re.fullmatch(r"Q[DIKW]\d+", label) and part:
                    rows.setdefault(label, {"question": "", "gen1": "", "cells": {}})["cells"][part] = cells[j]
        elif qid:
            for j, label in enumerate(labels[3:], start=3):
                cur["cells"][label] = cells[j]
    for qid, r in rows.items():
        for part, mark in r["cells"].items():
            if not MARK.match(mark):
                raise CarryError(f"{qid} · {part}: cell {mark!r} is not a register mark")
    return rows


def parse_division(lines):
    """One `#### N · Q.. · Name` division → its fields in order and its needs, as written."""
    fields, needs, cur = [], [], None
    for line in lines:
        f = FIELD.match(line)
        if f:
            cur = ["field", f.group(1), [f.group(2)]]
            fields.append(cur)
            continue
        n = NEED.match(line)
        if n:
            cur = ["need", n, [line]]
            needs.append(cur)
            continue
        if cur is None:
            if line.strip():
                raise CarryError(f"text before the first field: {line[:60]!r}")
            continue
        if cur[0] == "need" and not SPEC_LINE.match(line):
            if line.strip():
                raise CarryError(f"need {cur[1].group(1)}: a line that is not a spec line: {line[:60]!r}")
            cur = None
            continue
        cur[2].append(line)
    out = {}
    for _, label, text in fields:
        value = "\n".join(text).strip("\n")
        out[NAMED.get(label, label)] = value
    return out, [(n[1], n[2]) for n in needs]


def need_v2(match, lines):
    nid, kind, what, pass_, frm, retired = match.groups()
    n = {"kind": kind, "what": what}
    if pass_ is not None:
        n["pass"] = pass_
    if frm is not None:
        refs = [map_refs(x.strip()) for x in frm.split(",")]
        n["from"] = refs[0] if kind == "cite" and len(refs) == 1 else refs
    if retired is not None:
        n["retired"] = retired
    for line in lines[1:]:
        k, v = SPEC_LINE.match(line).groups()
        if k == "output":
            out = {}
            for part in v.split(" ; "):
                m = re.fullmatch(r"([\w.-]+) \[(.*)\]", part.strip())
                if not m:
                    raise CarryError(f"{nid}: output part {part!r} is not <file> [<columns>]")
                out[m.group(1)] = [c.strip() for c in m.group(2).split(",")]
            n["output"] = out
        else:
            n[k] = v
    return nid, n


def need_lines(nid, n):
    """A v2 need rendered back into the register's own lines (ids in the register's form)."""
    head = f"- {nid} · {n['kind']} · {n['what']}"
    if "pass" in n:
        head += f" · pass: {n['pass']}"
    if "from" in n:
        refs = n["from"] if isinstance(n["from"], list) else [n["from"]]
        head += " · from: " + ", ".join(unmap_refs(str(r)) for r in refs)
    if "retired" in n:
        head += f" · retired: {n['retired']}"
    lines = [head]
    for k in SPEC_KEYS:
        if k in n:
            v = n[k]
            if k == "output":
                v = " ; ".join(f"{f} [{', '.join(c)}]" for f, c in v.items())
            lines.append(f"    {k}: {v}")
    return lines


def asked_of(cells, order):
    """partitions.asked and not_elsewhere from the register's cells for one question."""
    names = [p for p in order if p in cells]
    asked = [p for p in names if cells[p] != "·" and not (
        cells[p].startswith("🚫 ") and cells[p][2:].strip() in LOGIC_REFUSALS)]
    rest = [p for p in names if p not in asked]
    block = {}
    if set(asked) == set(p for p in names if p != "cross") and "cross" not in asked:
        block["asked"] = "all"
    elif asked == ["cross"]:
        block["asked"] = "cross"
    else:
        block["asked"] = asked
    if block["asked"] != "all":
        by_mark = {}
        for p in rest:
            by_mark.setdefault(cells[p], []).append(p)
        block["not_elsewhere"] = "carried: the register marks it " + "; ".join(
            f"{mark} on {', '.join(ps)}" for mark, ps in by_mark.items())
    return block


def registers(old):
    found = sorted((old / "0-MT-meta").glob("MT0[1-4]-*/MT0[1-4]-*.md"))
    if len(found) != 4:
        raise CarryError(f"{old.name}: expected the four registers MT01-MT04, found {len(found)}")
    return found


def read_questions(old, order):
    """Every register division as the carried record: id, folder, fields, needs, cells."""
    out = []
    for reg in registers(old):
        text = reg.read_text(encoding="utf-8")
        queue = queue_rows(text)
        for head, lines in blocks(text):
            m = DIVISION.match(head)
            if not m:
                continue
            old_id, letter, n, name = m.groups()
            if old_id not in queue:
                raise CarryError(f"{reg.name}: {old_id} has a division but no Queue row")
            fields, needs = parse_division(lines)
            for k in ("ask", "why", "answer", "agreed"):
                if not fields.get(k):
                    raise CarryError(f"{old_id}: no '{k}' field")
            qid = new_id(letter, n)
            out.append({"old_id": old_id, "id": qid, "letter": letter, "name": name, "register": reg.parent.name,
                        "folder": f"t{qid[1:]}_{slug(name).replace('-', '_')}", "fields": fields, "needs": needs, **queue[old_id]})
    ids = [q["id"] for q in out]
    if len(set(ids)) != len(ids):
        raise CarryError("two divisions carry the same id")
    return out


def question_file(q, order, old_rel):
    level, _ = LEVEL_JOB[q["letter"]]
    f = q["fields"]
    needs = dict(need_v2(m, lines) for m, lines in q["needs"])
    source = {"board": old_rel, "register": q["register"], "id": q["old_id"], "gen1": q["gen1"],
              "cells": {p: q["cells"][p] for p in order if p in q["cells"]}}
    if f.get("stood"):
        source["stood"] = f["stood"]
    meta = {"id": q["id"], "level": level, "question": q["question"], "name": q["name"], "ask": f["ask"],
            "source": source, "partitions": asked_of(q["cells"], order), "needs": needs, "agreed": f["agreed"]}
    extras = [(k, v) for k, v in f.items() if k not in NAMED.values()]
    body = [q["name"], "=" * len(q["name"]), "", f"**Why now**: {f['why']}", "",
            f"**What would answer it**: {f['answer']}"]
    for k, v in extras:
        body += ["", f"**{k}**: {v}"]
    return ("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100000, default_flow_style=None)
            + "---\n\n" + "\n".join(body) + "\n")


def read_v2(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    meta, body = yaml.safe_load(m.group(1)), m.group(2)
    fields, label, buf = {}, None, []
    for line in body.split("\n")[3:]:
        f = FIELD.match(line)
        if f:
            if label:
                fields[label] = "\n".join(buf).strip("\n")
            label, buf = f.group(1), [f.group(2)]
        elif label:
            buf.append(line)
    if label:
        fields[label] = "\n".join(buf).strip("\n")
    return meta, fields


# ── meta ─────────────────────────────────────────────────────────────────────
def partitions_of(meta_text):
    """The partition register division → [{name, where} | {name, of}], in its order."""
    div = section(meta_text, "2 · Partition Register", 4)
    m = re.search(r"```text\n(.*?)\n```", div, re.S)
    if not m:
        raise CarryError("the Partition Register has no text block")
    lines = m.group(1).split("\n")
    cols = [x.start() for x in re.finditer(r"\S+(?: \S+)*", lines[0])]
    parts, cur = [], None
    for line in lines[1:]:
        if line.lstrip().startswith("─") or not line.strip():
            continue
        name = line[:cols[1]].strip()
        pop = line[cols[1]:cols[2]].strip() if len(line) > cols[1] else ""      # this table holds no wide characters
        if name and re.fullmatch(r"[a-z][a-z0-9]*", name):
            cur = {"name": name, "pop": pop}
            parts.append(cur)
        elif cur and not name and pop.startswith("AND "):
            cur["pop"] += " " + pop
    out = []
    for p in parts:
        if p["pop"].startswith("where: []"):
            out.append({"name": p["name"], "where": []})
        elif p["pop"].startswith("no rows of its own"):
            out.append({"name": p["name"], "of": [x["name"] for x in parts if x["name"] not in ("full", p["name"])
                                                  and not x["pop"].startswith(("where: []", "no rows"))]})
        else:
            where, col = [], None
            for clause in re.split(r"\s+AND\s+", p["pop"]):
                t = clause.split()
                if len(t) == 3:
                    col, op, val = t
                elif len(t) == 2 and col:
                    op, val = t
                else:
                    raise CarryError(f"partition {p['name']}: clause {clause!r}")
                try:
                    val = float(val)
                except ValueError:
                    pass
                where.append({"column": col, op: val})
            out.append({"name": p["name"], "where": where})
    if not out or out[0]["name"] != "full":
        raise CarryError("the partition register does not start with full")
    return out, div


def thresholds_text(meta_text, project, override):
    path = Path(override) if override else None
    if path is None:
        m = re.search(r"(?m)^file\s+(\S+\.ya?ml)\b", section(meta_text, "3 · Shared Thresholds", 4))
        if not m:
            raise CarryError("the meta page names no thresholds file; pass --thresholds")
        path = project / m.group(1)
    text = path.read_text(encoding="utf-8")
    yaml.safe_load(text)
    body = re.sub(r"\A(?:#.*\n|\s*\n)*", "", text)
    return ("# thresholds.yaml · the values every question and partition of this Block shares,\n"
            "# carried word for word from the board it was made from. A question names a key here and\n"
            "# never restates a value; a key is declared before the first run that reads it.\n\n"
            + body.rstrip("\n") + "\n\n"
            "power:\n"
            "  smallest_effect_pp: null  # the one board-wide smallest effect worth acting on, in percentage points;\n"
            "                            # declared with its reason before the first run with a power rule\n")


# ── writing and checking ─────────────────────────────────────────────────────
def build(old, block, thresholds=None, dataset=None):
    """{relative path: text} of the whole Block, made from the old board alone."""
    old = Path(old).resolve()
    project = old.parents[1]
    old_rel = Path(os.path.relpath(old, Path(block).resolve()))
    meta_path = old / "0-MT-meta" / "MT00-meta" / "MT00-meta.md"
    meta_text = meta_path.read_text(encoding="utf-8")
    parts, division = partitions_of(meta_text)
    order = [p["name"] for p in parts]
    files = {}
    board = (old / "board.md").read_text(encoding="utf-8")
    keep = [section(board, t, 2) for t in ("Topic", "Replication target")]
    ds = dict([dataset.split("=", 1)]) if dataset else {}
    files["board.md"] = ("---\nboard-kind: task-block\nworkbench: insight\n"
                         + yaml.safe_dump({"datasets": ds}, sort_keys=False, default_flow_style=False)
                         + f"carried-from: {old_rel.as_posix()}\n---\n\n"
                         f"# {title_of(board)}\n\n" + "\n\n".join(k for k in keep if k) + "\n")
    content = until_heading(from_heading(meta_text, "## Opening"), "## Aims").rstrip("\n")
    files["meta/meta.md"] = f"# {title_of(meta_text)}\n\n{content}\n"
    files["meta/partitions.md"] = ("---\n" + yaml.safe_dump({"partitions": parts}, sort_keys=False,
                                                              allow_unicode=True, width=100000, default_flow_style=None)
                                     + "---\n\n" + division + "\n")
    files["meta/thresholds.yaml"] = thresholds_text(meta_text, project, thresholds)
    for reg in registers(old):
        text = reg.read_text(encoding="utf-8")
        letter = {"data": "D", "information": "I", "knowledge": "K", "wisdom": "W"}[
            re.search(r"(?m)^question-level: (\w+)", text).group(1)]
        keep = [section(text, "Opening", 2), section(text, "1 · Queue", 3), section(text, "Law", 2)]
        files[f"{LEVEL_JOB[letter][1]}/level.md"] = f"# {title_of(text)}\n\n" + "\n\n".join(k for k in keep if k) + "\n"
    for q in read_questions(old, order):
        files[f"{LEVEL_JOB[q['letter']][1]}/{q['folder']}/question.md"] = question_file(q, order, old_rel.as_posix())
    return files


def division_text(meta, prose):
    """The register division rebuilt from a question file v2 alone, as the register laid it out."""
    out = [f"**The ask**: {meta['ask']}", "", f"**Why now**: {prose.get('Why now', '')}", "",
           f"**What would answer it**: {prose.get('What would answer it', '')}"]
    for nid, n in (meta.get("needs") or {}).items():
        out += need_lines(nid, n)
    out += [f"**Needs agreed**: {meta.get('agreed', '')}"]
    if meta["source"].get("stood"):
        out += ["", f"**Where it stands**: {meta['source']['stood']}"]
    for k, v in prose.items():
        if k not in ("Why now", "What would answer it"):
            out += ["", f"**{k}**: {v}"]
    return "\n".join(out)


def old_divisions(old):
    """{old id: the division's text as the register holds it, heading dropped}."""
    out = {}
    for reg in registers(old):
        for head, lines in blocks(reg.read_text(encoding="utf-8")):
            m = DIVISION.match(head)
            if m:
                out[m.group(1)] = "\n".join(lines).strip("\n")
    return out


def compare(old, prototype):
    """Field-by-field differences between the old board and a Block carried from it: [(where, old, new)]."""
    old, prototype = Path(old).resolve(), Path(prototype).resolve()
    meta_text = (old / "0-MT-meta" / "MT00-meta" / "MT00-meta.md").read_text(encoding="utf-8")
    order = [p["name"] for p in partitions_of(meta_text)[0]]
    diffs, rows = [], []
    raw = old_divisions(old)
    for q in read_questions(old, order):
        path = prototype / LEVEL_JOB[q["letter"]][1] / q["folder"] / "question.md"
        if not path.is_file():
            diffs.append((q["old_id"], "a question file", "missing"))
            continue
        meta, prose = read_v2(path)
        f = q["fields"]
        pairs = [("question", q["question"], meta.get("question")), ("name", q["name"], meta.get("name")),
                 ("ask", f["ask"], meta.get("ask")), ("why now", f["why"], prose.get("Why now")),
                 ("what would answer it", f["answer"], prose.get("What would answer it")),
                 ("agreed", f["agreed"], meta.get("agreed")), ("gen1", q["gen1"], meta["source"].get("gen1")),
                 ("where it stands", f.get("stood"), meta["source"].get("stood")),
                 ("cells", q["cells"], meta["source"].get("cells"))]
        pairs += [(k, v, prose.get(k)) for k, v in f.items() if k not in NAMED.values()]
        new_needs = meta.get("needs") or {}
        old_ids = [m.group(1) for m, _ in q["needs"]]
        if list(new_needs) != old_ids:
            pairs.append(("need ids", old_ids, list(new_needs)))
        for m, lines in q["needs"]:
            nid = m.group(1)
            got = need_lines(nid, new_needs[nid]) if nid in new_needs else None
            pairs.append((f"{nid}", "\n".join(lines), "\n".join(got) if got else None))
        pairs.append(("division text, rebuilt", raw[q["old_id"]], division_text(meta, prose)))
        for label, a, b in pairs:
            same = a == b
            rows.append((q["old_id"], q["id"], label, same))
            if not same:
                diffs.append((f"{q['old_id']} · {label}", a, b))
    return diffs, rows


def report(old, prototype, diffs, rows):
    qs = sorted({r[0] for r in rows}, key=lambda x: ("DIKW".index(x[1]), int(x[2:])))
    lines = ["Carry-over report", "=================", "",
             f"old board: {Path(old).name} · Block: {Path(prototype).name}", "",
             f"{len(qs)} questions · {len(rows)} fields compared · {len(diffs)} differ", "",
             "```text", f"{'old':<6}{'new':<5}fields  equal  needs"]
    for oid in qs:
        rs = [r for r in rows if r[0] == oid]
        lines.append(f"{oid:<6}{rs[0][1]:<5}{len(rs):>6}  {sum(r[3] for r in rs):>5}  "
                     f"{sum(1 for r in rs if re.fullmatch(r'E\d+', r[2]))}")
    lines.append("```")
    for where, a, b in diffs:
        lines += ["", f"**{where}**", "", "```text", f"old: {a}", f"new: {b}", "```"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("old_board")
    a.add_argument("block")
    a.add_argument("--dataset", help="the Block's first dataset, <name>=<extract .parquet under the SPACE root>")
    a.add_argument("--thresholds", help="the shared thresholds file, when the meta page does not name it")
    a.add_argument("--report", help="write the side-by-side report here")
    a.add_argument("--check", action="store_true", help="compare only; write nothing but the report")
    args = a.parse_args(argv)
    proto = Path(args.block)
    if not args.check:
        if proto.exists() and any(proto.iterdir()):
            raise SystemExit(f"{proto} exists and is not empty; a carry-over never writes over a Block")
        if not args.dataset or "=" not in args.dataset:
            raise SystemExit("--dataset <name>=<parquet> names the Block's first dataset")
        files = build(args.old_board, proto, args.thresholds, args.dataset)
        for rel, text in files.items():
            path = proto / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(f"wrote {len(files)} files into {proto}")
    diffs, rows = compare(args.old_board, proto)
    if args.report:
        Path(args.report).write_text(report(args.old_board, proto, diffs, rows), encoding="utf-8")
    n_q = len({r[0] for r in rows})
    print(f"{n_q} questions · {len(rows)} fields compared · {len(diffs)} differ")
    for where, _, _ in diffs[:20]:
        print("DIFF", where)
    return 1 if diffs else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CarryError as e:
        raise SystemExit(f"carry_over: {e}")
