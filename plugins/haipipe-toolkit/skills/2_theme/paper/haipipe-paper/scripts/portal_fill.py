#!/usr/bin/env python3
"""portal_fill.py · write a send's portal fill page, the shipped generator of the submission Job (JL 261103).

    portal_fill.py <submission Job> [--run <run dir>] [--started-by "<words>"] [--fields F] [--values F] [--out F]

Joins three things and writes <Board>/delivery/<submission Job>/portal-fill.html, one card per portal field with its
value, a Copy button, where the value comes from and its state:

    t02_portal-walk/runs/rNN_*/result/portal-fields.yaml   what the portal asks (the newest Run that has the file)
    t03_portal-fill/portal-values.yaml                     the value decided for each field (the paper's only input)
    delivery/<writing Job>/                                what the build made; the Job's face `for:` names the writing Job

portal-fields.yaml:   portal: <words> · draft_saved: <words> · steps: [{step, fields: [{id, label, kind, required, now,
                      says, options}]}]; `now` is what the portal's draft holds, empty when nothing is there.
portal-values.yaml:   <field id>: {value: text to paste · file: a path under delivery/<writing Job>/ · from_tex: a built
                      Section's Task name (its Abstract, its statement), beside value or alone · ask: what a person must
                      decide · disagree: true, what a read shows and no file can · check: title|words|tables|figures|
                      references · note: one line}. A value that starts "leave " means nothing is to be done.

    ✅ already in the draft   the portal's `now` equals the value, or there is nothing to do
    ✏️ paste or pick this     the value differs from `now`
    📎 upload this file       `file:` exists
    ⬜ no file yet            `file:` or `from_tex:` is not built
    🙋 a person decides       `ask:`, or no value decided yet
    ❗ the portal and the manuscript disagree
                              `disagree: true`; a `check:` whose value, or the portal's `now`, differs from the build;
                              or a packet file the build calls stale

`check:` compares only what the build itself records: title (the Abstract's `### Title`, else paper-build.toml
[paper] title, as build_delivery.py declared_title does), and build-manifest.json's build.main_text_words,
build.main_tables, build.main_figures and build.citations. Without a build the card says so and the state is unchanged.

With --run it also writes that Run's result/ receipt (headline.txt, runtime.yaml). --out writes the page elsewhere;
--fields and --values read other files; so a check can run on a paper without touching it.

This file never opens a network connection, never logs in, never types into a portal, never ticks a declaration and
never submits. A person pastes and a person presses Submit. The page's only script is the Copy button.

The scaffold of the Job is `paper_ladder.py submission`, which calls scaffold() here.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

import yaml

STATES = {"keep": ("✅", "already in the draft", "ok"), "paste": ("✏️", "paste or pick this", "do"),
          "upload": ("📎", "upload this file", "do"), "ask": ("🙋", "a person decides", "ask"),
          "differ": ("❗", "the portal and the manuscript disagree", "bad"), "missing": ("⬜", "no file yet", "bad")}
CHECKS = ("title", "words", "tables", "figures", "references")
CHECK_WORDS = {"title": "title", "words": "main text word count", "tables": "number of main tables",
               "figures": "number of main figures", "references": "number of references"}

TEX = [(r"(?m)^%[^\n]*$", ""), (r"\\section\*?\{[^}]*\}", ""), (r"\\(?:begin|end)\{abstract\}", ""),
       (r"\\keywords\{[^}]*\}", ""), (r"\\url\{([^}]*)\}", r"\1"), (r"\\emph\{([^}]*)\}", r"\1"),
       (r"\\textit\{([^}]*)\}", r"\1"), (r"\\textbf\{([^}]*)\}", r"\1"), (r"\$\\times\$", "×"),
       (r"\$\\approx\$", "≈"), (r"\$\\sim\$", "∼"), (r"\\times", "×"), (r"\\approx", "≈"), (r"\\sim", "∼"),
       (r"\{,\}", ","), (r"\\,", " "), (r"\\ ", " "), (r"--", "–"), (r"~", " "), (r"\$", ""), (r"\\%", "%"),
       (r"\\&", "&"), (r"<!--.*?-->", "")]


def stop(words: str) -> None:
    sys.exit(f"stop: {words}")


def _s(x) -> str:
    """A YAML value as text: an unquoted No is False to YAML and "No" to the portal."""
    if x is True:
        return "Yes"
    if x is False:
        return "No"
    return "" if x is None else str(x)


def plain(tex: str) -> str:
    for a, b in TEX:
        tex = re.sub(a, b, tex, flags=re.S)
    return re.sub(r"[ \t]*\n[ \t]*", " ", tex).replace("  ", " ").strip()


def same(a: str, b: str) -> bool:
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    return bool(a) and norm(a) == norm(b)


def face_of(job: Path) -> Path:
    return job / f"{job.name}.md"


def face_line(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*)$", text)
    return m.group(1).strip() if m else ""


def writing_of(job: Path) -> str:
    """The writing Job this send is for: the face's `for:` line, the same line the paper workbench reads."""
    if not face_of(job).is_file():
        stop(f"{job.name} has no face {job.name}.md: is it a submission Job?")
    name = face_line(face_of(job).read_text(encoding="utf-8"), "for")
    if not name:
        stop(f"{job.name}.md has no `for: <writing Job>` line")
    return name


