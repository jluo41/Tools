#!/usr/bin/env python3
"""render_task_table.py — task plan plus display, read off the tree.

    python3 render_task_table.py <tasks-dir | block-dir>
        [--surface all|task|config|run|store] default all
        [--format md|tsv]                    default md
        [--out PATH | --out auto]            auto = <tasks-dir>/TASK-TABLE.md
        [--check PATH] [--expect-fail]       re-render and diff against PATH

THE ONE LAW: nobody types a row IN the table. The three words that say what a
task is for live on the TASK PAGE (its L3 content, typed by a person):

    develops:  <one line: the thing this task builds>
    input:     <what it reads>
    output:    <what it writes>

and the table PROJECTS them. When the page has no such line, the table falls
back to the code's own words and says so in the Source column:

    develops   page `develops:`  →  the ticketed script's docstring headline
    input      page `input:`     →  config worklist/payload/inputs/source/base
    output     page `output:`    →  config entry + out_tier/out_platform/out_vintage,
                                     or entry + out_dimension/vintage/out_name,
                                     or output:, or store:

The generated row has two lenses: Develops/Input/Output are the plan
projection; Address/Task/Code/Runs/State are the observed tree and runtime
display projection. Configs are summarized on the Task row and expanded once
in Config Catalog. The table is a read projection, not a new authority.

`--check` re-renders and fails on any difference, so a copy on disk cannot
drift from the tree (haipipe-task S8). `--expect-fail` inverts the exit code so
the gate is shown to fail before a pass is trusted (GATE-1).

WHAT ELSE IT READS, and only this:
    folder structure           blocks > jobs > tasks by STRUCTURE; names are
                               checked against <b|j|t|r>NN_ and flagged, never
                               used as a filter
    tNN_<task>.md              state: · owner: · develops: · input: · output:
    scripts/ scripts/config/   the task's code and configs (legacy config/,
                               configs/ read and flagged S10); each config is
                               one Config Catalog row
    runs/*.sh|*.ps1            tickets = planned Runs; the script a ticket
                               names is the task's main script
    <job>/results/<task>/<run>/runtime.yaml   the receipt = an actual Run
    <job>/src/config-defaults.yaml `store:`   the job's mode (② consumer-
                               serving); a `store:` in a task config is DERIVED
Nothing from git, boards, or another table. A future Board Table is outside
this scan.

THE SHAPE (JL 260904): a BLOCK is a section, a JOB is one table, a TASK is one
row. Configs and Runs are appendix rows; they never multiply the Task row. The
job's facts (mode, store, tickets, runs) sit on its heading line.

    ## b04 · b04_npi_dimension_tables            block section
    ### b04j08 · j08_npi2photo                   job = one table, its rollup on this line
    | Addr | Task | Develops | Input | Output | Configs | Code | Runs | State |
    | b04j08t01 | t01_photo_url_table | one photo URL per NPI … | … |

Two appendix surfaces from the same scan:
    Config Catalog one config           task · config · purpose · mode · input · output
    Runs Overview  one Run              bNNjNNtNNrNN · task · config · ticket ↔ receipt · status
                                        (`all` shows receipts only; `--surface run` shows planned too)
    Store Slots    one (job, store)     where a consumer-serving job writes
"""
import argparse
import ast
import difflib
import re
import sys
from datetime import datetime
from pathlib import Path

IDX = re.compile(r"^([bjtr])(\d\d)_(.+)$")
NOT_A_TASK = {"src", "sbatch", "results", "notebooks", "QA", "workflow",
              "outline", "diagram", "__pycache__", "_tools", "dist", "chat"}
TICKET_EXT = {".sh", ".ps1"}
CODE_EXT = {".py", ".do", ".R", ".sh", ".ipynb"}
GEN_LINE = re.compile(r"^(<!-- generated .*-->|generated: .*)$")
# "05_stage_phy_store: ..." / "11_npi2photo — ..." / "fetch_photos — ..." → the words after the dash
HEAD_PREFIX = re.compile(r"^(?:\d+[_-])?[A-Za-z0-9_.\-]+\s*(?:[:—–-]+|--)\s+")

