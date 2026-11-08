"""values_ledger.py · every number a paper prints, as one ledger: a catalog of values, bindings to the text, a check.

    python values_ledger.py run   <value Task> <result dir>   one value Task's Run (its ticket calls this)
    python values_ledger.py check <j02 Job> <result dir>      the paper-wide Run (t99_paper_value_check)
    python values_ledger.py bind  <j02 Job>                   say which bindings the search would seed (writes nothing)
    python values_ledger.py bind  <j02 Job> --propose         write them to each Section's evidence/proposals.md
    python values_ledger.py bind  <j02 Job> --adopt           write the ticked ones as card items; then fixed
    python values_ledger.py bind  <j02 Job> --confirm [tNN_<section> ...]   an agent confirms them all (no ticks)

One engine for the two shapes a paper ledger had (haipipe-paper-evidence 0.7.0; JL 261103: "how do you think you can
unify them together"): printed-first (each printed number bound by hand to its value, so a wrong number is caught) and
value-first (each value searched for in the text and the displays, with no hand binding). Three layers:

1. Catalog. A value Task of the Board's `j02_evidence_value` keeps one value map, `tNN_/scripts/value_map.yaml`:

       rq: RQ1                         the research question every value of the map answers
       group: the main association     what the group of numbers is, in words
       writing: j11_writing_v1130_desk the writing Job checked (default: the Board's newest)
       defaults: {file: values.csv, column: value}
       runs: {main: work/b90_x/j01_y/t01_z/runs/r01_w}      short name -> a Project-relative work Run folder
       values:
         main.b:  {what: '<outcome>: difference', run: main, where: {key: main.b}, digits: 2}
         main.p:  {what: '<outcome>: P value', run: main, where: {key: main.p}, digits: 3, p: true}
       needs:   {late.b: {what: ..., printed: '4.1', section: t03_results, sentence: '7', why: 'waits for its Run'}}

   Per value: `what`, `run` (a name or a list), `file`, `where`/`where_not` (row filter) with `column`, or `key` (a dotted
   .json/.yaml key), or `expr`; `const`, `agg` (one, range, min, max, sum, count, maxabs, mean), `parse` (count, pct,
   regex:), `scale` (100 for a share printed as a percent), `digits`, `unit`, `format` (date, plain), `p: true` (a P
   value: matched only after "P =" or "P <"), `pending: <why>` (printed as it stands, waits for a Run; its result file need not exist yet), `id`, `note`,
   `section`, `row`, `col`. Each value gets the id `<RQ>-<tNN>-<nnn>` (or its own `id:`) and `checks:`, its lineage:
   the work Run that computed it, then the Runs that Run read, from the `source` column of its values.csv row: a key of
   the work Block's `src/inputs.yaml` `runs:` (address, path, label), a `typed:"<file>"` stand-in (a screen read,
   labelled by `typed:`), or a bNN.jNN.tNN.rNN address. `linked` is false for a value with no Run on disk;
   `screen_read` is true when its chain holds a typed stand-in; both block a printed value (evidence_ledger.py).

2. Bindings. A binding is a VALUE card item in haipipe-evidence's format (cards.py, 0.9.0), in the Section's
   `evidence/cards.yaml`: the card `source: j02.tNN`, the item `run: r01, for: [<sentence id>], value: <its id>,
   anchor: [<the printed words>]` (an older item may say `file: values.yaml, key: values.<key>.value` instead of
   `value:`); a display's item says `display: <name>` and `printed: [...]` instead of `for`/`anchor` (in the Section
   that frames the unit, or the display Task's own `evidence/cards.yaml`). Nobody types them: `bind --propose` adds a
   line per search hit to the holder's `evidence/proposals.md` (cards.bind_proposals, the "Proposing what to make"
   path); a person ticks it once and `bind --adopt` writes it (or an agent confirms with `bind --confirm`); a written
   binding is never rewritten by the search. A sentence id is a draft S id (`5`, the `## 3 · Draft` line
   `- B<n> · S5 · ...`) or a `## Content` `<!-- realizes: <id> -->` id (paper_text.py).

3. Check. Each binding: match (the anchor is in its sentence and its number is the value at the printed precision),
   differs (the anchor is there, the number is not the value's), missing (the anchor's words left the sentence), no
   anchor (the sentence restates the value without a number), owed (a `need`, or the map's `needs:`), pending (the
   value waits for a Run; the check says what it would be), stale (the bound key is in no value map). Two reverse
   lists: values never printed (no binding, no search hit), and, in the paper-wide check, numbers printed with no
   binding (candidates for an owed value). A search hit not bound yet shows as `found`. The statuses are
   haipipe-evidence's cards.item_status (exact half-up rounding at the printed precision), so the check is written once.

The Run writes values.yaml (`values.<key>.value` for cards; ids, checks, places, statuses), ledger.csv, values.html
(the ledger: ID · Where · Printed · Value · Status · Source and key) and headline.txt. No model call, no raw data, no
content hash; never edit a result, rerun the ticket.
"""
from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import re
import sys
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from html import escape as esc
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(next(p for p in HERE.parents if p.name == "skills") / "1_base/evidence/haipipe-evidence/scripts"))
import paper_text as pt  # noqa: E402
import cards  # noqa: E402   haipipe-evidence: tokens, same, agrees, item_status, lineage, bind_proposals, adopt_bindings

