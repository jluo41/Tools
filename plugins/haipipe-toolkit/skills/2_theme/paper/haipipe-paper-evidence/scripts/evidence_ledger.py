"""One version of a paper read as one evidence ledger: every Section's evidence side by side, and what disagrees.

    python evidence_ledger.py <version Job folder> [--max-displays N] [--json]

A version is a Job, `jNN_v<MMDD>_<desk>/`; its Sections, the Abstract and its letters are its Tasks, `tNN_<name>/`, each a
draft Task (haipipe-paper-draft). A Task's evidence is read in either of its two shapes:

    evidence/cards.yaml                    haipipe-evidence cards (CITE from discovery Runs, VALUE from work Runs), 261016 on; VALUE was WORK until 261020
    draft/<stem>-evidence-items.md         an older Page's typed Evidence Items (CITE · VALUE · DISPLAY), read by
                                           haipipe-draft's item_table, the one parser the Page workbench also uses
    display/Display<n>-<slug>/             its displays (haipipe-display)

A base skill sees one Task at a time; this reads the whole version, so it can say what no single Task can:

    ❗ one value, two Runs            the same VALUE (source, file, key) read from different Runs in two Sections
    ❗ one label, different estimates  an older VALUE label whose Results report different estimates, in one unit
    ❗ one citation key, two entries   the same key with another year or title in two Sections' .bib files
    ❗ too many displays              main-text displays over the venue's limit (--max-displays)
    ❗ a card does not resolve        haipipe-evidence's cards.check, per Section
    ⚠️ one label, the same estimates  two Results holding the same estimates (one copies the other)
    ⚠️ one display twice              the same display name in two Sections
    ⬜ open                           citations not yet verified, values not yet landed, needs not yet filled

Only the Sections in the version face's `haipipe:compile-order` block are numbered, counted and compared. Numbers
typed into table bodies or prose, and wording, are not read yet.

It prints and changes no file of the paper: the ledger is a view of the Tasks' own files. Exit 1 on a ❗.
haipipe-paper-evidence 0.1.0 (JL 261019: "and also have a haipipe-paper-evidence?").
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = next(p for p in HERE.parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base/evidence/haipipe-evidence/scripts"))
sys.path.insert(0, str(SKILLS / "1_base/draft/haipipe-draft"))
import cards as ev  # noqa: E402   haipipe-evidence: load, resolve, work_value, check
from src import item_table  # noqa: E402   haipipe-draft: read_items, the older Evidence Items

TASK = re.compile(r"^t(\d+)_")


def part_of(name: str) -> str:
    """t00 the Abstract, t01-t19 the main text, t20-t29 the appendix, t30 on the letters."""
    n = int(TASK.match(name).group(1))
    return "abstract" if n == 0 else "main" if n < 20 else "appendix" if n < 30 else "letter"


def tasks(job: Path) -> list[Path]:
    return sorted((p for p in job.iterdir() if p.is_dir() and TASK.match(p.name)), key=lambda p: int(TASK.match(p.name).group(1)))


def read_cards(task: Path, project: Path | None) -> tuple[list[dict], list[str]]:
    """Rows from evidence/cards.yaml, and cards.check's problems; ([], []) when the Task has no cards."""
    f = task / "evidence" / "cards.yaml"
    if not f.is_file():
        return [], []
    cards = ev.load(f)
    problems = ev.check(cards, project) if project else ["no project.yaml above the version: addresses not checked"]
    rows = []
    for card in cards:
        for it in card.get("items") or []:
            row = {"kind": ev.LABEL.get(card.get("kind"), "?"), "source": card.get("source", ""), "run": it.get("run", ""),
                   "for": it.get("for", []), "anchor": it.get("anchor", []), "file": it.get("file", ""),
                   "key": it.get("key", ""), "need": it.get("need", ""), "value": it.get("value")}
            if row["kind"] == "VALUE" and row["run"] and row["key"] and project:
                try:
                    res = ev.resolve(project, "value", f"{row['source']}.{row['run']}")
                    row["value"] = ev.work_value(res, row["file"], row["key"])
                except (ValueError, KeyError, IndexError, FileNotFoundError):
                    pass                                         # cards.check has named it
            rows.append(row)
    return rows, problems


def read_items(task: Path) -> list[dict]:
    """Rows from an older Page's draft/<stem>-evidence-items.md; [] when it has none."""
    face = task / f"{task.name}.md"
    if not face.is_file():
        return []
    out = []
    for item, r in item_table.read_items(face).items():
        if r.get("decision") == "drop":
            continue
        out.append({"item": item, "type": r.get("type", ""), "label": r.get("label", ""), "target": r.get("target", ""),
                    "result": r.get("result") or r.get("address") or "", "verified": bool(r.get("verification_signed"))})
    return out