STATUS = {"ok": "Done", "complete": "Done", "completed": "Done",
          "running": "Running", "failed": "Failed", "aborted": "Failed",
          "planned": "Ready", "blocked": "Held", "superseded": "Superseded"}
IN_KEYS = ("worklist", "payload", "inputs", "input", "source", "base")
BLOCK_MARKERS = {"|", ">", "|-", ">-", "|+", ">+"}


# ── tiny readers (no PyYAML: only scalar fields are needed) ──────────────────
def _scalar(raw):
    """Return a useful scalar without pretending to parse arbitrary YAML."""
    return raw.split("  #", 1)[0].strip().strip("'\"")


def _scalar_map(lines, indent=0):
    """Read scalar keys at one exact indent, including simple block scalars."""
    out = {}
    prefix = " " * indent
    key_re = re.compile(rf"^{re.escape(prefix)}([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$")
    i = 0
    while i < len(lines):
        m = key_re.match(lines[i])
        if not m:
            i += 1
            continue
        key, raw = m.group(1), m.group(2)
        if not raw or raw.startswith("#"):
            i += 1
            continue
        if raw in BLOCK_MARKERS:
            values, j = [], i + 1
            while j < len(lines):
                line = lines[j]
                if line.strip() and len(line) - len(line.lstrip()) <= indent:
                    break
                values.append(line[indent + 2:].strip() if line.strip() else "")
                j += 1
            value = ("\n" if raw.startswith("|") else " ").join(values).strip()
            if value:
                out.setdefault(key, value)
            i = j
            continue
        out.setdefault(key, _scalar(raw))
        i += 1
    return out