# a value Task's Run reads and checks; it is never named rNN_collect_* (that name is a question form's, haipipe-interaction:
# r02 found r01_collect_values listed under 🙋 Interaction as a form "not sent yet")
RUN = "r01_read_values"
OLD_RUNS = ("r01_collect_values",)
CHECK_TASK = "t99_paper_value_check"
CHECK_RUN = "r01_check_values"
GEN = "# GENERATED by haipipe-paper-evidence scripts/values_ledger.py from {src}; rerun the ticket, never edit this file.\n"
STATUSES = ("differs", "missing", "stale", "owed", "pending", "match", "no anchor", "found")
# each status in the words the workbench prints (servers/workbench-paper evidence_read.VALUE_WORDS), so the page and its
# pop-out say the same thing (r02: the pop-out kept "1 owed", "2 found" beside "1 waits for its Run")
WORDS = {"match": "match", "differs": "differs from its Run", "owed": "waits for its Run", "found": "found, not bound yet",
         "missing": "missing from its Run", "stale": "its Run changed", "pending": "waits for its Run",
         "no anchor": "its sentence moved"}


def said(c):
    """The counts in words, in STATUSES order: '1 differs from its Run, 6 match' ('1 matches' for one)."""
    return ", ".join(f"{c[s]} {'matches' if s == 'match' and c[s] == 1 else WORDS[s]}" for s in STATUSES if c[s])
DISPLAY_WORDS = ("Table", "Figure", "eTable", "eFigure", "Display", "Extended", "Supplementary")


# ════════════════════════════════════════════ 1 · catalog ════════════════════════════════════════════════════════════
def number(x):
    if isinstance(x, (int, float)) or x is None:
        return x
    s = str(x).strip().replace(",", "")
    for cast in (int, float):
        try:
            return cast(s)
        except ValueError:
            pass
    return str(x).strip()


def parse_cell(x, how):
    if not how:
        return number(x)
    s = str(x)
    if how == "count":
        return number(re.match(r"\s*([\d,.]+)", s)[1])
    if how == "pct":
        return float(re.search(r"\(([\d.]+)%\)", s)[1]) / 100
    if how.startswith("regex:"):
        return number(re.search(how[6:], s)[1])
    raise SystemExit(f"parse: {how} is count, pct or regex:<pattern>")


def match_row(row, where, where_not=None):
    for want, keep in ((where or {}, True), (where_not or {}, False)):
        for col, w in want.items():
            ws = [str(v) for v in (w if isinstance(w, list) else [w])]
            if (str(row.get(col, "")).strip() in ws) != keep:
                return False
    return True


def dotted(data, key):
    count = re.fullmatch(r"len\((.+)\)", key.strip())
    for part in (count[1] if count else key).split("."):
        data = data[int(part)] if isinstance(data, list) else data[part]
    return len(data) if count else data


SAFE = {"abs": abs, "min": min, "max": max, "round": round, "len": len, "int": int, "float": float, "sum": sum, "math": math}


def evaluate(expr, names):
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Lambda)) or (isinstance(node, ast.Attribute) and node.attr.startswith("_")):
            raise SystemExit(f"expr {expr!r}: only arithmetic over columns")
    return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}, **SAFE, **names})


def extend(found, v):
    if isinstance(v, dict):
        v = list(v.values())
    if isinstance(v, list):
        found.extend(number(x) for x in v)
    else:
        found.append(number(v))


def read_one(spec, runs, project, consts):
    names = spec["run"] if isinstance(spec["run"], list) else [spec["run"]]
    found = []
    for name in names:
        path = project / runs[name] / "result" / spec["file"]
        if path.suffix in (".json", ".yaml", ".yml"):
            text = path.read_text(encoding="utf-8")
            data = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
            extend(found, dotted(data, spec["key"]) if "key" in spec else evaluate(spec["expr"], {**data, **consts}))
            continue
        rows = [r for r in pt.rows_of(path) if match_row(r, spec.get("where"), spec.get("where_not"))]
        if not rows:
            raise SystemExit(f"{spec.get('_key')}: no row of {path} matches {spec.get('where')}")
        for r in rows:
            if "expr" in spec:
                cols = {re.sub(r"\W", "_", k): number(v) for k, v in r.items()}
                if any(cols.get(c) == "" for c in re.findall(r"[A-Za-z_]\w*", spec["expr"])):
                    continue
                extend(found, evaluate(spec["expr"], {**cols, **consts}))
            elif str(r.get(spec["column"], "")).strip() != "":
                found.append(parse_cell(r[spec["column"]], spec.get("parse")))
    return found


def aggregate(found, how):
    nums = [x for x in found if isinstance(x, (int, float))]
    if how == "one":
        if len(found) != 1:
            raise SystemExit(f"agg one: {len(found)} values {found[:6]}; give `where` or an agg")
        return found[0]
    if how == "count":
        return len(found)
    if how == "range":
        return [min(nums), max(nums)]
    if how == "maxabs":
        return max(abs(x) for x in nums)
    return {"min": min, "max": max, "sum": sum, "mean": lambda v: sum(v) / len(v)}[how](nums)


def rounded(x, digits):
    q = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f"{q:,.{digits}f}" if digits else f"{int(q):,}"


def show(value, spec):
    """The value as the paper prints it."""
    if spec.get("format") == "plain":
        return str(value)
    if isinstance(value, str):
        if spec.get("format") == "date":
            y, m, d = value.split("-")
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                      "October", "November", "December"]
            return f"{months[int(m) - 1]} {int(d)}, {y}"
        return value
    scale = spec.get("scale", 1)
    digits = spec.get("digits", 1 if scale == 100 else None)
    unit = spec.get("unit", "")

    def one(x):
        if isinstance(x, int) and scale == 1 and digits in (None, 0):
            return f"{x:,}"
        x = x * scale
        if digits is None:
            return f"{x:,}" if isinstance(x, int) else f"{x:g}"
        return rounded(x, digits)
    if isinstance(value, list):
        return f"{one(value[0])}{unit} to {one(value[1])}{unit}" if unit == "%" else f"{one(value[0])} to {one(value[1])}{unit}"
    return f"{one(value)}{unit}"