def estimates(result: Path) -> dict:
    """The estimates a value Result reports, {key: value}: every number under a key holding "estimate" (a p-value or
    a count is not an estimate); empty when the file is missing or holds none."""
    import yaml
    try:
        text = result.read_text(encoding="utf-8")
        data = json.loads(text) if text.lstrip().startswith("{") else yaml.safe_load(text)
    except (OSError, ValueError, yaml.YAMLError):
        return {}
    out = {}

    def walk(x, key=""):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, str(k))
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, (int, float)) and not isinstance(x, bool) and "estimate" in key.lower():
            out.setdefault(key, x)
    walk(data)
    return out


def one_unit(found: dict) -> frozenset:
    """The estimates as proportions, so 0.0007 and 0.07 percentage points compare equal (a key with `pp` or
    `percentage_point` is in percentage points), rounded to 6 significant digits."""
    pp = re.compile(r"(^|_)pp($|_)|percentage_point", re.I)
    return frozenset(float(f"{(v / 100 if pp.search(k) else v):.6g}") for k, v in found.items())


def said(found: dict) -> str:
    return ", ".join(f"{k} {v:g}" for k, v in found.items())


def compile_order(job: Path) -> list[str]:
    """The Tasks the version prints: its face's `haipipe:compile-order` block; [] when the face has none."""
    face = job / f"{job.name}.md"
    m = re.search(r"(?s)<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->",
                  face.read_text(encoding="utf-8")) if face.is_file() else None
    return re.findall(r"(?m)^\s*-\s*(t\d+_[\w.-]+)", m.group(1)) if m else []


def field(body: str, name: str) -> str:
    """One BibTeX field's value: {braced, nested}, "quoted", or a bare word; '' when the entry has none."""
    m = re.search(r"(?i)\b" + name + r"\s*=\s*", body)
    if not m:
        return ""
    i = m.end()
    if i < len(body) and body[i] == "{":
        depth = 0
        for j in range(i, len(body)):
            depth += {"{": 1, "}": -1}.get(body[j], 0)
            if depth == 0:
                return body[i + 1:j]
        return body[i + 1:]
    if i < len(body) and body[i] == '"':
        end = body.find('"', i + 1)
        return body[i + 1:end if end > 0 else None]
    return re.match(r"[^,}\s]*", body[i:]).group(0)


def bib_entries(task: Path, rows: list[dict], project: Path | None) -> dict:
    """{key: (year, title in plain lower case)} from the Section's own .bib files (draft/evidence/bibex/ on an older
    Page) and the .bib of each discovery Run its CITE cards name."""
    files = sorted((task / "draft" / "evidence" / "bibex").glob("*.bib"))
    for r in rows:
        if r["kind"] == "CITE" and r["run"] and project:
            try:
                files += sorted(ev.resolve(project, "cite", f"{r['source']}.{r['run']}").glob("*.bib"))
            except ValueError:
                pass                                             # cards.check has named it
    out = {}
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", text, re.S):
            body = m.group(2)
            title = re.sub(r"[^a-z0-9 ]", "", re.sub(r"[{}]", "", field(body, "title")).lower())
            out[m.group(1)] = (field(body, "year").strip(), " ".join(title.split()))
    return out


def displays(task: Path, items: list[dict]) -> list[str]:
    """The Task's displays: display/Display<n>-<slug>/ folders, then its older DISPLAY items, by label."""
    found = [p.name for p in sorted((task / "display").glob("Display*")) if p.is_dir()] if (task / "display").is_dir() else []
    return found + [i["label"] or i["item"] for i in items if i["type"] == "DISPLAY"]


