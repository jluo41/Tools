"""Where a paper stands: haipipe-paper's checklist.md, ticked from a paper Board's own files (JL 261031: "here we
should also try to add the checklist.md, so everytime, the haipipe-paper we can have the things like check the
progress"; JL 261101: "what is the final checklist we should have? what is the delivery, and what is the delivery
requirements"; "make the checklist to be a sNN as well").

    python paper_check.py <Paper-Board> [--json]      print it; change nothing
    python paper_check.py <Paper-Board> --write        also tick it into the Board's checklist topic,
                                                       sNN-paper-checklist/, below its GENERATED line

One line per checklist item, by layer (⓪ Layout, ① Plan, ② Explore, ③ Evidence, ④ Writing, ⑤ Delivery): ✅ done,
⏳ under way, ⬜ not yet, 🙋 waits on a person, with what it saw. The Layout lines are what `paper_ladder.py update`
fixes; every other line is the owning skill's work."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def display_plan():
    """haipipe-paper-plan's display_plan module, or None when it is not beside this skill."""
    import importlib.util
    f = Path(__file__).resolve().parents[2] / "haipipe-paper-plan" / "scripts" / "display_plan.py"
    if not f.is_file():
        return None
    spec = importlib.util.spec_from_file_location("display_plan", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

SKIP = ("_archive", "delivery", "history", "passes")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


def field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^\**{re.escape(name)}\**:\**\s*(.+?)\s*$", text)
    return m.group(1).strip().strip("`") if m else ""


def topic(board: Path, pattern: str) -> Path | None:
    return next((d for d in sorted(board.glob("s[0-9]*-*")) if d.is_dir() and re.match(pattern, d.name)), None)


def face(folder: Path) -> Path:
    return folder / f"{folder.name}.md"


def tasks(job: Path | None) -> list:
    return sorted(t for t in job.glob("t[0-9]*_*") if t.is_dir()) if job else []


def status_words(ts: list, good: str) -> tuple:
    """(how many say `good` in their status:, how many there are)."""
    def says(status: str) -> bool:
        """`good` said plainly: a status that starts with ⬜ or not, or says "not drawn", never counts (Paper-Example-C 261101)."""
        if re.match(r"\s*(?:⬜|○|not\b|no\b)", status, re.I):
            return False
        status = re.sub(r"(?i)\bnot\s+(?:yet\s+)?\w+|\bun[a-z]+", "", status)     # "not drawn", "unchecked"
        return bool(re.search(good, status, re.I))
    done = sum(1 for t in ts if says(field(read(face(t)), "status")))
    return done, len(ts)


def mark(done: int, total: int) -> str:
    return "⬜" if total == 0 or done == 0 else "✅" if done == total else "⏳"


def check(board: Path) -> list:
    """[(layer, id, what, mark, seen)] for every checklist item."""
    out = []
    add = lambda layer, i, what, m, seen: out.append((layer, i, what, m, seen))
    bmd = read(board / "board.md")
    project = next((d for d in board.parents if (d / "work").is_dir() or (d / "discovery").is_dir()), None)

    # ① plan
    filled = all(field(bmd, k) and not field(bmd, k).startswith("<") for k in ("spine", "close"))   # a template line starts with <…>
    add("plan", "P1", "The question", "✅" if filled else "⬜", "board.md spine: and close:" + ("" if filled else " not filled"))
    idea = topic(board, r"s\d+-idea")
    add("plan", "P2", "The idea", "✅" if idea else "⬜", idea.name if idea else "no ideation topic")
    story_name = field(bmd, "story-current")
    story = board / story_name if story_name and (board / story_name).is_dir() else topic(board, r"s\d+-story")
    add("plan", "P3", "The story", ("✅" if story_name and story.name == story_name else "⏳") if story else "⬜",
        (story.name + ("" if story_name and story.name == story_name else " (board.md story-current: not set)")) if story else "no story topic")
    sign = re.findall(r"(?m)^\**G\d+:?\**:?\s*⬜.*$", read(face(story))) if story else []
    add("plan", "P4", "The telling chosen", "🙋" if sign else ("✅" if story else "⬜"),
        sign[0].replace("**", "")[:80] if sign else "no open sign line")
    want = re.sub(r"[^a-z0-9]+", "-", field(bmd, "venue").lower()).strip("-")
    calls = sorted((board / "venues").glob("*/call.md"))
    call = next((c for c in calls if want and (c.parent.name == want or want in c.parent.name)), calls[0] if len(calls) == 1 else None)
    add("plan", "P5", "The venue", ("✅" if want else "⏳") if call else "⬜",
        (f"venues/{call.parent.name}/call.md" + ("" if want else " (board.md venue: not set)")) if call
        else ("no call.md" if not calls else "board.md venue: names none of " + ", ".join(c.parent.name for c in calls)))
    for i, what, pat in (("P6", "The data flow", r"s\d+-(?:paper-)?data-?flow"), ("P7", "The paper flow", r"s\d+-paper-(?:work|paper-)?flow"),
                         ("P8", "The related work", r"s\d+-related-work")):
        t = topic(board, pat)
        add("plan", i, what, "✅" if t else "⬜", t.name if t else "no topic")
    dp = display_plan()                       # P9 (JL 261101): each display planned, and within the venue's display rules
    t = topic(board, r"s\d+-paper-displays")
    lines = dp.check(board) if dp and t else []
    bad = [x for m, x in lines if m == "❗"]
    add("plan", "P9", "The display plan", ("⏳" if bad else "✅") if t else "⬜",
        (f"{t.name}: {len(dp.rows(board))} displays, " + (f"{len(bad)} against the venue: {bad[0]}" if bad
         else "within the venue's display rules")) if t else "no s06-paper-displays topic")

    # ② explore
    refs = {"work": set(), "discovery": set()}
    for md in board.rglob("*.md"):
        if any(p in SKIP for p in md.relative_to(board).parts):
            continue
        for kind, block in re.findall(r"\b(work|discovery)/(b\d+_[A-Za-z0-9_.-]+)", read(md)):
            if project and (project / kind / block).is_dir():
                refs[kind].add(block)
    add("explore", "E1", "Work Blocks named", "✅" if refs["work"] else "⬜", ", ".join(sorted(refs["work"])) or "none")
    add("explore", "E2", "Discovery Blocks named", "✅" if refs["discovery"] else "⬜", ", ".join(sorted(refs["discovery"])) or "none")
    rows = []
    stext = read(face(story)) if story else ""
    head = re.search(r"(?m)^\|\s*T\s*\|.*\|\s*state\s*\|.*$", stext)
    if head:
        cols = [c.strip() for c in head.group(0).strip().strip("|").split("|")]
        for line in stext[head.end():].splitlines()[2:]:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(dict(zip(cols, cells)).get("state", ""))
    live = [s for s in rows if not s.startswith("✕")]
    waiting = [s for s in live if s.startswith(("⏳", "⬜"))]
    add("explore", "E3", "The Runs returned", "⬜" if not live else ("⏳" if waiting else "✅"),
        f"{len(live) - len(waiting)} of {len(live)} Roadmap rows done" if live else "no Task Roadmap table")

    # ③ evidence
    jobs = {k: next((j for j in sorted(board.glob("j[0-9]*_*")) if re.search(p, j.name, re.I)), None)
            for k, p in (("display", r"evidence_display|_displays"), ("value", r"evidence_value"), ("cite", r"evidence_cite|citation"))}
    have = [k for k, j in jobs.items() if j]
    add("evidence", "V1", "The evidence Jobs", "✅" if len(have) == 3 else ("⏳" if have else "⬜"),
        ", ".join(j.name for j in jobs.values() if j) or "none")
    for i, what, k, good in (("V2", "Displays drawn", "display", r"\bdrawn\b|accepted"), ("V3", "Values filled", "value", r"filled|checked"),
                             ("V4", "Citations checked", "cite", r"checked|verified")):
        d, n = status_words(tasks(jobs[k]), good)
        add("evidence", i, what, mark(d, n), f"{d} of {n} Tasks" if n else "no Tasks yet")

    # ④ writing
    writing = [j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.match(r"j\d+_(?:writing_)?v\d", j.name)]
    add("writing", "W1", "A writing Job", "✅" if writing else "⬜", ", ".join(j.name for j in writing) or "none")
    signed = written = total = 0
    vnum = lambda f: [int(x) for x in re.findall(r"\d+", f.stem.rsplit("-draft-v", 1)[-1])]
    for j in writing[-1:]:                         # the newest send: the one the paper is being written for
        for t in tasks(j):
            total += 1
            drafts = sorted((t / "draft").glob(f"{t.name}-draft-v*.md"), key=vnum)
            if not drafts:
                continue
            text = read(drafts[-1])
            signed += field(text, "approved").startswith("✅")
            written += "⟦" not in text
    add("writing", "W2", "Plans signed", "🙋" if total and signed < total else mark(signed, total),
        f"{signed} of {total} Sections signed" if total else "no Sections yet")
    add("writing", "W3", "Text written", mark(written, total), f"{written} of {total} Sections with no placeholder left" if total else "no Sections yet")
    built = [j.name for j in writing if (board / "delivery" / j.name / "build-manifest.json").is_file()]
    add("writing", "W4", "Paper built", "✅" if built and len(built) == len(writing) else ("⏳" if built else "⬜"), ", ".join(built) or "not built")
    wait = [r.parent.name for r in board.rglob("runs/r*_collect_*/run.yaml")
            if "_archive" not in r.parts and re.search(r"(?m)^status:\s*waiting", read(r))]
    add("writing", "W5", "Nothing waits on a person", "🙋" if wait else "✅", ", ".join(wait) or "no waiting question set")
    newest = writing[-1] if writing else None
    out[:0] = layout(board, story)
    out.insert(next(k for k, r in enumerate(out) if r[1] == "W1"), ("evidence", "V5", "Numbers agree", *agree(newest)))
    out.extend(delivery(board, newest, call))
    return out


OLD_PAGES = re.compile(r"^(A1-Story|B[abc]-[A-Za-z0-9_-]+|Story\d*[A-Z]?-.*)$")


def layout(board: Path, story) -> list:
    """⓪ Layout: is the folder on the latest paper layout? Each line names the step of `paper_ladder.py update` that
    fixes it, or the skill that owns it."""
    out = []
    add = lambda i, what, m, seen: out.append(("layout", i, what, m, seen))
    old = [d.name for d in sorted(board.iterdir()) if d.is_dir() and OLD_PAGES.match(d.name)] + \
          [f"studio/{d.name}" for d in sorted((board / "studio").glob("*")) if d.is_dir()] if (board / "studio").is_dir() else \
          [d.name for d in sorted(board.iterdir()) if d.is_dir() and OLD_PAGES.match(d.name)]
    add("L1", "Pages are topics and Jobs", "⬜" if old else "✅",
        ("old: " + ", ".join(old) + " (update: migrate_paper.py, topics_paper.py)") if old else "no A1-Story/, B*-/ or studio/ left")
    jobs = [j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir()]
    undated = [j.name for j in jobs if re.match(r"j\d+_v\d{1,2}_", j.name)] + \
              [f"{j.name}/{t.name}" for j in jobs for t in j.glob("S-*") if t.is_dir()]
    versions = [j for j in jobs if re.match(r"j\d+_(?:writing_)?v\d", j.name)]
    add("L2", "Versions dated, Sections tNN", "⬜" if undated else "✅",
        ("old: " + ", ".join(undated[:4]) + " (update: rename_tasks.py)") if undated else
        "every version vMMDD, every Section tNN_" if versions else "no version yet, nothing to rename")
    plain = [j.name for j in jobs if re.fullmatch(r"j\d+_v\d{4}_[A-Za-z0-9-]+", j.name)]
    said = re.findall(r"j\d+_v<MMDD>_<desk>|j\d+_v\d{4}_[A-Za-z0-9-]+", read(board / "board.md"))
    said = [x for x in said if x not in [j.name for j in jobs]]           # a name no folder carries: the face's own words
    add("L3", "Writing Jobs named", "⬜" if plain else "🙋" if said else "✅",
        ("old: " + ", ".join(plain) + " (update: to jNN_writing_vMMDD_<desk>)") if plain else
        (f"board.md still says {said[0]} (haipipe-paper: say jNN_writing_v<MMDD>_<desk>)") if said else
        "jNN_writing_v<MMDD>_<desk>" if versions else "no writing Job yet")
    check_topic = topic(board, r"s\d+-paper-checklist")
    add("L4", "The checklist topic", "✅" if check_topic else "⬜", check_topic.name if check_topic else "none (update makes sNN-paper-checklist)")
    stext = read(face(story)) if story else ""
    flow = topic(board, r"s\d+-(?:paper-)?data-?flow")
    need = [n for n, ok in (("Story's Task Roadmap (T table)", re.search(r"(?m)^\|\s*T\s*\|", stext)),
                            ("Story's Discovery Roadmap (D table)", re.search(r"(?m)^\|\s*D\s*\|", stext)),
                            ("data flow's -drawing.yaml", flow and list(flow.glob("*-drawing.yaml")))) if not ok]
    add("L5", "Faces the views read", "🙋" if need else "✅",
        ("missing: " + "; ".join(need) + " (haipipe-paper-story, haipipe-paper-plan)") if need else "T and D tables, the data-flow map")
    return out


def agree(job) -> tuple:
    """V5: haipipe-paper-evidence's ledger of the newest writing Job; ❗ findings are what disagree."""
    if job is None:
        return "⬜", "no writing Job"
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "haipipe-paper-evidence" / "scripts"))
        import evidence_ledger
        L = evidence_ledger.ledger(job)
    except Exception as e:                       # the ledger is another skill's; its failure is a line, not a crash
        return "⬜", f"the ledger did not read ({type(e).__name__})"
    n = lambda v: len(v) if isinstance(v, (list, tuple)) else int(v or 0)
    bad, warn = n(L.get("bad")), n(L.get("warn"))
    return ("⏳" if bad else "✅"), (f"{bad} to fix, {warn} to look at (evidence_ledger.py)" if bad else
                                    f"no number disagrees{f', {warn} to look at' if warn else ''}")