def lineage(run_dir, spec, project, root):
    """haipipe-evidence's cards.lineage, each check's folder given relative to the SPACE root."""
    chain, has_source = cards.lineage(run_dir, spec["file"], spec.get("where"), project)
    out = []
    for c in chain:
        row = {"address": c["address"], "path": _rel(c["folder"], root) if c.get("folder") else "", "name": c["name"]}
        if c.get("typed"):
            row["typed"] = True
        out.append(row)
    return out, has_source


def _rel(folder, root):
    try:
        return Path(folder).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return Path(folder).as_posix()


def load_map(task):
    f = task / "scripts" / "value_map.yaml"
    if not f.is_file():
        raise SystemExit(f"{task}: no scripts/value_map.yaml")
    return yaml.safe_load(f.read_text(encoding="utf-8")) or {}


def catalog(task):
    """(map, {key: row}) for one value Task: each value read from its work Run, with its id and its lineage."""
    project, root = pt.project_root(task), pt.server_root(task)
    vmap = load_map(task)
    runs = vmap.get("runs") or {}
    rq = vmap.get("rq", "")
    tnn = task.name.split("_")[0]
    values = {}
    for n, (key, spec) in enumerate((vmap.get("values") or {}).items(), 1):
        spec = {**(vmap.get("defaults") or {}), **(spec or {}), "_key": key}
        row = {"id": spec.get("id") or f"{rq or 'V'}-{tnn}-{n:03d}", "rq": rq, "what": spec.get("what", key)}
        if "run" not in spec:                                    # a value typed into the map: printed, but unlinked
            value = spec.get("value")
            row.update(value=value, shown=show(value, spec) if value is not None else "", checks=[], linked=False,
                       screen_read=False, note="no Run: typed into the value map")
        elif spec.get("pending") and not all((project / runs[x] / "result" / spec["file"]).is_file()
                                             for x in (spec["run"] if isinstance(spec["run"], list) else [spec["run"]])):
            row.update(value=None, shown="", checks=[], linked=False, screen_read=False, file=spec["file"])   # waits for its Run
        else:
            consts = {c: aggregate(read_one(dict(cs, _key=key), runs, project, {}), "one")
                      for c, cs in (spec.get("const") or {}).items()}
            value = aggregate(read_one(spec, runs, project, consts), spec.get("agg", "one"))
            names = spec["run"] if isinstance(spec["run"], list) else [spec["run"]]
            run_dir = project / runs[names[0]]
            chain, has_source = lineage(run_dir, spec, project, root)
            checks = [{"address": pt.address_of(run_dir), "path": _rel(run_dir, root),
                       "name": "computed in " + pt.task_title(run_dir)}] + chain
            row.update(value=value, shown=show(value, spec), checks=checks, linked=run_dir.is_dir(),
                       screen_read=any(c.get("typed") for c in checks),
                       source=[f"{runs[x]}/result" for x in names] if len(names) > 1 else f"{runs[names[0]]}/result",
                       file=spec["file"])
            if has_source is False:
                row["no_source_column"] = True                  # its values.csv keeps no `source`: the chain stops here
        for k in ("column", "key", "expr", "where", "agg", "parse", "note", "section", "row", "col", "pending", "scale", "p"):
            if spec.get(k) is not None and k not in row:
                row[k] = spec[k]
        row["_spec"] = spec
        values[key] = row
    return vmap, values


# ════════════════════════════════════════════ the finder (seeds bindings) ════════════════════════════════════════════
tokens, same, agrees = cards.tokens, cards.same, cards.agrees


def is_p(key, row):
    return bool(row["_spec"].get("p")) or key.endswith(".p")


def after_p(before):
    b = before.rstrip()
    return bool(re.search(r"\b[Pp]\s*[=<>]?\s*$", b))


def places(job, board):
    """Every place a number is printed: [(where, section, sid, text, display or None)]."""
    out = []
    for sec in pt.sections(job) if job else []:
        for s in pt.printed(sec):
            out.append((pt.where_of(sec.name, s["id"]), sec.name, s["id"], s["text"], None))
    for d in pt.displays(board, job):
        for r in d["rows"]:
            out.append((d["name"], d["holder"].name, "", r, d))
    return out


def drawn_from(d, row):
    """A display hit stands only when the display names what it was drawn from and that shares a Run with the value
    (or it names nothing, so it cannot be held to one)."""
    if d is None or not d["sources"].strip():
        return True
    for c in row.get("checks") or []:
        parts = Path(c.get("path", "")).parts
        tail = "/".join(parts[-3:]) if len(parts) >= 3 else c.get("path", "")
        if (tail and tail in d["sources"]) or (c.get("address") and c["address"] in d["sources"]):
            return True
    return False