def fields_file(job: Path) -> Path | None:
    """The newest walk: the highest-numbered Run of t02_portal-walk that holds result/portal-fields.yaml."""
    found = sorted((job / "t02_portal-walk" / "runs").glob("*/result/portal-fields.yaml"))
    return found[-1] if found else None


def values_file(job: Path) -> Path:
    return job / "t03_portal-fill" / "portal-values.yaml"


def built_title(board: Path, writing: str) -> str:
    """The title as the build prints it: the Abstract's `### Title`, else paper-build.toml [paper] title."""
    for page in sorted((board / writing).glob("t00_*/t00_*.md")):
        m = re.search(r"(?ms)^###\s+Title\s*$(.*?)(?=^#{2,4}\s)", page.read_text(encoding="utf-8", errors="replace"))
        if m:
            text = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).replace("**", "").strip()
            if text:
                return " ".join(text.split())
    toml = board / "delivery" / writing / "paper-build.toml"
    if toml.is_file():
        m = re.search(r'(?ms)^\[paper\].*?^title\s*=\s*"([^"\n]*)"', toml.read_text(encoding="utf-8", errors="replace"))
        if m:
            return m.group(1)
    return ""


def built(board: Path, writing: str) -> dict:
    """What the build made: its folder, the facts `check:` compares with, and the packet's state per file."""
    delivery = board / "delivery" / writing
    man = {}
    try:
        man = json.loads((delivery / "build-manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    b = man.get("build") or {}
    facts = {"title": built_title(board, writing), "words": b.get("main_text_words"), "tables": b.get("main_tables"),
             "figures": b.get("main_figures"), "references": b.get("citations")}
    packet = {}
    for up in (man.get("portal") or {}).get("uploads") or []:
        for name in up.get("files") or []:
            packet[name] = up
    return {"writing": writing, "delivery": delivery, "facts": facts, "packet": packet, "manifest": bool(man),
            "words_from": b.get("main_text_words_from")}    # a --pdf-only build: the count may be behind the text


def _agrees(name: str, a: str, want) -> bool:
    if name == "title":
        return same(a, str(want))
    return re.sub(r"[,\s]", "", a) == str(want)


def checked(v: dict, text: str, now: str, b: dict) -> tuple[list, list]:
    """(what disagrees, what could not be checked) for a value's `check:`."""
    name = _s(v.get("check"))
    if not name:
        return [], []
    if name not in CHECKS:
        stop(f"check: {name} is not one of {', '.join(CHECKS)}")
    word, want = CHECK_WORDS[name], b["facts"].get(name)
    if want in (None, ""):
        return [], [f"Not checked: no build says the {word} yet."]
    bad = []
    if text and not _agrees(name, text, want):
        bad.append(f"This value says {text}; the build's {word} is {want}.")
    if now and not _agrees(name, now, want):
        bad.append(f"The portal's draft holds {now}; the build's {word} is {want}.")
    if name == "words" and b.get("words_from"):
        return bad, [f"This count is from {b['words_from']}; the text may have changed. Run a full build before pasting it."]
    return bad, []


def row(f: dict, v: dict, b: dict) -> dict:
    """One field: its value, where it comes from, and its state."""
    now, text, source, path, statement, unbuilt = _s(f.get("now")), _s(v.get("value")), "", None, "", False
    if v.get("from_tex"):
        t = _s(v["from_tex"])
        tex = b["delivery"] / t / "latex" / f"{t}.tex"
        words = plain(tex.read_text(encoding="utf-8")) if tex.is_file() else ""
        source = f"{b['writing']}/{t} (built {dt.datetime.fromtimestamp(tex.stat().st_mtime):%Y-%m-%d %H:%M})" if tex.is_file() \
            else f"{b['writing']}/{t}: not built"
        unbuilt = not tex.is_file() and not text
        statement = words if text else ""
        text = text or words
    bad, unsure = checked(v, text, now, b)
    if v.get("file"):
        path = Path(os.path.normpath(b["delivery"] / _s(v["file"])))     # the writing Job may not be built yet
        source = f"delivery/{b['writing']}/{_s(v['file'])}"
        up = b["packet"].get(path.name) if path.is_file() else None
        if up and up.get("state") == "stale":
            bad.append(f"The build calls this file stale: {up.get('detail', '')}")
        elif up and up.get("state") == "draft":
            unsure.append(f"Built, not approved: {up.get('detail', '')}")
    if bad or v.get("disagree"):
        state = "differ"
    elif path is not None:
        state = "keep" if now and now == path.name else ("upload" if path.is_file() else "missing")
    elif unbuilt:
        state = "missing"
    elif v.get("ask") or not (text or statement):
        state = "ask"
    elif text.startswith("leave ") and now in ("", "unchecked"):     # nothing to do, and nothing done
        state = "keep"
    elif now and (same(text, now) or (statement and same(statement, now))):
        state = "keep"
    else:
        state = "paste"
    ask = _s(v.get("ask")) or ("no value decided yet" if state == "ask" else "")
    return {"f": f, "v": v, "text": text, "statement": statement, "source": source, "path": path, "state": state,
            "now": now, "ask": ask, "found": bad + unsure}


def load_yaml(path: Path) -> dict:
    try:
        got = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        stop(f"{path.name} is not valid YAML: {' '.join(str(e).split())}")
    if not isinstance(got, dict):
        stop(f"{path.name} must be a mapping")
    return got


def survey(job: Path, fields: Path | None = None, values: Path | None = None) -> dict:
    """Read the walk, the values and the build; every field's row, changing nothing (paper_check.py reads this too)."""
    job = job.resolve()
    fields = fields or fields_file(job)
    if fields is None or not fields.is_file():
        stop(f"{job.name} has no walk: t02_portal-walk/runs/rNN_*/result/portal-fields.yaml")
    values = values or values_file(job)
    if not values.is_file():
        stop(f"{job.name} has no {values.name}")
    walk, vals = load_yaml(fields), load_yaml(values)
    if not walk.get("steps"):
        stop(f"{fields.name} has no steps")
    b = built(job.parent, writing_of(job))
    rows, seen = [], set()
    for step in walk["steps"]:
        for f in step.get("fields") or []:
            if not f.get("id") or not f.get("label"):
                stop(f"{fields.name}, {step.get('step')}: a field needs an id and a label: {f}")
            if f["id"] in seen:
                stop(f"{fields.name}: the field {f['id']} is listed twice")
            seen.add(f["id"])
            v = vals.get(f["id"]) or {}
            if not isinstance(v, dict):
                stop(f"{values.name}: {f['id']} must be a mapping, such as {{value: ...}}")
            rows.append({**row(f, v, b), "step": step.get("step", "")})
    return {"job": job, "walk": walk, "fields": fields, "values": values, "rows": rows,
            "unknown": sorted(str(k) for k in vals if k not in seen), "tally": {k: sum(r["state"] == k for r in rows) for k in STATES}}


def venue_name(job: Path) -> str:
    """The face's `venue:`, without the portal's name in parentheses."""
    name = face_line(face_of(job).read_text(encoding="utf-8"), "venue")
    return re.sub(r"\s*\([^)]*\)\s*$", "", name) or "The venue"


SHEET = Path(__file__).resolve().parents[1] / "ref" / "portal-sheet.html"     # JL 261104: "the award level UI", one page
SHORT = {"differ": "portal vs manuscript", "missing": "no file yet", "ask": "you decide"}


def summary(s: dict) -> str:
    """One line for the row that opens this page in the Writing view."""
    n, words = s["tally"], [f'{len(s["rows"])} fields']
    words += [f"{n[k]} {SHORT[k]}" for k in SHORT if n[k]]
    if n["paste"] + n["upload"]:
        words.append(f'{n["paste"] + n["upload"]} to paste or upload')
    return " · ".join(words)


def sheet_row(r: dict, here: Path) -> dict:
    """What the sheet shows for one field; a file opens by its path from the page."""
    f, v, leave = r["f"], r["v"], r["text"].startswith("leave ")
    built_file = r["path"] is not None and r["path"].is_file()
    return {"id": _s(f["id"]), "label": _s(f["label"]), "step": _s(r["step"]), "state": r["state"], "says": _s(f.get("says")),
            "options": [_s(o) for o in f.get("options") or []] if f.get("kind") == "radio" else [], "now": r["now"],
            "value": "" if leave else r["text"], "statement": r["statement"], "leave": r["text"].capitalize() if leave else "",
            "file": r["path"].name if r["path"] is not None else "",
            "href": os.path.relpath(r["path"], here) if built_file else "", "ask": r["ask"], "note": _s(v.get("note")),
            "found": r["found"], "source": r["source"]}


def page(s: dict, here: Path | None = None) -> str:
    """The sheet: ref/portal-sheet.html with this send's rows. It copies and keeps ticks in the browser, never more."""
    e, job = html.escape, s["job"]
    here = here or job.parent / "delivery" / job.name
    data = json.dumps([sheet_row(r, here) for r in s["rows"]], ensure_ascii=False).replace("<", "\\u003c")
    odd = (f'<p class=stop>{e(s["values"].name)} names fields the portal does not list: {e(", ".join(s["unknown"]))}.</p>'
           if s["unknown"] else "")
    fill = {"__KEY__": f"portal-sheet-done-{job.name}", "__SUMMARY__": e(summary(s)), "__VENUE__": e(venue_name(job)),
            "__PORTAL__": e(_s(s["walk"].get("portal"))), "__ODD__": odd,
            "__NOTE__": f"<!-- GENERATED by haipipe-paper scripts/portal_fill.py; edit {e(job.name)}/t03_portal-fill/portal-values.yaml, then rerun. -->"}
    text = SHEET.read_text(encoding="utf-8")
    for key, value in fill.items():
        text = text.replace(key, value)
    return text.replace("__DATA__", data)


def headline(s: dict) -> str:
    n = s["tally"]
    extra = f"; {len(s['unknown'])} values name no field: {', '.join(s['unknown'])}" if s["unknown"] else ""
    return (f"{len(s['rows'])} portal fields: " + ", ".join(f"{n[k]} {STATES[k][1]}" for k in STATES if n[k])
            + f"{extra}; page delivery/{s['job'].name}/portal-fill.html")


def receipt(run_dir: Path, s: dict, started: str, started_by: str) -> None:
    res = run_dir / "result"
    res.mkdir(parents=True, exist_ok=True)
    (res / "headline.txt").write_text(headline(s) + "\n", encoding="utf-8")
    (res / "runtime.yaml").write_text(
        f"run: {run_dir.name}\nstatus: completed\nexit_code: 0\nstarted_at: '{started}'\n"
        f"finished_at: '{dt.datetime.now().astimezone().isoformat(timespec='seconds')}'\nstarted_by: {json.dumps(started_by, ensure_ascii=False)}\n"
        f"worker: haipipe-paper scripts/portal_fill.py\nreads: {s['fields'].name}, {s['values'].name}, the writing Job's build\n",
        encoding="utf-8")


# ── the scaffold: paper_ladder.py submission ──────────────────────────────────────────────────────────
WALK_TICKET = """# {run} · read the portal, read only

A person starts this Run: only a person logs in, and the walk needs a saved draft of this send in the venue's portal.

1. The person opens the portal in their own browser, logs in, and opens the draft.
2. An agent reads each step of the portal, top to bottom, and writes `result/portal-fields.yaml`: every step and field,
   its options, what the portal says about it (`says`) and what the draft holds now (`now`).
3. Nothing is typed, ticked, uploaded, saved or submitted during the walk. Stop at any screen that would change the draft.
4. Keep ids stable across walks: `portal-values.yaml` is keyed by them. Put no link holding a session or a token in the file.

A later walk is a new Run (r02_…); `portal_fill.py` reads the highest-numbered one that has the file.
"""

FILL_TICKET = """#!/usr/bin/env bash
# GENERATED by haipipe-paper scripts/paper_ladder.py submission.
# {run}: write the portal fill page from the fields and portal-values.yaml. Offline; never opens the portal. Rerun after any change.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
JOB_DIR="$(cd "$RUN_DIR/../../.." && pwd)"
TK=""; PY="${{HAIPIPE_PYTHON:-}}"; D="$RUN_DIR"
while [ "$D" != "/" ]; do
  for c in "$D/Tools/plugins/haipipe-toolkit" "$D/plugins/haipipe-toolkit"; do
    [ -z "$TK" ] && [ -d "$c" ] && TK="$c"
  done
  [ -z "$PY" ] && [ -x "$D/.venv/bin/python" ] && PY="$D/.venv/bin/python"
  D="$(dirname "$D")"
done
[ -n "$TK" ] || {{ echo "haipipe-toolkit not found above $RUN_DIR" >&2; exit 2; }}
PY="${{PY:-$(command -v python3)}}"
exec "$PY" "$TK/skills/2_theme/paper/haipipe-paper/scripts/portal_fill.py" "$JOB_DIR" --run "$RUN_DIR" --started-by "${{1:-$(whoami)}}"
"""


def _slug(words: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", words.lower()).strip("-") or "file"


def seed_call(call: Path | None) -> dict:
    """What a venue's call.md can say about the portal's fields: its table rows, read by name, and the word limit."""
    if call is None or not call.is_file():
        return {}
    text, rows = call.read_text(encoding="utf-8", errors="replace"), {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 2 and not set(cells[0]) <= {"-", " ", ":"}:
            rows.setdefault(cells[0].lower(), cells[1])
    seeds = {k: rows[k] for k in ("words", "abstract", "title", "keywords", "main limit", "format", "supplement limit") if rows.get(k)}
    if "words" not in seeds:
        m = re.search(r"(?i)\b(?:up to|at most|not more than|no more than|maximum(?: of)?)\s+[\d,]+\s+words", text)
        if m:
            seeds["words"] = m.group(0)
    head = re.search(r"(?m)^#\s+(.+)$", text)
    if head:
        seeds["name"] = head.group(1).split(" · ")[0].strip()
    return seeds


def upload_slots(board: Path, writing: str) -> tuple[list, str]:
    """[(slot, file or "", note)] from the writing Job's packet: paper-build.toml [portal] and the last build's files."""
    delivery = board / "delivery" / writing
    try:
        import tomllib
        cfg = tomllib.loads((delivery / "paper-build.toml").read_text(encoding="utf-8")).get("portal") or {}
    except (ImportError, OSError, ValueError):
        cfg = {}
    try:
        man = (json.loads((delivery / "build-manifest.json").read_text(encoding="utf-8")).get("portal") or {})
    except (OSError, ValueError):
        man = {}
    folder = str(cfg.get("folder") or man.get("folder") or "portal")
    made = {u.get("slot"): u.get("files") or [] for u in man.get("uploads") or []}
    out = []
    for up in cfg.get("upload") or [{"slot": u.get("slot"), "note": u.get("note")} for u in man.get("uploads") or []]:
        slot, src = str(up.get("slot", "Upload")), str(up.get("from", ""))
        names = made.get(slot) or ([str(up["as"])] if up.get("as") else [])
        if not names and src and not re.search(r"[*?\[]", src):
            names = [Path(src).name]
        note = str(up.get("note") or "")
        if len(names) > 1:
            out += [(f"{slot} {i}", f"{folder}/{n}", note) for i, n in enumerate(names, 1)]
        else:
            out.append((slot, f"{folder}/{names[0]}" if names else "", note))
    return out, ("the writing Job's [portal] packet" if out else "")


def _says(*parts) -> str:
    return " ".join(p for p in parts if p)


def _flow(v: dict) -> str:
    return "{" + ", ".join(f"{k}: {json.dumps(x, ensure_ascii=False)}" for k, x in v.items()) + "}"


def starter(board: Path, writing: str, call_rel: str, seeds: dict) -> tuple[dict, dict]:
    """(portal-fields.yaml as data, portal-values.yaml as {id: value}): the fields most portals ask, each `now` empty;
    a walk of the real portal replaces the fields."""
    slots, _ = upload_slots(board, writing)
    limit = seeds.get("main limit")
    if not slots:
        slots = [("Manuscript", "", ""), ("Figures", "", ""), ("Supplement", "", ""), ("Cover letter", "", "")]
    files, values = [], {}
    for slot, file, note in slots:
        i = f"fi.{_slug(slot)}"
        says = _says(f"Display limit {limit}." if limit and "figure" in slot.lower() else "",
                     f"Format {seeds['format']}." if seeds.get("format") and "figure" in slot.lower() else "",
                     f"Supplement limit {seeds['supplement limit']}." if seeds.get("supplement limit") and "suppl" in slot.lower() else "")
        field = {"id": i, "label": slot, "kind": "upload", "required": "suppl" not in slot.lower(), "now": ""}
        if says:
            field["says"] = says
        files.append(field)
        values[i] = {"file": file} if file else {"ask": "no [[portal.upload]] names this file yet: add it to paper-build.toml, then build"}
        if note:
            values[i]["note"] = note
    facts = built(board, writing)["facts"]
    title = {"id": "ms.title", "label": "Title", "kind": "text", "required": True, "now": ""}
    if seeds.get("title"):
        title["says"] = f"{seeds['title']} ({call_rel})."
    words = {"id": "ms.words", "label": "Word count", "kind": "text", "required": False, "now": ""}
    if seeds.get("words"):
        words["says"] = f"{seeds['words']} ({call_rel})."
    abstract = {"id": "ms.abstract", "label": "Abstract", "kind": "textarea", "required": True, "now": ""}
    if seeds.get("abstract"):
        abstract["says"] = f"{seeds['abstract']} ({call_rel})."
    values["ms.title"] = ({"value": facts["title"]} if facts["title"] else {"ask": "the paper's title; no build says it yet"}) | {"check": "title"}
    values["ms.abstract"] = ({"from_tex": "t00_abstract"} if (board / writing / "t00_abstract").is_dir()
                             else {"ask": "this send's Abstract: name its Task with from_tex, or decide what goes here"})
    values["ms.words"] = ({"value": str(facts["words"])} if facts["words"] else {"ask": "the main text's words; no build says them yet"}) | {"check": "words"}
    steps = [{"step": "1 Files", "fields": files},
             {"step": "2 Title and abstract", "fields": [title, abstract, words]},
             {"step": "3 Authors", "fields": [{"id": "au.authors", "label": "Authors", "kind": "text", "required": True, "now": ""},
                                              {"id": "au.corresponding", "label": "Corresponding author", "kind": "text", "required": True, "now": ""}]},
             {"step": "4 Statements", "fields": [{"id": "st.coi", "label": "Conflicts of interest", "kind": "textarea", "required": True, "now": ""},
                                                 {"id": "st.funding", "label": "Funding", "kind": "text", "required": True, "now": ""},
                                                 {"id": "st.data", "label": "Data sharing", "kind": "textarea", "required": False, "now": ""},
                                                 {"id": "st.ai_use", "label": "Use of AI", "kind": "textarea", "required": False, "now": ""}]},
             {"step": "5 Before Submit", "fields": [{"id": "st.declaration", "label": "Declarations", "kind": "checkbox", "required": True, "now": ""},
                                                    {"id": "af.submit", "label": "Submit", "kind": "button", "required": True, "now": ""}]}]
    values.update({"au.authors": {"ask": "each author's name, degrees, affiliation and email, as the title page prints them"},
                   "au.corresponding": {"ask": "name the corresponding author, as the manuscript does"},
                   "st.coi": {"ask": "each author's conflicts, as the back matter says"},
                   "st.funding": {"ask": "the funding, as the back matter says"},
                   "st.data": {"ask": "the data sharing statement, as the back matter says"},
                   "st.ai_use": {"ask": "the use of AI, as the back matter says"},
                   "st.declaration": {"ask": "a person reads each declaration and ticks it; never an agent"},
                   "af.submit": {"ask": "a person presses Submit, then writes `sent` in delivery/delivery.md"}})
    return ({"portal": "<the portal's name, once the walk has read it>", "draft_saved": "not opened yet: a starter, not a walk",
             "steps": steps}, values)


def scaffold(board: Path, writing: str, mmdd: str, desk: str, venue: str = "") -> tuple[str, dict]:
    """(Job name, {path under the Board: text}): the submission Job for one writing Job, nothing written yet."""
    jobs = sorted(p.name for p in board.glob("j[0-9]*_submission_*") if p.is_dir())
    for name in jobs:
        if face_of(board / name).is_file() and face_line(face_of(board / name).read_text(encoding="utf-8"), "for") == writing:
            stop(f"{name} is already the submission Job of {writing}")
    n = max([20] + [int(name[1:3]) for name in jobs]) + 1
    job = f"j{n:02d}_submission_v{mmdd}_{desk}"

    venues = sorted(d.name for d in (board / "venues").glob("*") if (d / "call.md").is_file())
    if venue and venue not in venues:
        stop(f"venues/{venue}/call.md does not exist; the Board has: {', '.join(venues) or 'none'}")
    slug = venue or (desk if desk in venues else (venues[0] if len(venues) == 1 else ""))
    call_rel = f"venues/{slug}/call.md" if slug else ""
    seeds = seed_call(board / call_rel) if slug else {}
    wface = board / writing / f"{writing}.md"
    said = face_line(wface.read_text(encoding="utf-8"), "venue") if wface.is_file() else ""
    name = said if said and not said.startswith("<") else (seeds.get("name") or "<venue>")

    fields, values = starter(board, writing, call_rel, seeds)
    used = [k for k in seeds if k != "name"]
    seeded = (f"# Seeded from {call_rel}: {', '.join(used) or 'nothing it says matches a field'}.\n" if slug
              else "# No venues/<venue>/call.md chosen, so nothing is seeded from a venue.\n")
    fields_text = ("# STARTER, not a walk: the fields most portals ask. A person-started read of the venue's own portal replaces it\n"
                   "# (this Run's ticket says how; a later walk is a new Run).\n" + seeded
                   + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True, width=120))
    values_text = (f"# The value for each portal field; this file is all a paper keeps. value: text to paste · file: under delivery/{writing}/ · "
                   "from_tex: a built Section's Task · ask: a person decides · disagree: true · check: title|words|tables|figures|references · note: one line\n"
                   + "".join(f"{k}: {_flow(v)}\n" for k, v in values.items()))

    letter = next((d.name for d in sorted((board / writing).glob("t3[0-9]_*")) if d.is_dir() and "cover" in d.name), "")
    t01 = "t01_cover-letter"
    if letter:
        letter_face = (f"# {t01} · Cover letter\n\ntask-type: description\nstate: the words are in the writing Job\nowner: <person>\n"
                       f"words-in: ../../{writing}/{letter}\ngoal: the letter the portal takes, from the writing Job's own letter Task\n"
                       "close: a person has read the built letter\n"
                       f"made-by: the writing Job's build ([coverletter]), delivery/{writing}/\n\n"
                       f"This send's letter words stay in `{writing}/{letter}`, so this Task holds none: the build reads that Task first.\n")
    else:
        letter_face = (f"# {t01} · Cover letter\n\ntask-type: draft\npage-type: section\nfolder-kind: section\nsection_kind: letter\n"
                       f"structure-source: paper/haipipe-paper-draft/ref/generic-template.md\nstate: ⬜ OPEN · plan to write\n"
                       f"story-row: {job} / {t01}\nreader-question: <what the editor asks here>\nentry-state: <what the editor holds coming in>\n"
                       "exit-state: <what the editor holds going out>\nmust-establish: <why this paper, why this journal>\n"
                       "must-refuse: <what it must not overstate>\ntransition-out: <none>\n\n## Opening\n\n<the editor's question, answered in one paragraph>\n\n"
                       "## Content\n\n<the letter's body only: the build adds the date, the addressee, \"Dear …\" and the signature>\n\n"
                       f"## Questions\n\n```yaml\nquestions: []\n```\n\nThe build finds this Task when the writing Job has no letter of its own; "
                       f"to name it, `[coverletter] task = \"../../{job}/{t01}\"` in `delivery/{writing}/paper-build.toml`.\n")
    walk_run, fill_run = "r01_read_portal", "r01_fill_portal"
    files = {
        f"{job}/{job}.md": (
            f"# {job} · the send to {name}\n\nlayer: submission\nfor: {writing}\nvenue: {name}\nstate: open · nothing submitted\n"
            "goal: everything the portal asks beside the manuscript, ready to review and paste\n"
            "close: a person has checked every field on the fill page and pressed Submit in the portal themselves\n"
            f"reads: the writing Job's built files and portal packet{', ' + call_rel if slug else ''}\n\n## Tasks\n\n"
            f"1. [{t01}]({t01}/{t01}.md) · Cover letter: the letter's words\n"
            "2. [t02_portal-walk](t02_portal-walk/t02_portal-walk.md) · Portal walk: what the portal asks\n"
            "3. [t03_portal-fill](t03_portal-fill/t03_portal-fill.md) · Portal fill: each field's value, a Copy button beside it, and what needs a person\n\n"
            f"## Deliverables\n\n- [ ] `delivery/{job}/portal-fill.html` (the fill page)\n"
            "- [ ] Submitted: only a person presses Submit and writes `sent` in `delivery/delivery.md`\n\n"
            "This Job never submits and never types into the portal. Its page comes from the shipped haipipe-paper `scripts/portal_fill.py`; "
            "the Job holds only its values.\n"),
        f"{job}/{t01}/{t01}.md": letter_face,
        f"{job}/t02_portal-walk/t02_portal-walk.md": (
            "# t02_portal-walk · Portal walk\n\ntask-type: description\nstate: ⬜ not walked · the fields are a starter\nowner: <person>\n"
            f"goal: every field {name}'s portal asks\nclose: a read-only walk of this send's own draft, started by a person who logged in\n"
            f"made-by: runs/{walk_run}\n"),
        f"{job}/t02_portal-walk/runs/{walk_run}/run.yaml": (
            f"run: {walk_run}\nkind: soft\nrole: read\nrun_type: main\nsays: 'The real portal tabs of this send, read with a person logged in; "
            "nothing typed, ticked or saved by the agent.'\nhost: a person's own browser\nstarted_by: '<the person who starts the walk>'\n"
            f"ticket: {walk_run}.md\nwrites:\n- result/portal-fields.yaml\n"),
        f"{job}/t02_portal-walk/runs/{walk_run}/{walk_run}.md": WALK_TICKET.format(run=walk_run),
        f"{job}/t02_portal-walk/runs/{walk_run}/result/portal-fields.yaml": fields_text,
        f"{job}/t03_portal-fill/t03_portal-fill.md": (
            "# t03_portal-fill · Portal fill\n\ntask-type: description\nstate: ⬜ not built · nothing submitted\nowner: <person>\n"
            "goal: one page to review before the portal: each field's value, a Copy button, and what a person must decide\n"
            "close: every row is pasted or decided by a person; Submit is pressed by a person, never here\n"
            f"reads: ../t02_portal-walk/runs/rNN_*/result/portal-fields.yaml, portal-values.yaml, the writing Job's portal packet\n"
            f"made-by: runs/{fill_run} (haipipe-paper scripts/portal_fill.py)\nprinted: delivery/{job}/portal-fill.html\n"),
        f"{job}/t03_portal-fill/portal-values.yaml": values_text,
        f"{job}/t03_portal-fill/runs/{fill_run}/run.yaml": (
            f"run: {fill_run}\nkind: hard\nrole: make\nrun_type: main\nsays: 'The portal fill page: every field with its value, a Copy button and its state.'\n"
            f"host: this machine\ntime: seconds\nticket: {fill_run}.sh\nworker: haipipe-paper scripts/portal_fill.py\n"
            f"writes:\n- result/\n- delivery/{job}/portal-fill.html\nstarted_by: '<the person who presses Run>'\n"),
        f"{job}/t03_portal-fill/runs/{fill_run}/{fill_run}.sh": FILL_TICKET.format(run=fill_run),
    }
    return job, files


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("job", type=Path, help="the submission Job folder, jNN_submission_v<MMDD>_<desk>/")
    ap.add_argument("--run", type=Path, help="this Run's folder: also write its result/ receipt")
    ap.add_argument("--started-by", default="", help="who started it, for the receipt")
    ap.add_argument("--fields", type=Path, help="read this portal-fields.yaml, not the newest walk's")
    ap.add_argument("--values", type=Path, help="read this portal-values.yaml, not the Job's")
    ap.add_argument("--out", type=Path, help="write the page here, not to delivery/<submission Job>/portal-fill.html")
    a = ap.parse_args(argv)
    started = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    job = a.job.resolve()
    s = survey(job, a.fields, a.values)
    out = a.out or job.parent / "delivery" / job.name / "portal-fill.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(s, out.parent.resolve()), encoding="utf-8")
    if a.run:
        receipt(a.run.resolve(), s, started, a.started_by)
    print(headline(s))


if __name__ == "__main__":
    main()
