"""check_instance.py <instance> [--strict] [--write] · check a Prototype and one Instance of it.

ref/prototype-contract.md (haipipe-insight). Two halves:

  PROTOTYPE  every question file v2 is complete and legal: its short question, name,
             ask, Why now and What would answer it, its partitions block and power,
             its live needs and their specs, its cites one rung below, its one entry
             script (SPEC line); review suspects (Q1, Q2, Q4, Q6) are printed as notes
  INSTANCE   every question has its folder in the same rung, its scripts/ copy and
             lock, one run ticket per partition it is asked on, each run's receipt,
             the spec's files and columns, its generated report, and the question's
             page; drift between the two boards' scripts is shown

Status is computed per question x partition, never read from a register:
  —  not asked · 🚫 refused · 🟡 owed · ✅ <YYMMDD> CHECK closed and current · STALE
A trailing ⚑ marks a cell whose Instance scripts differ from the Prototype's.

--write writes the grid to the Instance's 0-Meta/status.md (generated; never edit it).
Exit 1 on any problem; with --strict, also on any 🟡, STALE or waiting Prototype update.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2] / "haipipe-insight" / "ref"))
from check_evidence import CAUSAL  # noqa: E402
from run_question import (META, QFOLDER, RUNG_DIR, GateError, asked_partitions, entry_script,  # noqa: E402
                          expected_outputs, front, live_needs, question_folders, sha256, shared_digest, shared_paths)
from scaffold_instance import TICKET  # noqa: E402
from sync_instance import status as sync_status  # noqa: E402

NEED_ID = re.compile(r"\b[DIKW]\d{2}\.E\d+\b")
RUNG = {"data": "D", "information": "I", "knowledge": "K", "wisdom": "W"}
ORDER = "DIKW"
KINDS_AT = {"D": {"compute"}, "I": {"compute", "cite"}, "K": {"compute", "cite", "judge"}, "W": {"cite", "judge"}}
SPEC = ("what", "pass", "cut", "unit", "measure", "by", "uncertainty", "rivals", "output")
JOINED = re.compile(r",? (?:and|or) (?:what|which|how|does|do|is|are|why|when|whether|who)\b", re.I)
TESTS = ("rate_precision", "two_proportion", "script")
AGREED = re.compile(r"^(⬜|✅ \d{6})$")
REALIZES = re.compile(r"<!-- realizes: (C\d+\.P\d+\.B\d+) -->")
ITEM = re.compile(r"^### (E\d+-[A-Z]+-[\w-]+) · (C\d+\.P\d+\.B\d+)", re.M)


# ── the Prototype ────────────────────────────────────────────────────────────
def load_questions(prototype):
    qs, dup = {}, []
    for qdir in question_folders(prototype):
        qfile = qdir / f"{qdir.name}.md"
        try:
            meta, prose = front(qfile) if qfile.is_file() else (None, "")
        except Exception as e:  # noqa: BLE001
            meta, prose = {"_error": str(e)}, ""
        if isinstance(meta, dict):
            meta["_prose"] = prose
        qid = qdir.name[:3]
        if qid in qs:
            dup.append(f"{qdir.name}: id {qid} is also {qs[qid][0].name}; an id is used once")
        qs[qid] = (qdir, meta)
    return qs, dup


def misplaced(board):
    """Question folders outside the rung folder of their letter."""
    board = Path(board)
    out = [d for d in board.iterdir() if d.is_dir() and QFOLDER.match(d.name)]
    for letter, rung in RUNG_DIR.items():
        if (board / rung).is_dir():
            out += [d for d in (board / rung).iterdir()
                    if d.is_dir() and d.name != "src" and not (QFOLDER.match(d.name) and d.name[0] == letter)]
    return out


def check_question(qid, qdir, q, qs, thresholds, partitions, prose=""):
    """(problems, notes) for one question file v2. A problem breaks the contract; a note is a
    question-review suspect (Q1 one thing, Q2 logic, Q4 rung) for haipipe-insight-question GI1."""
    p, notes = [], []
    letter = qid[0]
    if q is None:
        return [f"{qid}: no {qdir.name}.md"], notes
    if "_error" in q:
        return [f"{qid}: {q['_error']}"], notes
    if q.get("id") != qid:
        p.append(f"{qid}: id is {q.get('id')!r}, not {qid}, the start of its folder name")
    if RUNG.get(q.get("rung")) != letter:
        p.append(f"{qid}: rung {q.get('rung')!r} is not the letter {letter}")
    if q.get("retired"):                                   # history: kept word for word, never run or cited
        succ = q.get("superseded_by")
        if not isinstance(succ, list):
            p.append(f"{qid}: a retired question names its successors (superseded_by: [<id>, …], or [])")
        for sid in succ or []:
            if sid not in qs:
                p.append(f"{qid}: superseded_by {sid}, which the Prototype does not hold")
        if any(qdir.glob("scripts/*.py")):
            p.append(f"{qid}: a retired question keeps no scripts/")
        return p, notes
    for k in ("question", "name", "ask"):
        if not str(q.get(k) or "").strip():
            p.append(f"{qid}: no {k} (the short question, its name, the ask)")
    ask = (q.get("ask") or "").strip()
    for label in ("Why now", "What would answer it"):
        if not re.search(rf"(?m)^\*\*{label}\*\*: \S", prose):
            p.append(f"{qid}: the file's prose has no **{label}**")
    if letter in "DI" and CAUSAL.search(ask):
        notes.append(f"{qid}: Q4 rung · a {letter} ask uses a cause word ('{CAUSAL.search(ask).group(0)}')")
    if len(re.findall(JOINED, ask)) + ask.count("?") - 1 > 0:
        notes.append(f"{qid}: Q1 one thing · the ask joins more than one question")
    if not AGREED.match(str(q.get("agreed", ""))):
        p.append(f"{qid}: agreed is ⬜ or ✅ <YYMMDD>")
    pb = q.get("partitions") or {}
    names = [x["name"] for x in partitions]
    asked = pb.get("asked")
    if asked not in ("all", "cross") and not (isinstance(asked, list) and asked and set(asked) <= set(names) - {"cross"}):
        p.append(f"{qid}: partitions.asked is all, cross, or a list of partitions.md names")
    if asked != "all" and not pb.get("not_elsewhere"):
        p.append(f"{qid}: partitions.not_elsewhere says why it is not asked on every partition")
    pw = pb.get("power", "none")
    if isinstance(pw, dict):
        if pw.get("test") not in TESTS:
            p.append(f"{qid}: power.test is one of {', '.join(TESTS)}")
        if pw.get("test") in ("rate_precision", "two_proportion"):
            if pw.get("effect") is None and (thresholds.get("power") or {}).get("smallest_effect_pp") is None:
                p.append(f"{qid}: no smallest effect: declare {META}/thresholds.yaml power.smallest_effect_pp "
                         f"or the question's power.effect")
            if pw.get("effect") is not None and not pw.get("effect_reason"):
                p.append(f"{qid}: power.effect overrides the board-wide effect, so power.effect_reason says why")
            if not pw.get("outcome"):
                p.append(f"{qid}: power.outcome names the base rate's column")
            if pw.get("test") == "two_proportion" and not pw.get("groups"):
                p.append(f"{qid}: power.groups names the compared column")
    elif pw != "none":
        p.append(f"{qid}: partitions.power is none or a power rule")
    needs = q.get("needs") or {}
    live = live_needs(q)
    if not live:
        p.append(f"{qid}: no live needs")
    csv_cols = {}
    for nid, n in needs.items():
        full = f"{qid}.{nid}"
        if not re.fullmatch(r"E\d+", str(nid)):
            p.append(f"{full}: a need id is E<n>")
        kind = n.get("kind")
        if not n.get("what"):
            p.append(f"{full}: a need says what it is")
        if nid not in live:
            continue                                         # a retired need is history: kept, never run or cited
        if kind not in KINDS_AT[letter]:
            p.append(f"{full}: a {kind} need is not legal at rung {letter}")
        if kind == "compute":
            for k in SPEC:
                if not n.get(k):
                    p.append(f"{full}: spec lacks {k}")
            out = n.get("output")
            if out is not None and not (isinstance(out, dict) and all(
                    re.fullmatch(r"[\w.-]+\.(csv|json)", f) and isinstance(c, list) and c for f, c in out.items())):
                p.append(f"{full}: output maps each <file>.csv|json to its column list")
            for f, cols in (out or {}).items() if isinstance(out, dict) else []:
                if f.endswith(".csv"):
                    if f in csv_cols and csv_cols[f][1] != cols:
                        p.append(f"{full}: {f} is also {qid}.{csv_cols[f][0]}'s, with other columns")
                    csv_cols.setdefault(f, (nid, cols))
        elif kind == "cite":
            src = str(n.get("from", ""))
            if not NEED_ID.fullmatch(src):
                p.append(f"{full}: cite from is <L><NN>.E<n>")
            else:
                sq, sn = src.split(".")
                target = qs.get(sq, (None, None))[1]
                if not target or "_error" in target or sn not in (target.get("needs") or {}):
                    p.append(f"{full}: cites {src}, which the Prototype does not hold")
                elif target["needs"][sn].get("retired") or target.get("retired"):
                    p.append(f"{full}: cites {src}, which is retired")
                else:
                    gap = ORDER.index(letter) - ORDER.index(sq[0])
                    if not (gap == 1 or (gap == 0 and asked == "cross")):
                        p.append(f"{full}: cites {sq}, not one rung below (the same rung only from a cross question)")
        elif kind == "judge":
            reads = n.get("from") or []
            for f in reads if isinstance(reads, list) else [reads]:
                if str(f) in needs and str(f) not in live:
                    p.append(f"{full}: judges from {f}, which is retired")
                elif not (str(f) in live or NEED_ID.fullmatch(str(f))):
                    p.append(f"{full}: judges from {f}, not a need")
            if not reads:
                p.append(f"{full}: a judge names what it reads")
    if letter in "KW":
        read = {str(f) for n in live.values() if n.get("kind") == "judge"
                for f in (n.get("from") if isinstance(n.get("from"), list) else [n.get("from")])}
        idle = [nid for nid, n in live.items() if n.get("kind") != "judge" and nid not in read]
        if idle and any(n.get("kind") == "judge" for n in live.values()):
            notes.append(f"{qid}: Q2 logic · no judge reads {', '.join(idle)}")
    for phrase, to in (q.get("ask_covered") or {}).items():
        if phrase.lower() not in ask.lower():
            p.append(f"{qid}: ask_covered phrase '{phrase}' is not in the ask")
        for nid in (to if isinstance(to, list) else []):
            if nid not in live:
                p.append(f"{qid}: '{phrase}' maps to {nid}, not a live need")
    has_compute = any(n.get("kind") == "compute" for n in live.values())
    scripts = qdir / "scripts"
    if has_compute:
        try:
            entry_script(scripts, qid)
        except GateError as e:
            p.append(f"{qid}: {e}")
    elif scripts.is_dir() and any(scripts.glob("*.py")):
        p.append(f"{qid}: a question without compute needs has no scripts/")
    if any(qdir.glob("*.py")):
        p.append(f"{qid}: scripts sit in {qdir.name}/scripts/, not beside the question file")
    return p, notes


def same_tables(qs):
    """Q6 new: two questions whose live needs compute the same table (file and columns)."""
    seen, notes = {}, []
    for qid, (_, q) in qs.items():
        for nid, n in live_needs(q or {}).items() if q and "_error" not in q else []:  # retired questions have none
            for f, cols in (n.get("output") or {}).items() if n.get("kind") == "compute" else []:
                key = (f, tuple(cols))
                if key in seen and seen[key][0] != qid:
                    notes.append(f"{qid}.{nid}: Q6 new · computes {f} as {seen[key][0]}.{seen[key][1]} does")
                seen.setdefault(key, (qid, nid))
    return notes


# ── the page ─────────────────────────────────────────────────────────────────
def page_cites(qfolder):
    """The need ids the question's page cites, and each need's Evidence Item artifacts."""
    md = qfolder / f"{qfolder.name}.md"
    text = md.read_text(encoding="utf-8") if md.is_file() else ""
    realized = set(REALIZES.findall(text))
    cited, artifacts = set(), {}
    items = qfolder / "draft" / f"{qfolder.name}-evidence-items.md"
    if items.is_file():
        body = items.read_text(encoding="utf-8")
        heads = list(ITEM.finditer(body))
        for i, h in enumerate(heads):
            chunk = body[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(body)]
            need = re.search(r"\*\*Need\*\*:\s*(.+)", chunk)
            art = re.search(r"\*\*Artifact\*\*:\s*`([^`]+)`", chunk)
            for nid in NEED_ID.findall(need.group(1))[:1] if need else []:   # a cite item reads "<own> ← <cited>"
                if art:
                    artifacts.setdefault(nid, set()).add(art.group(1))
                if h.group(2) in realized:
                    cited.add(nid)
    plans = sorted((qfolder / "draft").glob(f"{qfolder.name}-draft-v*.md")) if (qfolder / "draft").is_dir() else []
    for plan in plans[-1:]:
        para = bullet = None
        for line in plan.read_text(encoding="utf-8").splitlines():
            ph = re.match(r"^### (C\d+\.P\d+)\b", line)
            if ph:
                para, bullet = ph.group(1), None
                continue
            b = re.match(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·", line)
            if b and para:
                bullet = f"{para}.B{b.group(1)}"
                continue
            j = re.match(r"^\s+Evidence:\s*none\s*·\s*judge\s+(" + NEED_ID.pattern + ")", line)
            if j and bullet in realized:
                cited.add(j.group(1))
    return text, cited, artifacts


def utc(v):
    t = pd.Timestamp(str(v))
    return t.tz_convert("UTC") if t.tzinfo else t.tz_localize("UTC")


def last_check(qfolder):
    """The latest closed page CHECK run: (closed_at, verdict) or None."""
    best = None
    for f in sorted((qfolder / "runs").glob("run-check-*.md")):
        try:
            meta, body = front(f)
        except Exception:  # noqa: BLE001
            continue
        if meta.get("status") != "closed" or not meta.get("closed_at"):
            continue
        v = re.search(r"VERDICT:\s*([A-Z]+)", body)
        at = utc(meta["closed_at"])
        if best is None or at > best[0]:
            best = (at, v.group(1) if v else "")
    return best


# ── one question in the Instance ─────────────────────────────────────────────
def check_partition(qf, qid, q, pq, part, shared, page):
    """(mark, problems) for one asked question x partition."""
    p = []
    ticket = qf / "runs" / f"{part}.sh"
    if not ticket.is_file() or ticket.read_text() != TICKET:
        p.append(f"{qf.name}: runs/{part}.sh is missing or not the standard ticket")
    rec_path = qf / "results" / part / "runtime.yaml"
    if not rec_path.is_file():
        return "🟡", p
    rec = yaml.safe_load(rec_path.read_text()) or {}
    status = rec.get("status")
    if status == "failed":
        return "🟡", p + [f"{qf.name} · {part}: its run failed · {rec.get('problem')}"]
    if status not in ("ok", "refused"):
        return "🟡", p + [f"{qf.name} · {part}: its run is {status}"]
    if not (qf / "reports" / part / "report.md").is_file():
        p.append(f"{qf.name} · {part}: no generated report in reports/{part}/")
    if str(q.get("agreed", "")).startswith("⬜"):
        p.append(f"{qf.name} · {part}: ran before {qid}'s needs were agreed")
    stale = (rec.get("spec_sha256") != sha256(pq / f"{pq.name}.md")
             or rec.get("scripts_sha256") != sha256(qf / "scripts")
             or rec.get("shared_sha256") != shared_digest(pq.parent.parent, pq.parent.name, qf / "scripts", q))
    if stale:
        return "STALE", p
    if status == "refused":
        return f"🚫 {rec.get('reason', '')}".strip(), p
    for f, cols in expected_outputs(q).items():
        path = qf / "results" / part / f
        if not path.is_file():
            p.append(f"{qf.name} · {part}: result lacks {f}")
        elif f.endswith(".csv") and list(pd.read_csv(path, nrows=0).columns) != cols:
            p.append(f"{qf.name} · {part}: {f} columns differ from the spec")
    text, cited, artifacts, hdr, chk = page
    if not text:
        return "🟡", p
    ended = utc(rec["ended"])
    if not hdr.get("results-read") or utc(hdr["results-read"]) < ended:
        return "🟡", p
    reads_part = any(f"results/{part}/" in a or f"reports/{part}/" in a for arts in artifacts.values() for a in arts)
    if not reads_part:
        p.append(f"{qf.name}: the page cites nothing of partition {part}")
    if chk and chk[1] == "CLOSE" and chk[0] > ended and not p:
        return f"✅ {chk[0].strftime('%y%m%d')}", p
    return "🟡", p


def page_state(qf, qid, q):
    """The question page's text, citations, header and latest CHECK, plus page-level problems."""
    text, cited, artifacts = page_cites(qf)
    hdr = dict(re.findall(r"^([a-z][a-z-]*):\s*(.*?)\s*$", text.split("\n## ", 1)[0], re.M)) if text else {}
    p = []
    if text:
        for nid, n in live_needs(q).items():
            full = f"{qid}.{nid}"
            if full not in cited:
                p.append(f"{qf.name}: the page does not cite {full}")
            if n.get("kind") == "cite":
                for a in artifacts.get(full, ()):
                    if not (qf / a).resolve().is_file():
                        p.append(f"{qf.name}: {full} reads {a}, which does not exist")
    return (text, cited, artifacts, hdr, last_check(qf)), p