def find(values, where_list):
    """{key: [hit]}: where each value is printed. A hit is {where, section, sid, display, printed, anchor}. Guards: a P
    only after "P =" or "P <"; a bare one-digit whole number never; a number with fewer than two significant digits
    and fewer than two decimals only as part of an estimate's run "b (lo to hi)"; an estimate with a CI only as that
    run; a P, N or mean of an estimate only where the estimate prints; a display only when drawn from the value's Runs."""
    hits = {k: [] for k in values}
    stems = {}
    for k in values:
        stem, _, part = k.rpartition(".")
        if part in ("b", "ci_lo", "ci_hi") and stem:
            stems.setdefault(stem, set()).add(part)
    trios = {s for s, parts in stems.items() if parts == {"b", "ci_lo", "ci_hi"}}
    for key, row in values.items():
        v = row.get("value")
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        scale = row["_spec"].get("scale", 1)
        p = is_p(key, row)
        stem, _, part = key.rpartition(".")
        if stem in trios and part in ("b", "ci_lo", "ci_hi"):
            continue                                        # the trio rule below
        for where, sec, sid, text, d in where_list:
            if not drawn_from(d, row):
                continue
            for printed, x, dec, before, verb in tokens(text):
                if p != after_p(before):
                    continue
                if not p and dec == 0 and abs(x) < 10:
                    continue
                sig = len(printed.lstrip("<-0.").replace(",", "").replace(".", ""))
                if not p and sig < 2 and dec < 2:
                    continue
                ok = (p and v < float(printed[1:])) if printed.startswith("<") else same(x, dec, v, scale)
                if ok:
                    hits[key].append({"where": where, "section": sec, "sid": sid, "display": d["name"] if d else None,
                                      "printed": verb, "anchor": verb})
                    break
    for stem in trios:                                      # an estimate and its CI print as a run: b (lo to hi)
        b, lo, hi = (values[f"{stem}.{x}"] for x in ("b", "ci_lo", "ci_hi"))
        scale = b["_spec"].get("scale", 1)
        if not all(isinstance(r.get("value"), (int, float)) for r in (b, lo, hi)):
            continue
        for where, sec, sid, text, d in where_list:
            if not drawn_from(d, b):
                continue
            toks = [t for t in tokens(text) if not t[0].startswith("<") and t[2] >= 1]
            for i, tb in enumerate(toks):
                if not same(tb[1], tb[2], b["value"], scale):
                    continue
                for j in (i + 1, i + 2):                    # the 95 of "95% CI" may sit between
                    if j + 1 < len(toks) and same(toks[j][1], toks[j][2], lo["value"], scale) and \
                            same(toks[j + 1][1], toks[j + 1][2], hi["value"], scale):
                        base = {"where": where, "section": sec, "sid": sid, "display": d["name"] if d else None}
                        trio = f"{tb[4]} ({toks[j][4]} to {toks[j + 1][4]})"
                        hits[f"{stem}.b"].append(dict(base, printed=trio, anchor=tb[4]))
                        hits[f"{stem}.ci_lo"].append(dict(base, printed=trio, anchor=toks[j][4], with_estimate=True))
                        hits[f"{stem}.ci_hi"].append(dict(base, printed=trio, anchor=toks[j + 1][4], with_estimate=True))
                        break
                else:
                    continue
                break
    for key in values:                                       # P, N, mean: only beside their estimate
        stem, _, part = key.rpartition(".")
        if stem in trios and part not in ("b", "ci_lo", "ci_hi"):
            at = {h["where"] for h in hits[f"{stem}.b"]}
            hits[key] = [h for h in hits[key] if h["where"] in at]
    for key in hits:                                         # one hit per place
        seen, keep = set(), []
        for h in hits[key]:
            if h["where"] not in seen:
                seen.add(h["where"])
                keep.append(h)
        hits[key] = keep
    return hits


# ════════════════════════════════════════════ 2 · bindings ═══════════════════════════════════════════════════════════
def value_job(board):
    return next((j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"evidence_value|_values?$", j.name)), None)


def holders(board, job):
    """Where bindings live: each printed Section, then each display Task of the display Job."""
    out = list(pt.sections(job)) if job else []
    pool = next((j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"display", j.name)), None)
    return out + (pt.tasks(pool) if pool else [])


def read_cards(holder):
    f = holder / "evidence" / "cards.yaml"
    if not f.is_file():
        return f, "", {"evidence": []}
    text = f.read_text(encoding="utf-8")
    head = "".join(line + "\n" for line in text.splitlines() if line.startswith("#")) if text.startswith("#") else ""
    return f, head, yaml.safe_load(text) or {"evidence": []}


def bindings(board, job, jnn):
    """Every VALUE card item bound to this Board's value Job (`source: jNN.tNN`): [{holder, card, item}]."""
    out = []
    for h in holders(board, job):
        _, _, doc = read_cards(h)
        for card in doc.get("evidence") or []:
            src = str(card.get("source", ""))
            if card.get("kind") in ("value", "work") and src.split(".")[0] == jnn:
                for it in card.get("items") or []:
                    out.append({"holder": h, "task": src.split(".")[1] if "." in src else "", "item": it})
    return out


def key_of(item, values):
    """The catalog key an item is bound to: by its value id (`value: RQ1-t01-002`), else by `key: values.<key>.value`."""
    if cards.is_value_id(item.get("value")):
        return next((k for k, r in values.items() if r["id"] == item["value"]), f"id {item['value']}")
    return re.sub(r"^values\.|\.value$", "", str(item.get("key", "")))