def delivery(board: Path, job, call) -> list:
    """⑤ Delivery: the package of the newest send and its requirements: the files (haipipe-paper-assemble's required
    outputs), the venue's desk rules (venues/<venue>/call.md), clean text, the build's readiness (ref/
    submission-readiness.md), then the person's reading pass, approval and send."""
    out = []
    add = lambda i, what, m, seen: out.append(("delivery", i, what, m, seen))
    man = {}
    if job is not None:
        f = board / "delivery" / job.name / "build-manifest.json"
        try:
            man = json.loads(read(f)) if f.is_file() else {}
        except ValueError:
            man = {}
    outs = {k: v for k, v in (man.get("outputs") or {}).items() if v}   # an output a profile does not make is empty
    here = lambda key: bool(outs.get(key)) and (board / "delivery" / job.name / outs[key]).is_file()
    main = [k for k in ("pdf", "docx") if here(k)]
    add("D1", "The manuscript", "✅" if len(main) == 2 else ("⏳" if main else "⬜"),
        " and ".join({"pdf": "PDF", "docx": "Word"}[k] for k in main) + " built" if main else "not built (haipipe-paper-assemble)")
    sup = [k for k in outs if "supplement" in k]
    add("D2", "The supplement", "✅" if not sup or all(here(k) for k in sup) else "⏳",
        ", ".join(Path(outs[k]).name for k in sup) if sup else "none declared")
    letters = [t for t in (job.glob("t[0-9]*_*letter*") if job else []) if t.is_dir()]
    cl = man.get("cover_letter") or {}            # build_delivery.py records the letter apart: cover_letter.outputs
    cl_out = {k: v for k, v in (cl.get("outputs") or {}).items() if v}
    built_letter = [v for v in cl_out.values() if (board / "delivery" / job.name / v).is_file()] if job else []
    built_letter += [outs[k] for k in outs if "letter" in k and here(k)]
    add("D3", "The cover letter", ("✅" if cl.get("ready", True) else "⏳") if built_letter else ("⏳" if letters else "⬜"),
        (" and ".join(Path(v).name for v in built_letter) + ("" if cl.get("ready", True) else " (built; its checks not all passed)"))
        if built_letter else (letters[0].name + " (not built)") if letters else "no letter Task in the writing Job")
    ctext = read(call) if call else ""
    limit = re.search(r"(?mi)^\|\s*words\s*\|\s*(?:up to|not more than|maximum)?\s*([\d,]+)", ctext) or \
        re.search(r"(?i)\b(?:up to|at most|not more than|no more than|maximum(?: of)?)\s+([\d,]+)\s+words", ctext)   # or in a sentence
    words = man.get("build", {}).get("main_text_words")
    issues = []
    if limit and words and words > int(limit.group(1).replace(",", "")):
        issues.append(f"{words} words, limit {limit.group(1)}")
    unknown = ctext.count("UNKNOWN")
    if unknown:
        issues.append(f"{unknown} desk rules not found yet")
    venue_slug = call.parent.name if call else ""
    prof = man.get("venue_profile", "")
    if prof and venue_slug and not set(re.split(r"[-_]", prof)) & set(re.split(r"[-_]", venue_slug)):
        issues.append(f"built with the {prof} profile")
    if call and not limit:
        issues.append("no word limit read from call.md (a `| words | up to N |` row, or \"at most N words\")")
    if call and words is None:
        issues.append("not built, so the word count is unknown")
    add("D4", "The venue's desk rules", ("⏳" if issues else "✅") if call else "⬜",
        ("; ".join(issues) if issues else f"within venues/{venue_slug}/call.md") if call else "no call.md")
    secs = sorted((board / "delivery" / job.name / "latex" / "sections").glob("*.tex")) if job else []   # the build's own copy
    marks = [t.stem for t in secs if "⟦" in read(t)]
    owed = [t.stem for t in secs if "TOADD" in read(t)] + list(man.get("draft_citations") or []) + list(man.get("unresolved_refs") or [])
    add("D5", "Clean text", "⬜" if not secs else ("⏳" if marks else "✅"),
        (f"placeholders in {', '.join(marks[:4])}" if marks else "no ⟦…⟧ left") if secs else "no LaTeX Sections yet")
    add("D6", "Citations verified", "⬜" if not secs else ("⏳" if owed else "✅"),
        (f"owed: {', '.join(map(str, owed[:4]))}" if owed else "no TOADD, every key resolves") if secs else "no LaTeX Sections yet")
    status = man.get("submission_readiness", {}).get("status") or man.get("status", "")
    blockers = man.get("submission_readiness", {}).get("blockers") or []
    add("D7", "The build is ready", "✅" if status and status != "DRAFT" else ("⏳" if man else "⬜"),
        (f"DRAFT: {len(blockers)} blockers (ref/submission-readiness.md)" if status == "DRAFT" else status) if man else "not built")
    portal = man.get("portal") or {}                  # 0.13.0 engine: the files uploaded to the portal as they are
    ups = portal.get("uploads") or []
    off = [u["slot"] for u in ups if u.get("state") in ("missing", "stale")]
    unapproved = [u["slot"] for u in ups if u.get("state") == "draft"]
    add("D8", "The portal packet", ("✅" if not off and not unapproved else "⏳") if ups else "⬜",
        (f"{portal.get('ready', 0)} of {len(ups)} slots ready in {portal.get('folder', 'portal')}/portal.md"
         + (f"; missing or stale: {', '.join(off[:3])}" if off else "")
         + (f"; {len(unapproved)} built, not approved" if unapproved else "")) if ups
        else "no [portal] in paper-build.toml (haipipe-paper-assemble § The portal packet)")
    add("D9", "Read and approved", "🙋", "a person reads the built paper and approves this exact build (G4)")
    sent = [ln for ln in read(board / "delivery" / "delivery.md").splitlines()
            if job is not None and job.name in ln and re.search(r"\|\s*sent\s*\|", ln)]
    add("D10", "Sent", "✅" if sent else "🙋", sent[-1].strip("| ").split("|")[0].strip() + " sent" if sent
        else "only a person marks it sent (delivery/delivery.md)")
    return out