def run(instance, strict=False):
    instance = Path(instance).resolve()
    meta, _ = front(instance / "board.md")
    problems, notes = [], []
    if meta.get("board-kind") != "insight-instance":
        return ["board.md is not board-kind: insight-instance"], {}, []
    prototype = (instance / meta["prototype"]).resolve()
    if front(prototype / "board.md")[0].get("board-kind") != "insight-prototype":
        problems.append(f"{prototype.name}/board.md is not board-kind: insight-prototype")
    partitions = front(prototype / META / "partitions.md")[0]["partitions"]
    names = [x["name"] for x in partitions]
    if names[:1] != ["full"]:
        problems.append(f"{META}/partitions.md: the first partition is full, unfiltered")
    if not str(meta.get("extract", "")).endswith(".parquet"):
        problems.append("board.md: extract names a .parquet under the SPACE root")
    tfile = prototype / META / "thresholds.yaml"
    thresholds = (yaml.safe_load(tfile.read_text()) or {}) if tfile.is_file() else {}
    qs, dup = load_questions(prototype)
    problems += dup
    for board in (prototype, instance):
        problems += [f"{board.name}/{d.relative_to(board)}: a question folder is <L><NN>-<name> in the rung "
                     f"folder of its letter" for d in misplaced(board)]
    for qid, (qdir, q) in qs.items():
        qp, qn = check_question(qid, qdir, q, qs, thresholds, partitions, (q or {}).get("_prose", ""))
        problems += qp
        notes += qn
    notes += same_tables(qs)
    drift = {}
    for qf, name, st, reviewed in sync_status(instance):
        if st == "in sync":
            continue
        drift.setdefault(qf.name, []).append(st)
        if st == "instance changed" and not reviewed:
            problems.append(f"{qf.name}/scripts/{name}: changed in the Instance and not reviewed "
                            f"(sync_instance.py --reviewed {name} after an independent review)")
        elif st == "both changed":
            problems.append(f"{qf.name}/scripts/{name}: changed in both boards; merge, then "
                            f"sync_instance.py --pull --keep-instance")
        elif st in ("prototype changed", "new in prototype"):
            notes.append(f"{qf.name}/scripts/{name}: {st}; sync_instance.py --pull, then rerun")
        elif st == "only in instance":
            notes.append(f"{qf.name}/scripts/{name}: only in the Instance")
    grid, wanted = {}, set()
    for qid, (pq, q) in qs.items():
        if not q or "_error" in q:
            continue
        qf = instance / pq.parent.name / pq.name
        wanted.add(qf)
        asked = asked_partitions(q, partitions)
        has_compute = any(n.get("kind") == "compute" for n in live_needs(q).values())
        if has_compute and not (qf / "scripts" / "prototype.lock").is_file():
            problems.append(f"{pq.parent.name}/{qf.name}: no scripts/ copy with its prototype.lock "
                            f"(run scaffold_instance.py)")
        page, pp = page_state(qf, qid, q) if qf.is_dir() else (("", set(), {}, {}, None), [])
        problems += pp
        shared = shared_paths(prototype, pq.parent.name, qf / "scripts")
        row = {}
        for name in names:
            if name not in asked:
                row[name] = "—"
                if (qf / "runs" / f"{name}.sh").exists():
                    problems.append(f"{qf.name}: runs/{name}.sh, but the Prototype does not ask {qid} on {name}")
                continue
            if not has_compute:                                   # a Wisdom question: the page alone
                text, _, _, hdr, chk = page
                row[name] = f"✅ {chk[0].strftime('%y%m%d')}" if text and chk and chk[1] == "CLOSE" and not pp else "🟡"
                continue
            mark, p = check_partition(qf, qid, q, pq, name, shared, page) if qf.is_dir() else ("🟡", [])
            problems += p
            row[name] = mark + (" ⚑" if qf.name in drift else "")
        grid[qid] = row
    for rung in RUNG_DIR.values():
        for d in (instance / rung).glob("[DIKW][0-9][0-9]-*") if (instance / rung).is_dir() else []:
            if d.is_dir() and d not in wanted:
                problems.append(f"{rung}/{d.name}: the Prototype has no such question")
    if strict:
        problems += [f"{qid} · {n}: {m}" for qid, row in grid.items() for n, m in row.items()
                     if m.startswith("🟡") or m.startswith("STALE")]
        problems += [f"update waiting: {x}" for x in notes if "pull" in x]
    return problems, grid, notes