def check_binding(b, values, texts, disp_rows):
    """One binding's ledger rows (one per anchor), by haipipe-evidence's cards.item_status."""
    it, h = b["item"], b["holder"]
    key = key_of(it, values)
    disp = it.get("display")
    sid = ",".join(str(n) for n in it.get("for") or [])
    base = {"where": disp or pt.where_of(h.name, sid), "section": h.name, "sid": sid, "display": disp, "key": key,
            "bound": "card", "note": ""}
    row = values.get(key)
    if row is None and not it.get("need"):
        return [dict(base, status="stale", printed=" / ".join(it.get("anchor") or it.get("printed") or []), value="",
                     id=str(it.get("value") or ""), note=f"no value map holds {key}")]
    text = " ".join(disp_rows.get(disp, [])) if disp else " ".join(texts(h).get(str(n), "") for n in it.get("for") or [])
    pub = public(row) if row else {}
    waits = row and row.get("pending") and row.get("value") is None   # its Run has not returned: nothing to compare yet
    return [dict(base, status="pending" if waits and st == "no anchor" and printed else st, printed=printed,
                 value=pub.get("shown", ""), id=pub.get("id", ""), note=row["pending"] if waits and st == "no anchor" and printed else note)
            for printed, st, note in cards.item_status(it, pub, text)]


# ════════════════════════════════════════════ 3 · check ══════════════════════════════════════════════════════════════
class Paper:
    """The Board read once: writing Job, places, displays, bindings, catalogs."""

    def __init__(self, j02, writing=None):
        self.j02 = j02
        self.board = pt.board_of(j02)
        self.project, self.root = pt.project_root(j02), pt.server_root(j02)
        self.job = pt.writing_job(self.board, writing)
        self.places = places(self.job, self.board)
        self.disp_rows = {d["name"]: d["rows"] for d in pt.displays(self.board, self.job)}
        self.jnn = j02.name.split("_")[0]
        self.binds = bindings(self.board, self.job, self.jnn)
        self._texts = {}

    def texts(self, holder):
        if holder not in self._texts:
            self._texts[holder] = pt.index(holder)
        return self._texts[holder]

    def value_tasks(self):
        return [t for t in pt.tasks(self.j02) if (t / "scripts" / "value_map.yaml").is_file()]


def paper_of(j02):
    """The Paper the paper-wide verbs (check, bind) read: the writing Job the value maps name in `writing:` when they
    agree on one, as `run` reads it for its own Task; else the Board's newest. A revision version made after the
    bindings were ticked (paper_ladder.py next) so leaves them on the send they were ticked in until the maps move."""
    paper = Paper(j02)
    named = {load_map(t).get("writing") for t in paper.value_tasks()} - {None, ""}
    return Paper(j02, named.pop()) if len(named) == 1 else paper


def ledger_rows(paper, task, vmap, values):
    """(rows, hits) for one value Task: its bindings checked, its search hits not bound yet as `found`, its needs."""
    tnn = task.name.split("_")[0]
    hits = find(values, paper.places)
    rows = []
    bound_at = set()
    for b in (x for x in paper.binds if x["task"] == tnn):
        for r in check_binding(b, values, paper.texts, paper.disp_rows):
            rows.append(r)
            bound_at.add((r["key"], r["where"]))
    for key, hs in hits.items():
        for h in hs:
            if (key, h["where"]) not in bound_at and not h.get("with_estimate"):
                row = values[key]
                rows.append({"where": h["where"], "section": h["section"], "sid": h["sid"], "display": h["display"],
                             "key": key, "bound": "", "status": "pending" if row.get("pending") else "found",
                             "printed": h["printed"], "value": row["shown"], "id": row["id"],
                             "note": row.get("pending", "") or "found by the search; waits for your tick in evidence/proposals.md"})
    for key, need in (vmap.get("needs") or {}).items():
        need = need or {}
        sec, sid = need.get("section", ""), str(need.get("sentence", ""))
        rows.append({"where": pt.where_of(sec, sid) if sec else "not placed", "section": sec, "sid": sid, "display": None,
                     "key": key, "bound": "map", "status": "owed", "printed": str(need.get("printed", "")), "value": "",
                     "id": "", "what": need.get("what", ""), "note": need.get("why") or need.get("what", "")})
    return rows, hits


def counts(rows):
    return {s: sum(r["status"] == s for r in rows) for s in STATUSES}


def headline(name, values, rows, unprinted):
    c = counts(rows)
    places = len({(r["key"], r["where"]) for r in rows if r["status"] != "owed"})
    parts = said(c)
    return (f"{name}: {len(values)} values, {len(values) - len(unprinted)} printed in {places} places"
            + (f" ({parts})" if parts else "") + f"; {len(unprinted)} never printed")


def public(row):
    return {k: v for k, v in row.items() if not k.startswith("_")}