def ledger(job: Path, max_displays: int | None = None) -> dict:
    job = Path(job).resolve()
    try:
        project = ev.project_root(job)
    except ValueError:
        project = None
    sections, bad, warn = [], [], []
    order = compile_order(job)
    for t in tasks(job):
        rows, problems = read_cards(t, project)
        items = read_items(t)
        shows = displays(t, items)
        cite = [r for r in rows if r["kind"] == "CITE"] + [i for i in items if i["type"] == "CITE"]
        work = [r for r in rows if r["kind"] == "VALUE"] + [i for i in items if i["type"] == "VALUE"]
        open_cite = sum(1 for r in rows if r["kind"] == "CITE" and r["need"]) + \
            sum(1 for i in items if i["type"] == "CITE" and not i["verified"])
        open_value = sum(1 for r in rows if r["kind"] == "VALUE" and r["need"]) + \
            sum(1 for i in items if i["type"] == "VALUE" and not i["result"])
        sections.append({"task": t.name, "part": part_of(t.name), "printed": not order or t.name in order,
                         "shape": "cards" if rows else "items" if items else "none", "cite": len(cite), "work": len(work), "displays": shows, "open_cite": open_cite,
                         "open_value": open_value, "problems": problems, "rows": rows, "items": items})
        bad += [f"{t.name}: {p}" for p in problems] if (not order or t.name in order) else []
    printed = [s for s in sections if s["printed"]]

    # one value, two Runs: the same (source, file, key) read from different Runs
    seen: dict[tuple, dict[str, list[str]]] = {}
    for s in printed:
        for r in s["rows"]:
            if r["kind"] == "VALUE" and r["key"] and r["run"]:
                seen.setdefault((r["source"], r["file"], r["key"]), {}).setdefault(r["run"], []).append(s["task"])
    for (src, file, key), runs in seen.items():
        if len(runs) > 1:
            where = "; ".join(f"{run} in {', '.join(dict.fromkeys(ts))}" for run, ts in runs.items())
            bad.append(f"one value, two Runs: {src} {file}:{key} is read from {where}")

    # one label, two Results: an older VALUE label bound to different Results; the same estimates in both is a
    # copy (⚠️), different estimates is a conflict (❗)
    labels: dict[str, dict[str, list[str]]] = {}
    for s in printed:
        for i in s["items"]:
            if i["type"] == "VALUE" and i["label"] and i["result"]:
                labels.setdefault(i["label"], {}).setdefault(i["result"], []).append(s["task"])
    for label, results in labels.items():
        if len(results) > 1:
            where = "; ".join(f"{res} in {', '.join(ts)}" for res, ts in results.items())
            found = [estimates(job / ts[0] / res) for res, ts in results.items()]
            units = [one_unit(f) for f in found]
            if all(units) and all(u <= v or v <= u for u in units for v in units):    # one holds the other's
                warn.append(f"one label, two Results, the same estimates: {label} is {where}")
            elif all(units):
                bad.append(f"one label, different estimates: {label} is {where} ({' vs '.join(map(said, found))})")
            else:
                bad.append(f"one label, two Results, not compared: {label} is {where}")

    # one citation key, two entries: the same key with another year or title in two Sections
    keys: dict[str, dict[tuple, list[str]]] = {}
    for s in printed:
        for key, entry in bib_entries(job / s["task"], s["rows"], project).items():
            keys.setdefault(key, {}).setdefault(entry, []).append(s["task"])
    for key, entries in keys.items():
        if len(entries) > 1:
            told = "; ".join(f"{y or 'no year'} \"{t_[:50]}\" in {', '.join(ts)}" for (y, t_), ts in entries.items())
            bad.append(f"one citation key, two entries: {key} is {told}")

    # displays: numbered for the paper, the main text within the venue's limit, none shown twice
    main = [(s["task"], d) for s in printed if s["part"] in ("abstract", "main") for d in s["displays"]]
    appendix = [(s["task"], d) for s in printed if s["part"] == "appendix" for d in s["displays"]]
    numbered = [(f"Display {k}", t, d) for k, (t, d) in enumerate(main, 1)] + \
               [(f"eDisplay {k}", t, d) for k, (t, d) in enumerate(appendix, 1)]
    if max_displays is not None and len(main) > max_displays:
        bad.append(f"too many displays: {len(main)} in the main text, the venue allows {max_displays}")
    shown: dict[str, list[str]] = {}
    for _, t, d in numbered:
        shown.setdefault(re.sub(r"^Display\d+-", "", d), []).append(t)
    warn += [f"one display twice: {d} in {', '.join(ts)}" for d, ts in shown.items() if len(ts) > 1]
    return {"version": job.name, "sections": sections, "displays": numbered, "bad": bad, "warn": warn,
            "open_cite": sum(s["open_cite"] for s in printed), "open_value": sum(s["open_value"] for s in printed),
            "compile_order": bool(order)}


def show(L: dict) -> str:
    out = [f"{L['version']} · one evidence ledger", "",
           f"{'Section':26} {'part':9} {'read from':10} {'CITE':>5} {'VALUE':>5} {'displays':>8} {'open':>6}"]
    for s in L["sections"]:
        part = s["part"] if s["printed"] else "⏸ off"
        out.append(f"{s['task']:26} {part:9} {s['shape']:10} {s['cite']:5} {s['work']:5} {len(s['displays']):8} "
                   f"{s['open_cite'] + s['open_value']:6}")
    if L["displays"]:
        out += ["", "Displays, numbered for the paper:"] + [f"  {n:12} {t:26} {d}" for n, t, d in L["displays"]]
    if L["compile_order"]:
        out += ["", "⏸ off: not in the version's compile order, so not numbered, counted or compared"]
    out += [""] + [f"❗ {b}" for b in L["bad"]] + [f"⚠️ {w}" for w in L["warn"]]
    out.append(f"⬜ open: {L['open_cite']} citations not verified, {L['open_value']} values not landed")
    out.append("✅ the version's evidence agrees across Sections" if not L["bad"] else f"❗ {len(L['bad'])} to fix")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("job", type=Path, help="the version Job folder, jNN_v<MMDD>_<desk>/")
    ap.add_argument("--max-displays", type=int, help="the venue's limit on main-text displays")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not a.job.is_dir() or not tasks(a.job):
        raise SystemExit(f"{a.job}: no tNN_ Tasks; give a version Job folder, jNN_v<MMDD>_<desk>/")
    L = ledger(a.job, a.max_displays)
    print(json.dumps({k: v for k, v in L.items()}, indent=1, default=str) if a.json else show(L))
    return 1 if L["bad"] else 0


if __name__ == "__main__":
    sys.exit(main())