def yaml_fields(path):
    """Return top-level scalars and the simple two-space ``_meta`` scalars."""
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return {}, {}
    top = _scalar_map(lines, 0)
    meta = {}
    meta_start = next((i for i, line in enumerate(lines) if line == "_meta:"), None)
    if meta_start is not None:
        meta_end = next((i for i in range(meta_start + 1, len(lines))
                         if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", lines[i])), len(lines))
        meta = _scalar_map(lines[meta_start + 1:meta_end], 2)
    return top, meta


def flat_yaml(path):
    """Read top-level scalar fields for receipts, stores, and config fallbacks."""
    try:
        return _scalar_map(path.read_text(errors="replace").splitlines(), 0)
    except OSError:
        return {}


def head_field(path, key):
    """`key: value` in the first 40 lines of a page; '' when the line is empty."""
    try:
        for line in path.read_text(errors="replace").splitlines()[:40]:
            m = re.match(rf"^{key}:\s*(.*?)\s*$", line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return None


def headline(script: Path):
    """First non-empty docstring / comment line, minus a `NN_name —` prefix."""
    try:
        text = script.read_text(errors="replace")
    except OSError:
        return ""
    doc = ""
    if script.suffix == ".py":
        try:
            doc = ast.get_docstring(ast.parse(text)) or ""
        except Exception:
            doc = ""
    else:  # .do / .R / .sh: leading comment lines
        for line in text.splitlines()[:15]:
            s = line.strip()
            if s.startswith(("//", "*", "#")) and not s.startswith("#!"):
                s = s.lstrip("/*# ").strip().lstrip("=-*#").strip()
                if s:
                    doc = s
                    break
    para = []
    for l in doc.splitlines():
        if not l.strip():
            if para:
                break
            continue
        para.append(l.strip())
    line = " ".join(para)
    line = HEAD_PREFIX.sub("", line, count=1).strip()
    m = re.match(r"^(.{20,}?[.!?])(?=\s+[A-Z(\[]|\s*$)", line)   # first full sentence; "M.D./D.O. worklist" is not one
    line = m.group(1) if m else line
    return line if len(line) <= 140 else line[:137].rstrip() + "…"


def prefix(name, level):
    m = IDX.match(name)
    if m and m.group(1) == level:
        return f"{level}{m.group(2)}", None
    return f"{level}??", f"N1 {name}: not <{level}>NN_<name>"


def subdirs(p):
    return sorted(d for d in p.iterdir() if d.is_dir() and not d.name.startswith((".", "_")))


# ── scan ─────────────────────────────────────────────────────────────────────
def scan(root: Path):
    findings, blocks = [], []
    block_dirs = [root] if IDX.match(root.name) and root.name[0] == "b" else subdirs(root)
    for b in block_dirs:
        if not any(subdirs(b)):
            continue
        baddr, f = prefix(b.name, "b")
        if f:
            findings.append(f)
        jobs = []
        for j in subdirs(b):
            jaddr, f = prefix(j.name, "j")
            if f:
                findings.append(f)
            store, store_src = job_store(j, findings)
            tasks = [scan_task(t, j, baddr + jaddr, findings)
                     for t in subdirs(j) if t.name not in NOT_A_TASK]
            src = sorted(p.name for p in (j / "src").glob("*") if p.is_file() and not p.name.startswith(".")) if (j / "src").is_dir() else []
            orphan_results(j, tasks, findings)
            jobs.append(dict(addr=baddr + jaddr, name=j.name, path=j, tasks=tasks,
                             store=store, store_src=store_src, src=src))
        blocks.append(dict(addr=baddr, name=b.name, path=b, jobs=jobs))
    return blocks, findings


def job_store(j, findings):
    for name in ("config-defaults.yaml", "config-defaults.do"):
        p = j / "src" / name
        if p.is_file() and flat_yaml(p).get("store"):
            return flat_yaml(p)["store"], f"declared · src/{name}"
    seen = {}
    for cfg in sorted(list(j.glob("*/scripts/config/*.y*ml")) + list(j.glob("*/config*/*.y*ml"))):
        v = flat_yaml(cfg).get("store")
        if v:
            seen.setdefault(v, cfg.relative_to(j))
    if len(seen) > 1:
        findings.append(f"S-store {j.name}: {len(seen)} distinct store: values ({', '.join(seen)})")
    if seen:
        v, src = next(iter(seen.items()))
        return v, f"derived · {src}"
    return None, None


def main_script(t, scripts, tickets):
    """The script a ticket runs; else the one named like the task; else the first."""
    stems = {s.stem: s for s in scripts}
    clean = lambda x: re.sub(r"^[A-Za-z]?\d+[_-]", "", x)
    for tk in tickets:
        try:
            txt = tk.read_text(errors="replace")
        except OSError:
            continue
        names = re.findall(r'TASK_NAME="([^"]+)"', txt) + re.findall(r"([A-Za-z0-9_.\-]+)\.(?:py|do|R)\b", txt)
        for n in names:
            for cand in (n, clean(n)):
                if cand in stems:
                    return stems[cand]
    noun = IDX.match(t.name).group(3) if IDX.match(t.name) else t.name
    for s in scripts:
        if s.stem in noun or noun in s.stem:
            return s
    return scripts[0] if scripts else None


def config_fields(cfg):
    """Merge supported top-level fields with the config's simple ``_meta``."""
    top, meta = yaml_fields(cfg)

    def get(key):
        return top.get(key) or meta.get(key) or ""

    return top, meta, get


def config_io_one(cfg):
    """Return the plan values declared by one config, without guessing."""
    _top, _meta, get = config_fields(cfg)
    inp = next((f"{k}: {get(k)}" for k in IN_KEYS if get(k)), "")
    entry = get("entry")
    if get("out_tier"):
        out = "/".join(x for x in (entry, get("out_tier"), get("out_platform"), get("out_vintage")) if x)
    elif get("out_dimension"):
        out = "/".join(x for x in (entry, get("out_dimension"), get("vintage") or get("out_vintage"), get("out_name")) if x)
    elif get("output"):
        out = get("output")
    elif get("store"):
        out = get("store")
    else:
        out = ""
    return compact(inp, 240), compact(out, 240)


def config_io(configs):
    """(input, output, source) from the NEWEST config's declared fields."""
    if not configs:
        return "", "", ""
    cfg = configs[-1]
    inp, out = config_io_one(cfg)
    return inp, out, f"config {cfg.name}"


def config_purpose(cfg):
    """Return a declared purpose and its source; never infer one from a name."""
    top, meta, _ = config_fields(cfg)
    for source, key, fields in (("top-level purpose", "purpose", top),
                                ("top-level description", "description", top),
                                ("_meta.purpose", "purpose", meta),
                                ("_meta.description", "description", meta),
                                ("top-level headline", "headline", top),
                                ("_meta.headline", "headline", meta)):
        if fields.get(key):
            return fields[key], source
    return "", "not declared"


def config_record(cfg, task):
    """The Config Catalog record for one config file."""
    _top, _meta, get = config_fields(cfg)
    inp, out = config_io_one(cfg)
    purpose, purpose_src = config_purpose(cfg)
    return dict(name=cfg.name, path=str(cfg.relative_to(task)),
                purpose=compact(purpose, 180) if purpose else "? (not declared)", purpose_src=purpose_src,
                mode=get("mode") or "—", inp=inp or "—", out=out or "—")


def scan_task(t, j, job_addr, findings):
    taddr, f = prefix(t.name, "t")
    if f:
        findings.append(f)
    addr = job_addr + taddr
    page = t / f"{t.name}.md"
    fld = (lambda k: head_field(page, k)) if page.is_file() else (lambda k: None)
    if page.is_file():
        state = fld("state") or "? (no state: line)"
    else:
        state = "⬜ no page"
        findings.append(f"S5 {addr} {t.name}: no {t.name}.md")
    owner = fld("owner") or ""

    scripts = sorted(p for p in (t / "scripts").glob("*") if p.is_file() and p.suffix in CODE_EXT) \
        if (t / "scripts").is_dir() else []
    if not scripts and (t / f"{t.name}.py").is_file():
        scripts = [t / f"{t.name}.py"]
        findings.append(f"S-legacy {addr} {t.name}: code at task root, not scripts/")
    cfg_dir = next((c for c in (t / "scripts" / "config", t / "config", t / "configs") if c.is_dir()), None)
    if cfg_dir is not None and cfg_dir.parent == t:
        findings.append(f"S10 {addr} {t.name}: {cfg_dir.name}/ at task root; belongs in scripts/config/")
    configs = sorted(p for p in cfg_dir.glob("*") if p.is_file()) if cfg_dir else []
    config_records = [config_record(cfg, t) for cfg in configs]
    config_by_stem = {cfg.stem: record for cfg, record in zip(configs, config_records)}
    tickets = sorted(p for p in (t / "runs").glob("*") if p.is_file() and p.suffix in TICKET_EXT) \
        if (t / "runs").is_dir() else []

    # what it develops: page first, code second
    main = main_script(t, scripts, tickets)
    develops, dsrc = fld("develops"), "page"
    if not develops:
        develops, dsrc = (headline(main) if main else ""), (f"docstring {main.name}" if main else "")
    inp, out, iosrc = fld("input"), fld("output"), "page"
    cin, cout, csrc = config_io(configs)
    if not inp:
        inp, iosrc = cin, csrc
    if not out:
        out = cout
        iosrc = csrc if not fld("input") else iosrc
    src_note = dsrc if dsrc == "page" and iosrc == "page" else " · ".join(s for s in (dsrc, iosrc) if s and s != "page")

    receipts = {}
    for res_root, dialect in ((j / "results" / t.name, "job"), (t / "results", "task-local")):
        if not res_root.is_dir():
            continue
        if dialect == "task-local":
            findings.append(f"S-results {addr} {t.name}: results/ inside the task; the law is <job>/results/<task>/")
        for run_dir in subdirs(res_root):
            r = run_dir / "runtime.yaml"
            if r.is_file():
                receipts[run_dir.name] = dict(path=r, **flat_yaml(r))
            else:
                findings.append(f"R01 {addr} {t.name}/{run_dir.name}: results folder without runtime.yaml")

    runs, seen, off = [], set(), []
    for tk in tickets:
        raddr, f = prefix(tk.stem, "r")
        if f:
            off.append(tk.name)
        seen.add(tk.stem)
        cfg = config_by_stem.get(tk.stem)
        runs.append(run_row(addr, raddr, tk.stem, tk, receipts.get(tk.stem), t,
                            cfg["path"] if cfg else "? (config not found)"))
    if off:
        findings.append(f"N1 {addr} {t.name}: {len(off)} of {len(tickets)} tickets not rNN_<stem> "
                        f"(e.g. {', '.join(off[:2])})")
    for stem, rec in receipts.items():
        if stem not in seen:
            findings.append(f"R-orphan {addr} {t.name}/{stem}: receipt with no ticket in runs/")
            cfg = config_by_stem.get(stem)
            runs.append(run_row(addr, prefix(stem, "r")[0], stem, None, rec, t,
                                cfg["path"] if cfg else "? (config not found)"))

    return dict(addr=addr, name=t.name, path=t, page=page if page.is_file() else None,
                state=state, owner=owner, develops=develops or "?", inp=inp or "—", out=out or "—",
                src=src_note or "page", scripts=[s.name for s in scripts],
                main=main.name if main else "", configs=config_records,
                tickets=[p.name for p in tickets], runs=runs)


def run_row(taddr, raddr, stem, ticket, rec, t, config):
    if rec is None:
        status, started, ended, exit_code, result, src = "Ready", "", "", "", "", "ticket only"
    else:
        raw = rec.get("status", "")
        status = STATUS.get(raw.lower(), f"? ({raw})" if raw else "? (no status)")
        started = rec.get("started") or rec.get("started_at") or ""
        ended = rec.get("ended") or rec.get("finished_at") or ""
        exit_code, src = rec.get("exit_code", ""), "receipt"
        result = str(rec["path"].parent.relative_to(t.parent.parent))
    return dict(addr=taddr + raddr, task=t.name, config=config, run=stem,
                ticket=f"runs/{ticket.name}" if ticket else "⬜ none", status=status,
                started=started[:16], ended=ended[:16], exit_code=str(exit_code),
                result=result, source=src)


def orphan_results(j, tasks, findings):
    names = {t["name"] for t in tasks}
    if (j / "results").is_dir():
        for d in subdirs(j / "results"):
            if d.name not in names:
                findings.append(f"R-orphan {j.name}/results/{d.name}: no such task in this job")


# ── surfaces ─────────────────────────────────────────────────────────────────
# SHAPE (JL 260904): a BLOCK is a section, a JOB is one table, a TASK is one row.
# Configs and Runs are appendices, so neither multiplies the Task row. The job's
# own facts (mode, store, tickets, runs) sit on its heading line, so there is no
# separate Job Rollup surface: the heading IS the rollup.
def run_counts(runs):
    c = {}
    for r in runs:
        k = r["status"].split(" ")[0]
        c[k] = c.get(k, 0) + 1
    return c


def fmt_counts(c):
    parts = [f"{k} {c[k]}" for k in ("Done", "Running", "Failed", "Held", "Ready", "?") if k in c]
    return " · ".join(parts) if parts else "—"


TASK_HDR = ["Addr", "Task", "Develops", "Input", "Output", "Configs", "Code", "Runs", "State"]


def compact(value, limit=80):
    value = " ".join(str(value).split())
    return value if len(value) <= limit else value[:limit - 1].rstrip() + "…"


def config_summary(configs):
    """Keep the Task row readable while pointing to every config in the appendix."""
    if not configs:
        return "—"
    labels = []
    for cfg in configs:
        label = cfg["name"]
        if cfg["mode"] != "—":
            label += f" [{cfg['mode']}]"
        labels.append(label)
    if len(labels) <= 4:
        return " · ".join(labels)
    return f"{len(labels)} cfg · " + " · ".join(labels[:3]) + f" · +{len(labels) - 3} more (Config Catalog)"


def task_row(t, italics=True):
    """One task = one row. Develops in italics when it is the code's own words
    (docstring), plain when a person typed it on the page. TSV carries no mark."""
    dev = t["develops"]
    if italics and dev != "?" and not t["src"].startswith("page") and "docstring" in t["src"]:
        dev = f"_{dev}_"
    code = t["main"] or "—"
    configs = config_summary(t["configs"])
    runs = f"{len(t['tickets'])} tk" + (f" · {fmt_counts(run_counts(t['runs']))}" if t["runs"] else "")
    return [t["addr"], t["name"], dev, t["inp"], t["out"], configs, code, runs, t["state"]]


def job_heading(j):
    ts = j["tasks"]
    runs = [r for t in ts for r in t["runs"]]
    mode = f"② → {j['store']} ({j['store_src'].split(' · ')[0]})" if j["store"] else "① self-serving"
    pages = sum(1 for t in ts if t["page"] is not None)
    typed = sum(1 for t in ts if t["src"] == "page")
    return (f"### {j['addr']} · {j['name']}\n\n"
            f"{mode} · {len(ts)} tasks · pages {pages}/{len(ts)} (develops typed {typed}) · "
            f"src {len(j['src'])} · tickets {sum(len(t['tickets']) for t in ts)} · "
            f"runs {fmt_counts(run_counts(runs))}")


def surface_blocks(blocks):
    """Sections: ## block → ### job → | task rows |."""
    out = []
    for b in blocks:
        n_tasks = sum(len(j["tasks"]) for j in b["jobs"])
        stores = sorted({j["store"] for j in b["jobs"] if j["store"]})
        out += [f"## {b['addr']} · {b['name']}", "",
                f"{len(b['jobs'])} jobs · {n_tasks} tasks" + (f" · stores: {', '.join(stores)}" if stores else ""), ""]
        for j in b["jobs"]:
            out += [job_heading(j), "", md_table(TASK_HDR, [task_row(t) for t in j["tasks"]]), ""]
    return "\n".join(out)


CONFIG_HDR = ["Task", "Config", "Purpose", "Mode", "Input", "Output", "Purpose source"]


def config_rows(blocks):
    return [[f"{t['addr']} {t['name']}", cfg["path"], cfg["purpose"], cfg["mode"],
             cfg["inp"], cfg["out"], cfg["purpose_src"]]
            for b in blocks for j in b["jobs"] for t in j["tasks"] for cfg in t["configs"]]


RUN_HDR = ["Run", "Task", "Config", "Ticket", "Status", "Started", "Ended", "Exit", "Result", "Source"]


def run_rows(blocks, receipts_only):
    return [[r["addr"], r["task"], r["config"], r["ticket"], r["status"], r["started"] or "—", r["ended"] or "—",
             r["exit_code"] or "—", r["result"] or "—", r["source"]]
            for b in blocks for j in b["jobs"] for t in j["tasks"] for r in t["runs"]
            if not receipts_only or r["source"] == "receipt"]


STORE_HDR = ["Store", "Job", "Provenance", "Outputs declared by its tasks", "Runs Done"]


def store_rows(blocks):
    rows = []
    for b in blocks:
        for j in b["jobs"]:
            if not j["store"]:
                continue
            outs = sorted({t["out"] for t in j["tasks"] if t["out"] != "—"})
            done = sum(1 for t in j["tasks"] for r in t["runs"] if r["status"] == "Done")
            rows.append([j["store"], f"{j['addr']} {j['name']}", j["store_src"], "; ".join(outs) or "—", str(done)])
    return rows


# ── render ───────────────────────────────────────────────────────────────────
def md_table(hdr, rows):
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out) if rows else "_(no rows)_"


def tsv_table(hdr, rows):
    return "\n".join(["\t".join(hdr)] + ["\t".join(str(c).replace("\t", " ") for c in r) for r in rows])


def render(root, blocks, findings, which, fmt):
    tasks = [t for b in blocks for j in b["jobs"] for t in j["tasks"]]
    runs = [r for t in tasks for r in t["runs"]]
    configs = [cfg for t in tasks for cfg in t["configs"]]
    n_jobs = sum(len(b["jobs"]) for b in blocks)
    typed = sum(1 for t in tasks if t["src"] == "page")
    receipts = sum(1 for r in runs if r["source"] == "receipt")
    declared_config_descriptions = sum(1 for cfg in configs if cfg["purpose"] != "? (not declared)")
    lines = []
    if fmt == "md":
        lines += [f"<!-- generated by task-table/ref/render_task_table.py from {root} · do not edit; rerun instead -->",
                  f"# Task Table · {root.name}", "",
                  f"generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                  f"blocks {len(blocks)} · jobs {n_jobs} · tasks {len(tasks)} · tickets {sum(len(t['tickets']) for t in tasks)} "
                  f"· configs {len(configs)} ({declared_config_descriptions} described) · receipts {receipts} "
                  f"· runs {fmt_counts(run_counts(runs))}",
                  f"Develops: {typed} typed on the page, {len(tasks) - typed} _in italics_ = the code's own docstring, "
                  f"not yet confirmed by a person", ""]
    if which in ("all", "task"):
        if fmt == "md":
            lines += [surface_blocks(blocks)]
        else:
            lines += ["# Task Table", tsv_table(TASK_HDR, [task_row(t, italics=False) for t in tasks]), ""]
    if which in ("all", "config"):
        rows = config_rows(blocks)
        if rows or which == "config":
            lines += (["## Config Catalog · one row per configuration", "", md_table(CONFIG_HDR, rows), ""] if fmt == "md"
                      else ["# Config Catalog", tsv_table(CONFIG_HDR, rows), ""])
    if which in ("all", "run"):
        rows = run_rows(blocks, receipts_only=(which == "all"))
        title = "Runs Overview · one row per receipt" if which == "all" else "Runs Overview · one row per Run (ticket ↔ receipt)"
        if rows or which == "run":
            lines += ([f"## {title}", "", md_table(RUN_HDR, rows), ""] if fmt == "md"
                      else [f"# {title}", tsv_table(RUN_HDR, rows), ""])
    if which in ("all", "store"):
        rows = store_rows(blocks)
        lines += ([f"## Store Slots · one row per consumer-serving job", "", md_table(STORE_HDR, rows), ""] if fmt == "md"
                  else ["# Store Slots", tsv_table(STORE_HDR, rows), ""])
    if findings and which == "all":
        lines += ["## ⚠ Findings · read off the tree, not judged", ""]
        lines += [f"- {f}" for f in sorted(set(findings))]
        lines += ["", "_Full audit: haipipe-task/ref/check_task_tree.py_", ""]
    return "\n".join(lines).rstrip() + "\n"




def strip_gen(text):
    return "\n".join(l for l in text.splitlines() if not GEN_LINE.match(l))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--surface", default="all", choices=["all", "task", "config", "run", "store"])
    ap.add_argument("--format", default="md", choices=["md", "tsv"])
    ap.add_argument("--out", help="write here; 'auto' = <root>/TASK-TABLE.md")
    ap.add_argument("--check", help="re-render and diff against this file; exit 1 on drift")
    ap.add_argument("--expect-fail", action="store_true", help="invert the --check exit code (GATE-1)")
    A = ap.parse_args()

    root = Path(A.root).resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    blocks, findings = scan(root)
    text = render(root, blocks, findings, A.surface, A.format)

    if A.check:
        old = Path(A.check).read_text() if Path(A.check).is_file() else ""
        same = strip_gen(old) == strip_gen(text)
        if same:
            print(f"✅ {A.check} matches the tree")
        else:
            diff = list(difflib.unified_diff(strip_gen(old).splitlines(), strip_gen(text).splitlines(),
                                             "on disk", "re-rendered", lineterm="", n=0))
            print("\n".join(diff[:40]))
            print(f"\n❌ DRIFT: {A.check} no longer matches the tree ({len(diff)} diff lines)")
        code = 0 if same else 1
        sys.exit((1 - code) if A.expect_fail else code)

    if A.out:
        out = root / "TASK-TABLE.md" if A.out == "auto" else Path(A.out)
        out.write_text(text)
        print(f"wrote {out}  ({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