def write_result(out, name, src, doc, rows, values, html_doc, line):
    out.mkdir(parents=True, exist_ok=True)
    (out / "values.yaml").write_text(GEN.format(src=src) + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120),
                                     encoding="utf-8")
    with (out / "ledger.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "where", "status", "bound", "printed", "value", "key", "note"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    (out / "values.html").write_text(html_doc, encoding="utf-8")
    (out / "headline.txt").write_text(line + "\n", encoding="utf-8")
    print(line)


def run(task, out):
    """One value Task's Run."""
    task = Path(task).resolve()
    vmap = load_map(task)
    paper = Paper(task.parent, vmap.get("writing"))
    vmap, values = catalog(task)
    rows, hits = ledger_rows(paper, task, vmap, values)
    printed_keys = {r["key"] for r in rows if r["status"] not in ("owed", "stale", "missing")}
    printed_keys |= {k for k, hs in hits.items() if hs}
    unprinted = [k for k in values if k not in printed_keys]
    for key, row in values.items():
        row["printed"] = [{k: r[k] for k in ("where", "printed", "status", "bound")} for r in rows if r["key"] == key]
    line = headline(task.name, values, rows, unprinted)
    doc = {"task": task.name, "group": vmap.get("group", ""), "rq": vmap.get("rq", ""),
           "writing": paper.job.name if paper.job else "", "headline": line, "counts": counts(rows),
           "values": {k: public(v) for k, v in values.items()}, "never_printed": unprinted,
           "needs": vmap.get("needs") or {}}
    html_doc = page(task.name, vmap.get("group", ""), line, rows, values, unprinted, paper)
    write_result(Path(out), task.name, f"{task.name}/scripts/value_map.yaml", doc, rows, values, html_doc, line)
    return doc


def unbound_numbers(paper, all_rows):
    """Numbers the text prints that no binding and no value accounts for: candidates for an owed value."""
    taken = {}
    for r in all_rows:
        taken.setdefault(r["where"], set()).update(re.findall(r"-?\d[\d,]*(?:\.\d+)?|\.\d+", str(r["printed"]).replace("−", "-")))
    out = []
    for where, sec, sid, text, d in paper.places:
        if d is not None:
            continue
        for printed, x, dec, before, verb in tokens(text):
            body = printed.lstrip("<")
            if dec == 0 and abs(x) < 10:
                continue
            if dec == 0 and 1900 <= x <= 2100:
                continue                                    # a year
            if re.search(r"(?:" + "|".join(DISPLAY_WORDS) + r"|Section|S|C\d\.P)\s*$", before):
                continue                                    # Table 2, Figure 1, a sentence id
            if body == "95" and re.match(r"\s*%\s*(?:CI|confidence)", text[text.find(verb) + len(verb):][:16] or ""):
                continue
            if body.replace("-", "") in {t.replace("-", "") for t in taken.get(where, set())}:
                continue
            out.append({"where": where, "printed": verb, "sentence": text[:160]})
    return out


def check(j02, out):
    """The paper-wide Run: every value Task's ledger at once, and the numbers printed with no binding."""
    j02 = Path(j02).resolve()
    paper = paper_of(j02)
    all_rows, all_values, never = [], {}, []
    for task in paper.value_tasks():
        vmap, values = catalog(task)
        rows, hits = ledger_rows(paper, task, vmap, values)
        for r in rows:
            r["task"] = task.name
        all_rows += rows
        printed = {r["key"] for r in rows if r["status"] not in ("owed", "stale", "missing")} | {k for k, h in hits.items() if h}
        never += [values[k]["id"] for k in values if k not in printed]
        all_values.update({f"{task.name}:{k}": v for k, v in values.items()})
    tnns = {t.name.split("_")[0] for t in paper.value_tasks()}
    for b in paper.binds:                                    # a binding to a Task with no value map is stale
        if b["task"] not in tnns:
            for r in check_binding(b, {}, paper.texts, paper.disp_rows):
                all_rows.append(dict(r, task=b["task"]))
    loose = unbound_numbers(paper, all_rows)
    c = counts(all_rows)
    n_tasks = len(paper.value_tasks())             # each count in its own number ("1 value Tasks", "1 printed numbers")
    line = (f"{CHECK_TASK}: {len(all_values)} value{'s' * (len(all_values) != 1)} in {n_tasks} value "
            f"Task{'s' * (n_tasks != 1)}; " + said(c) + f"; {len(never)} never printed; "
            f"{len(loose)} printed number{'s' * (len(loose) != 1)} with no binding")
    doc = {"task": CHECK_TASK, "writing": paper.job.name if paper.job else "", "headline": line, "counts": c,
           "rows": all_rows, "never_printed": never, "printed_unbound": loose,
           "blocking": [k for k, v in all_values.items() if not v["linked"] or v["screen_read"]]}
    merged = {k.split(":", 1)[1]: v for k, v in all_values.items()}
    html_doc = page(CHECK_TASK, "every value Task at once", line, all_rows, merged, [], paper, loose=loose)
    write_result(Path(out), CHECK_TASK, "every value map of " + j02.name, doc, all_rows, all_values, html_doc, line)
    return doc


def bind(j02, propose=False, adopt=False, confirm=None):
    """Seed bindings from the search on haipipe-evidence's proposals path. Without a flag: say what it would propose.
    `--propose`: add a `bind VALUE <id> to <place>` line per hit to each holder's evidence/proposals.md (its need lines
    kept, its ticks kept). `--adopt`: write the ticked lines as card items (cards.adopt_bindings). `--confirm [tNN ...]`:
    an agent or person confirms every proposed binding of those holders (all when none named) and writes them."""
    j02 = Path(j02).resolve()
    paper = paper_of(j02)
    catalogs = {t.name.split("_")[0]: catalog(t)[1] for t in paper.value_tasks()}
    bound = set()
    for b in paper.binds:
        values = catalogs.get(b["task"], {})
        it = b["item"]
        bound.add((key_of(it, values), it.get("display") or pt.where_of(b["holder"].name, ",".join(map(str, it.get("for") or [])))))
    disp_holder = {d["name"]: d["holder"] for d in pt.displays(paper.board, paper.job)}
    per = {}                                                   # holder → [(tNN, rows by id, found {id: [(sid, words)]})]
    for tnn, values in catalogs.items():
        by_holder = {}
        for key, hs in find(values, paper.places).items():
            for h in hs:
                if (key, h["where"]) in bound:
                    continue
                holder = disp_holder.get(h["display"]) if h["display"] else paper.job / h["section"]
                if holder is None:
                    continue
                place = f"display:{h['display']}" if h["display"] else h["sid"]
                by_holder.setdefault(holder, {}).setdefault(values[key]["id"], []).append((place, h["anchor"]))
        for holder, found in by_holder.items():
            per.setdefault(holder, []).append((tnn, {public(v)["id"]: public(v) for v in values.values()}, found))
    total = adopted = 0
    for holder in sorted(set(per) | ({h for h in holders(paper.board, paper.job)} if adopt or confirm is not None else set())):
        f = holder / "evidence" / "cards.yaml"
        have = cards.load(f) if f.is_file() else []
        props = []
        for tnn, rows, found in per.get(holder, []):
            props += cards.bind_proposals(rows, {}, holder.name, f"{paper.jnn}.{tnn}", RUN.split("_")[0], have, found=found)
        if (adopt or confirm is not None) and props:
            only = [pid for pid, _, _ in props] if confirm is not None and (not confirm or holder.name in confirm) else None
            if confirm is None or only:
                n = cards.adopt_bindings(f, props, only)
                adopted += n
                if n:
                    print(f"{holder.name}: {n} bindings written into evidence/cards.yaml")
                have = cards.load(f) if f.is_file() else []
                props = [p for p in props if p[0] not in cards.ticked(f.parent / "proposals.md") and (only is None or p[0] not in only)]
        total += len(props)
        if props:
            print(f"{holder.name}: {len(props)} bindings proposed")
        if propose or adopt or confirm is not None:
            lines = cards.proposals(have, holder.name) + [(pid, line) for pid, line, _ in props]
            out = f.parent / "proposals.md"
            if lines or out.is_file():
                out.parent.mkdir(parents=True, exist_ok=True)
                cards.write_proposals(out, lines)
    if adopt or confirm is not None:
        print(f"{adopted} bindings written; {total} still proposed")
    elif propose:
        print(f"{total} bindings proposed in each holder's evidence/proposals.md; tick them, then bind --adopt")
    else:
        print(f"{total} bindings the search would propose (dry run; --propose writes them to evidence/proposals.md)")


# ════════════════════════════════════════════ values.html ════════════════════════════════════════════════════════════
COLOUR = {"match": "var(--ok)", "differs": "var(--bad)", "missing": "var(--warn)", "stale": "var(--bad)",
          "owed": "var(--owed)", "pending": "var(--warn)", "no anchor": "var(--mut)", "found": "var(--found)"}
CSS = (":root{--fg:#1f2328;--mut:#6e7781;--line:#eaeef2;--ok:#1a7f37;--bad:#cf222e;--warn:#9a6700;--owed:#8250df;"
       "--found:#0969da;--link:#24292f;--bg:#fff}"
       "@media(prefers-color-scheme:dark){:root{--fg:#e6edf3;--mut:#8d96a0;--line:#30363d;--ok:#3fb950;--bad:#f85149;"
       "--warn:#d29922;--owed:#a371f7;--found:#58a6ff;--link:#c9d1d9;--bg:#0d1117}}"
       "body{font:13px/1.45 -apple-system,system-ui,sans-serif;margin:12px;color:var(--fg);background:var(--bg)}"
       "h3{margin:0 0 10px;font-size:14px}h4{margin:18px 0 6px;font-size:13px}table{border-collapse:collapse;width:100%;table-layout:fixed}th:nth-child(1){width:22%}th:nth-child(2){width:16%}th:nth-child(3),th:nth-child(4){width:10%}th:nth-child(5){width:9%}th:nth-child(6){width:33%}td.w{overflow-wrap:normal;word-break:normal}td{overflow-wrap:anywhere}"
       "th,td{padding:6px 8px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{font-weight:600}"
       "td.n{font-variant-numeric:tabular-nums}"
       "td.st small,td.st .mut{font-weight:400;white-space:normal}"
       ".id{font:11px ui-monospace,Menlo,monospace;color:var(--mut);margin-top:2px}td.nm{font-weight:500}td.st{font-weight:600}"
       ".mut{color:var(--mut)}code{font:12px ui-monospace,Menlo,monospace}a{color:var(--link)}td.src a{text-decoration:none}"
       "td.src a:hover{text-decoration:underline}.flag{color:var(--bad);font-weight:600}details{margin-top:14px}"
       "summary{cursor:pointer;color:var(--mut)}"
       # a phone (JL 261103 walk, 390 px): each row a small card, the name and the Source across, Where · Printed ·
       # Value · Status on one line between them; the header row hides
       "@media(max-width:600px){table,tbody{display:block}tr{display:grid;grid-template-columns:auto auto auto 1fr;"
       "gap:2px 12px;padding:8px 0;border-bottom:1px solid var(--line)}tr:first-child{display:none}"
       "td{border:0;padding:0}td:first-child,td:nth-child(6){grid-column:1/-1}td.st{overflow-wrap:normal;white-space:nowrap}}")


def page(name, group, line, rows, values, unprinted, paper, loose=None):
    """values.html, the MISQ ledger's look led by the value's name: Value name (its ID under it) · Where · Printed ·
    Value · Status · Source and key (JL 261103: "the first column should be the name"); problems first, the
    values never printed in a closed list (and, paper-wide, the numbers printed with no binding)."""
    root = paper.root

    def link(c):
        if not c.get("path"):
            return esc(c.get("name", ""))
        return (f'<a target=_top href="{esc(pt.href(root / c["path"], root))}" title="{esc(c["address"])} · '
                f'{esc(c["path"])}">{esc(c["name"])}</a>')

    def src(key, row):
        if not row:
            return f"<td class=src><code>{esc(key)}</code></td>"
        flags = ([("<span class=flag>no Run</span>")] if not row.get("linked") else []) + \
                ([("<span class=flag>screen read</span>")] if row.get("screen_read") else [])
        trail = " ← ".join(link(c) for c in row.get("checks") or [])
        return f"<td class=src><div>{trail} {' '.join(flags)}</div><div class=mut><code>{esc(key)}</code></div></td>"

    def where_cell(r):
        sec = paper.job / r["section"] if paper.job and r.get("section") else None
        w = esc(r["where"])
        if r.get("display"):
            return f"<td class=w><b>{w}</b></td>"
        if sec is not None and sec.is_dir():
            return f'<td class=w><a target=_top href="{esc(pt.href(sec, root, "&section=work&group=write"))}">{w}</a></td>'
        return f"<td class=w>{w}</td>"

    def value_cell(r, row):
        if not row:
            return f"<td class=n>{esc(str(r['value']))}</td>"
        stem = r["key"].rpartition(".")[0]
        lo, hi = values.get(f"{stem}.ci_lo"), values.get(f"{stem}.ci_hi")
        text = f"{row['shown']} ({lo['shown']} to {hi['shown']})" if r["key"].endswith(".b") and lo and hi else row["shown"]
        return f"<td class=n>{esc(text)}</td>"

    def order(r):
        return (STATUSES.index(r["status"]) if r["status"] in ("differs", "missing", "stale", "owed", "pending") else 9,
                [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", r["where"])])

    shown_rows = [r for r in rows if not (r["key"].endswith((".ci_lo", ".ci_hi")) and r["status"] in ("match", "found")
                                          and any(x["key"] == r["key"].rpartition(".")[0] + ".b" and x["where"] == r["where"] for x in rows))]
    at = {(r["key"], r["where"]): r for r in rows}
    for i, r in enumerate(shown_rows):                       # an estimate bound with its CI prints as b (lo to hi)
        stem = r["key"].rpartition(".")[0]
        lo, hi = at.get((f"{stem}.ci_lo", r["where"])), at.get((f"{stem}.ci_hi", r["where"]))
        if r["key"].endswith(".b") and lo and hi and "(" not in str(r["printed"]):
            shown_rows[i] = dict(r, printed=f"{r['printed']} ({lo['printed']} to {hi['printed']})")
    def name_cell(r, row):
        what = (row or {}).get("what") or r.get("what") or r["key"]
        rid = (row or {}).get("id") or r.get("id") or ""
        return f"<td class=nm>{esc(what)}" + (f"<div class=id>{esc(rid)}</div>" if rid else "") + "</td>"

    th = "<tr><th>Value name</th><th>Where</th><th>Printed</th><th>Value</th><th>Status</th><th>Source and key</th></tr>"
    body = "".join(
        f"<tr>{name_cell(r, values.get(r['key']))}{where_cell(r)}<td class=n>{esc(str(r['printed']))}</td>"
        f"{value_cell(r, values.get(r['key']))}<td class=st style='color:{COLOUR.get(r['status'], 'inherit')}'>{esc(WORDS.get(r['status'], r['status']))}"
        + (f"<div class=mut style='font-weight:400'>{esc(r['note'])}</div>" if r.get("note") and r["status"] != "found" else "")
        + f"</td>{src(r['key'], values.get(r['key']))}</tr>"
        for r in sorted(shown_rows, key=order))
    rest = "".join(
        f"<tr>{name_cell({'key': k}, values[k])}<td class=w>not printed</td><td></td><td class=n>{esc(values[k]['shown'])}</td>"
        f"<td class=mut>kept</td>{src(k, values[k])}</tr>" for k in unprinted)
    rqs = sorted({v.get("rq") for v in values.values() if v.get("rq")})
    head = (", ".join(rqs) + " · " if rqs else "") + (f"{group} · " if group else "") + line.split(": ", 1)[-1]
    html_doc = (f"<!doctype html><meta charset=utf-8><title>{esc(name)}</title>"
                "<!-- GENERATED by haipipe-paper-evidence scripts/values_ledger.py; rerun the ticket, never edit this file. -->"
                f"<style>{CSS}</style><h3>{esc(head)}</h3><table>{th}{body}</table>")
    if unprinted:
        html_doc += f"<details><summary>{len(unprinted)} values never printed in the paper</summary><table>{th}{rest}</table></details>"
    if loose is not None:
        cells = "".join(f"<tr><td class=w>{esc(x['where'])}</td><td class=n>{esc(x['printed'])}</td><td class=mut>{esc(x['sentence'])}</td></tr>"
                        for x in loose)
        html_doc += (f"<h4>{len(loose)} number{'s' * (len(loose) != 1)} printed with no binding (a value still to come, or a number to bind)</h4>"
                     + (f"<table><tr><th>Where</th><th>Printed</th><th>Sentence</th></tr>{cells}</table>" if loose else
                        "<p class=mut>none</p>"))
    return html_doc + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("run", help="one value Task's Run")
    a.add_argument("task", type=Path)
    a.add_argument("out", type=Path)
    c = sub.add_parser("check", help="the paper-wide Run")
    c.add_argument("job", type=Path)
    c.add_argument("out", type=Path)
    b = sub.add_parser("bind", help="seed or confirm bindings")
    b.add_argument("job", type=Path)
    b.add_argument("--propose", action="store_true", help="write the proposals into each holder's evidence/proposals.md")
    b.add_argument("--adopt", action="store_true", help="write the ticked proposals as card items")
    b.add_argument("--confirm", nargs="*", metavar="SECTION", help="confirm every proposal of these holders (all when none)")
    args = ap.parse_args(argv)
    if args.cmd == "run":
        run(args.task, args.out)
    elif args.cmd == "check":
        check(args.job, args.out)
    else:
        bind(args.job, args.propose, args.adopt, args.confirm)


if __name__ == "__main__":
    main()