GENERATED = ("<!-- GENERATED by haipipe-paper scripts/paper_check.py --write: the checklist ticked from the Board's own "
             "files. Rerun it; never edit below this line. -->")
LAYERS = {"layout": "⓪ Layout", "plan": "① Plan", "explore": "② Explore", "evidence": "③ Evidence", "writing": "④ Writing",
          "delivery": "⑤ Delivery"}


def lines(rows: list) -> str:
    """The checklist as Markdown: a heading per layer, one line per item."""
    out, last = [], ""
    for layer, i, what, m, seen in rows:
        if layer != last:
            out += ["", f"### {LAYERS[layer]}", ""]
            last = layer
        out.append(f"- {m} **{i} · {what}**: {seen}")
    return "\n".join(out).strip() + "\n"


def write(board: Path, rows: list) -> Path | None:
    """Tick the checklist into the checklist topic's face, below its GENERATED line; what is above stays as written."""
    t = topic(board, r"s\d+-paper-checklist")
    if t is None:
        return None
    f = face(t)
    text = read(f)
    head = text.split(GENERATED)[0] if GENERATED in text else text
    head = re.sub(r"(?:\s*\nChecklist\n-+\s*)+$", "", head.rstrip()).rstrip()      # its own heading, however many reruns left
    stamp = sum(1 for r in rows if r[3] == "✅"), len(rows)
    f.write_text(f"{head}\n\n\nChecklist\n---------\n\n{GENERATED}\n\n{stamp[0]} of {stamp[1]} done.\n\n{lines(rows)}",
                 encoding="utf-8")
    return f


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("board", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true", help="also tick it into the Board's sNN-paper-checklist topic")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        sys.exit(f"stop: {board.name} has no board.md")
    rows = check(board)
    if a.json:
        print(json.dumps([dict(zip(("layer", "id", "what", "mark", "seen"), r)) for r in rows], ensure_ascii=False, indent=1))
        return 0
    last = ""
    for layer, i, what, m, seen in rows:
        if layer != last:
            print(f"\n{LAYERS[layer]}")
            last = layer
        print(f"  {m} {i} {what:<28} {seen}")
    if a.write:
        f = write(board, rows)
        print(f"\nticked into {f.relative_to(board)}" if f else "\nno sNN-paper-checklist topic: paper_ladder.py update makes it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