def render(grid, names):
    w = max([len(q) for q in grid] + [3])
    lines = [" " * w + "  " + "  ".join(f"{n:<14}" for n in names)]
    lines += [f"{qid:<{w}}  " + "  ".join(f"{row[n][:14]:<14}" for n in names) for qid, row in grid.items()]
    return lines


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("instance")
    a.add_argument("--strict", action="store_true")
    a.add_argument("--write", action="store_true", help="write the grid to <instance>/0-Meta/status.md")
    args = a.parse_args(argv)
    problems, grid, notes = run(args.instance, args.strict)
    names = list(next(iter(grid.values()))) if grid else []
    table = render(grid, names) if grid else []
    print("\n".join(table))
    for x in notes:
        print("NOTE   ", x)
    for x in problems:
        print("PROBLEM", x)
    cells = [m for row in grid.values() for m in row.values() if m != "—"]
    summary = (f"{len(grid)} questions · {len(cells)} asked cells · {sum(m.startswith('✅') for m in cells)} ✅ · "
               f"{sum(m.startswith('🚫') for m in cells)} 🚫 · {sum(m.startswith('🟡') for m in cells)} 🟡 · "
               f"{sum(m.startswith('STALE') for m in cells)} STALE · {sum('⚑' in m for m in cells)} ⚑ · "
               f"{len(problems)} problems")
    print(summary)
    if args.write:
        out = Path(args.instance) / META / "status.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.write_text("# Status · computed by haipipe-insight-check ref/check_instance.py; never edit by hand\n\n"
                       f"checked: {now}\n\n```text\n" + "\n".join(table) + f"\n```\n\n{summary}\n"
                       + ("\n" + "\n".join(f"- {x}" for x in problems) + "\n" if problems else ""), encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
