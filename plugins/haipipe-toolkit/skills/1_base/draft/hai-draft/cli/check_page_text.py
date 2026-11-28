"""check_page_text.py: the checks that read one Page's text and its plan files.
Sections, sentences, fences, file paths, generated blocks, comments, feedback coverage; check_face calls them."""
import collections
import json
import re
from pathlib import Path

from cli.check_common import (ERROR, HERE, WARN, _plan_rel, outside_checkout,  # noqa: E402
                              section_text)
from src.outline_version import plan_dir, plan_files, record_path  # noqa: E402
from src.common import AIM_STATE_RE, aim_ids  # noqa: E402
from src.page_context import audit_related_rows  # noqa: E402
from src.outline_version import latest_outline  # noqa: E402
from src.item_table import bullets as typed_evidence_bullets, evidence_none_targets  # noqa: E402
from src.feedback import (rounds as _rounds, parse_round, register_path,  # noqa: E402
                          register_ids, routed_rows)


RETIRED_SECTIONS = {
    # section name -> why it went, and what does the job now
    "Boundary": "JL 260731; what a page covers is the Opening's job",
    "Question": "renamed to `## Opening` (260731)",
    "Items to Finish": "renamed to `## Aims` (260731)",
    "Where we are": "renamed to `## States` (260731), then merged into `## Aims` (260819)",
    # The 260819 merge named only the OLD name above, so `RETIRED_SECTIONS.get`
    # returned None for the CURRENT one and the comment at the head of this file
    # ("`retired-section` reports it") described behaviour the table did not
    # have. 1,026 lines of a retired section passed silently on the MISQ paper
    # board for eleven days (JL 260830).
    "Files": "moved to `draft/records/<stem>-files.md` (JL 260831, QPf12 row 3): one "
             "`### F<n> · <what it is for>` record per file with `Path` and `Role`; a "
             "Related Board Page is a record with `Role: related` and its row verbatim under it",
    "States": "merged into `## Aims` (260819): one Aim row carries its tick, "
              "its `Done when:` test and its `Now:` fact. Live asks "
              "(`### Needs JL · tick these`) become that Aim's `Now:` line",
}


def check_fence_balance(text, name, rep):
    """An unclosed FENCE swallows the rest of the page, silently.

    Everything after it renders as code: Aims, States, Files and Log come out
    as raw markdown inside one grey box. The page still builds, still passes
    every other check, and still reports 0 errors. JL found it by LOOKING at
    the rendered `QBt5-for-value` on 260807, where a slice edit had removed one
    fence's opening line and left its closing one, so parity was inverted from
    that point to the end of the file.

    Cheap to check and impossible to catch by reading, which is what earns it a
    rule: the damage shows at the BOTTOM of the page and the cause is in the
    middle.
    """
    opens, state, managed = [], False, False
    for i, line in enumerate(text.split("\n"), 1):
        st = line.lstrip()
        # MANAGED SPANS ARE NOT THIS PAGE'S PROSE. A generated mirror page
        # carries another unit's bytes verbatim, fences included, so counting
        # them made parity odd on two pages that render perfectly. Measured
        # 260807: the rule's first version flagged Skill-6 and Skill-8, and
        # both were checked in the RENDERED html and found intact.
        if st.startswith("<!--") and "haipipe:" in st:
            managed = ":start" in st
            continue
        if managed:
            continue
        if st.startswith(FENCE):
            state = not state
            if state:
                opens.append(i)
            elif opens:
                opens.pop()
    if state and opens:
        rep.add(ERROR, "fence-unclosed", "%s:%d" % (name, opens[-1]),
                "a fence is never closed, so every section below it renders as "
                "code. The page still builds and every other check still "
                "passes, which is why this one exists.")


def check_content_attribution(text, name, rep):
    """The OFFICIAL-DOCUMENT rule: Content states rules, never attributions.

    Ruled 260820, reading the compiled PDF: "don't say too much 'JL' or
    'YYMMDD', this is the official document." A bare six-digit date code or a
    person's name as authority inside `## Content` (or the Diagram caption) is
    a Log row wearing prose: the reader of the document cannot parse it and
    should not have to. Who and when live in `## Log`, `## Discussion`, and
    tick lines. Fenced blocks are skipped, because a fence may carry a frozen
    transcription another pen owns; the CHECK judge reads those by eye.
    New authority names join the name pattern here when the board gains them.
    """
    body = re.search(r"(?ms)^## (?:Content|Outline|Diagram)\b.*?(?=^## (?!Content|Outline|Diagram)|\Z)",
                     text)
    spans = re.findall(r"(?ms)^## (?:Content|Outline|Diagram)\b[^\n]*\n(.*?)(?=^## |\Z)",
                       text)
    if not spans:
        return
    date_re = re.compile(r"\b26[01]\d{3}\b")
    name_re = re.compile(r"\bJL\b")
    offset = 0
    for span in spans:
        start = text.index(span, offset)
        offset = start + len(span)
        base = text[:start].count("\n") + 1
        fenced = False
        for i, line in enumerate(span.split("\n")):
            st = line.lstrip()
            if st.startswith(FENCE):
                fenced = not fenced
                continue
            if fenced or st.startswith(">") or st.startswith("<!--"):
                continue
            hits = []
            if date_re.search(line):
                hits.append("a bare date code")
            if name_re.search(line):
                hits.append("a person named as authority")
            if hits:
                rep.add(WARN, "content-attribution", "%s:%d" % (name, base + i),
                        "Content is the official document and this line carries "
                        + " and ".join(hits) + "; state the rule itself and move "
                        "the who/when to a Log row (hai-draft-writing, the "
                        "present-tense rule).")


_NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+|\b\d+\.\d+\b|\b\d+(?:\.\d+)?\s*(?:million|thousand|billion|percent|%)")


def _latest_approved_plan(path):
    """Return the newest plan only when it carries ``approved: ✅``."""
    o = plan_dir(path.parent)
    plan = latest_outline(o, path.stem)
    if plan is None:
        return None
    approved = bool(re.search(
        r"(?m)^approved:\s*✅",
        plan.read_text(encoding="utf-8", errors="replace"),
    ))
    return plan if approved else None


def _latest_plan_approved(path):
    """Compatibility predicate for the approved-plan gate."""
    return _latest_approved_plan(path) is not None


def check_section_sentences(text, path, name, rep):
    """The CONTENT/WRITE contract on a Section Page using an approved plan
    (hai-draft-writing §①): every Content sentence ends `<!-- realizes:
    C.P.B -->` (`sentence-without-realizes`), and every sentence that carries a
    number (a comma-grouped count, a decimal, `8.69 million`, a percentage) has
    a `> Value:` lane under it (`number-without-lane`). Gated on the approved
    plan because a page with no agreed slot plan has nothing to realize; the
    pages written before the rule stay silent until their next CONTENT/WRITE."""
    if path is None or not re.search(r"(?m)^page-type:\s*section\b", text[:800]):
        return
    plan = _latest_approved_plan(path)
    if plan is None:
        return
    plan_text = plan.read_text(encoding="utf-8", errors="replace")
    item_types = collections.defaultdict(set)
    for _item, target, _head, item_type, _expected, _acceptance, _folded in typed_evidence_bullets(plan_text):
        item_types[target].add(item_type)
    no_evidence = evidence_none_targets(plan_text)
    spans = re.findall(r"(?ms)^## Content\b[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not spans:
        return
    span = spans[0]
    start = text.index(span)
    base = text[:start].count("\n") + 1
    lines = span.split("\n")
    fenced = False
    for i, line in enumerate(lines):
        st = line.strip()
        if st.startswith(FENCE):
            fenced = not fenced
            continue
        if fenced or not st or st.startswith((">", "#", "<!--", "(", "**", "-", "|", "!", "["  )):
            continue
        core = re.sub(r"<!--.*?-->", "", st).strip()
        if not re.search(r"[.?!][\"')\]]*(\s*\[[^\]]*\])?\s*$", core):
            continue                      # a title line, a keyword list: not a sentence
        if "realizes:" not in st:
            rep.add(WARN, "sentence-without-realizes", "%s:%d" % (name, base + i),
                    "a Section sentence drafted from an approved plan names its slot: "
                    "end it with `<!-- realizes: C<n>.P<m>.B<k> -->` (hai-draft-writing §①)")
        realization = re.search(r"<!--\s*realizes:\s*(C\d+\.P\d+\.B\d+[a-z]*)\s*-->", st)
        target = realization.group(1) if realization else ""
        has_citation = bool(re.search(r"\\cite(?:p|t)?\*?(?:\[[^\]]*\])*\{[^}]+\}", core))
        if target and has_citation and "CITE" not in item_types.get(target, set()):
            detail = ("explicitly declares Evidence none" if target in no_evidence
                      else "has no CITE Evidence Item")
            rep.add(WARN, "citation-without-bullet-evidence", "%s:%d" % (name, base + i),
                    "%s carries a citation but %s; return that Bullet to OUTLINE/SHAPE"
                    % (target, detail))
        probe = re.sub(r"\[[^\]]*\]|\\cite[pt]?\{[^}]*\}", "", core)
        has_value = bool(_NUM_RE.search(probe))
        if target and has_value and "VALUE" not in item_types.get(target, set()):
            detail = ("explicitly declares Evidence none" if target in no_evidence
                      else "has no VALUE Evidence Item")
            rep.add(WARN, "value-without-bullet-evidence", "%s:%d" % (name, base + i),
                    "%s carries a concrete value but %s; return that Bullet to OUTLINE/SHAPE"
                    % (target, detail))
        if has_value:
            j, has_lane = i + 1, False
            while j < len(lines) and lines[j].strip().startswith(">"):
                if re.match(r"^>\s*Value:", lines[j].strip()):
                    has_lane = True
                    break
                j += 1
            if not has_lane:
                rep.add(WARN, "number-without-lane", "%s:%d" % (name, base + i),
                        "this sentence states a number and no `> Value:` lane follows it; "
                        "write the source Page, bracket or Evidence Item and its state "
                        "(hai-draft-writing §①)")


def check_retired_sections(text, name, rep):
    """A section JL retired must not come back, and must not merely be ALIASED.

    `src/common.py` still maps the old names so old pages keep rendering. That
    kindness is exactly why 45 of 55 pages sat on the pre-260731 vocabulary for
    two days while a skill claimed they had all been converted: the render
    looked right, so nothing ever said otherwise. A rename the renderer forgives
    is a rename no one finishes. This check is what makes it finishable.
    """
    for i, line in enumerate(text.split("\n"), 1):
        head = line.strip()
        if not head.startswith("## "):
            continue
        why = RETIRED_SECTIONS.get(head[3:].strip())
        if why:
            # WARN, not ERROR: ERROR is reserved for silent DATA LOSS
            # (`duplicate-section`). This is visible drift, and four sibling
            # boards carry 217 rows of it that are not this sweep's to fix.
            rep.add(WARN, "retired-section", f"{name}:{i}",
                    f"`{head}` was retired: {why}")


def check_duplicate_sections(text, name, rep):
    """A repeated `## ` heading SILENTLY DISCARDS everything under the first.

    `split_sections` in `src/parse.py` builds a dict, so the later block wins
    and the earlier one never reaches the render. Nothing reported it: the
    page looks whole in the editor and is short on the page. QB2a carried two
    `## Where we are` headings for two days, and roughly 4.6 KB of dated
    post-mortems under the first had never been seen by anyone (found by a
    fresh-context agent on 260802, not by any check).

    This is an ERROR rather than a warning because it is silent data loss.
    """
    seen, fence = {}, False
    for i, ln in enumerate(text.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^##\s+(\S.*?)\s*$", ln)
        if not m:
            continue
        head = m.group(1)
        if head in seen:
            rep.add(ERROR, "duplicate-section", f"{name}:{i}",
                    f"`## {head}` also at line {seen[head]}; the render keeps "
                    "only the LAST one and silently drops everything under the "
                    "first (QB4 §8.2.2)")
        else:
            seen[head] = i


_FRAMES = {}


def _canvas_frames(board_dir):
    """Frame names in the board's own `board.excalidraw`, cached per board."""
    root = Path(board_dir)
    for _ in range(4):                      # a page sits in a group folder
        scene = root / "board.excalidraw"
        if scene.exists():
            break
        root = root.parent
    else:
        return None
    key = str(scene)
    if key not in _FRAMES:
        try:
            data = json.loads(scene.read_text(encoding="utf-8"))
            _FRAMES[key] = {e.get("name", "") for e in data.get("elements", [])
                            if e.get("type") == "frame"}
        except Exception:
            _FRAMES[key] = None
    return _FRAMES[key]


def check_canvas_frames(text, name, rep, board_dir=None):
    """A `&frame=<id>` that names no frame in `board.excalidraw` links to nothing.

    `serve_frame()` 404s, but the page still LOOKS like it has a drawing, so the
    gap only shows when someone clicks. Three fresh-context agents hit this on
    260802 from three different pages, which is how it got measured at all.
    """
    frames = _canvas_frames(board_dir)
    if not frames:
        return
    for i, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith(("#", ">")):
            continue
        for m in re.finditer(r"[&?]frame=([A-Za-z0-9_-]+)", line):
            fid = m.group(1)
            if fid not in frames:
                rep.add(WARN, "dead-canvas-frame", f"{name}:{i}",
                        f"`frame={fid}` names no frame in `board.excalidraw`, "
                        "so the link 404s (QB4 §2.7)")


def _files_record_text(path):
    """The page's draft/records/<stem>-files.md, with each `- **Path**: `x`` row
    rewritten as a bare `- `x`` row so the Files path checks read it unchanged."""
    if not path:
        return ""
    p = Path(path); f = record_path(plan_dir(p.parent), p.stem, "files")
    if not f.is_file():
        return ""
    t = f.read_text(encoding="utf-8", errors="replace")
    return re.sub(r"(?m)^(\s*[-*])\s+\*\*Path\*\*:\s*", r"\1 ", t)

def check_file_paths(text, name, rep, board_dir=None, path=None):
    """Every backticked path in `## Files` must resolve (JL 260802).

    Files is the action map, and a stale path is worse than no path: the
    reader only discovers it is dead after following it. Prose can be wrong
    and still read as prose; a path is either right or a dead end. QB4 itself
    carried four dead ones by 260802, because `build.py` and `stage.py` moved
    into `cli/` and `assets/board.css` was split into `assets/css/*.css`.

    Resolved against the ENGINE dir first, then the board folder, then the
    repo root, because a Files row may point at any of the three.
    """
    block = section_text(text, "Files") or ""
    # Since 260831 the file map lives in draft/records/<stem>-files.md (JL, QPf12 row 3);
    # its `- **Path**: `x`` rows are checked with the same teeth as a page's rows.
    block = block + "\n" + _files_record_text(path)
    roots = [HERE, HERE.parent]
    if board_dir:
        d = Path(board_dir)
        # a Files row may be written relative to the PAGE's own folder, to the
        # board root, or to the repo root; all three are legitimate and in use.
        # Climb to the board root instead of assuming it is one level up: a
        # folded page (`<name>/<name>.md`, JL 260815) sits one level deeper,
        # and the fixed `[d, d.parent]` silently dropped board-relative
        # resolution for every folded page.
        roots.append(d)
        for p in d.resolve().parents:
            roots.append(p)
            if (p / "board.md").is_file():
                break
        root = next((p for p in d.resolve().parents
                     if (p / "pyproject.toml").is_file()), None)
        if root:
            roots.append(root)
    # EVERY backticked path in the row, not only the first. A row written
    # `- `a.py` · `b.py`` had its second path silently unchecked, which is how
    # QB5 reported one dead path while carrying five (260802).
    for row in re.finditer(r"(?m)^\s*[-*]\s+(`[^`]+`(?:\s*[·,]\s*`[^`]+`)*)", block):
        for m in re.finditer(r"`([^`]+)`", row.group(1)):
            raw = m.group(1).strip()
            for cand in raw.split(" · "):
                cand = cand.strip().strip("`")
                if not cand or " " in cand or not re.search(r"[./]", cand):
                    continue
                if any((r / cand).exists() for r in roots):
                    continue
                if "*" in cand or "<" in cand or ">" in cand:
                    # a glob (assets/css/*.css) or an angle-bracketed placeholder
                    # (<path/to/thing.py>) names a shape, not a file. The template
                    # is copied for every new page, so its example rows must not
                    # arrive pre-broken (JL 260802).
                    continue
                if cand.split("/")[0].startswith("."):
                    # runtime state (`.hai-board/activity.sqlite3`) exists
                    # only after the server has run; its absence proves nothing
                    continue
                if board_dir and outside_checkout(Path(board_dir), cand):
                    rep.add(WARN, "outside-checkout", f"{name} · Files",
                            f"`{cand}` lives outside this checkout")
                    continue
                rep.add(WARN, "dead-file-path", f"{name} · Files",
                        f"`{cand}` does not resolve from the engine, the board, "
                        "or the repo root (QB4 §6.3.1)")


def check_related_board_pages(path, name, text, rep):
    """Validate the typed, scoped Page links under Files (QB4 §6.4).

    Ordinary Files rows may point anywhere the work continues. A Related Board
    Pages row is narrower: its target must be a real Page on this Board, its
    visible Page id must agree with that source, and its requested Content scope
    must exist. Those facts are deterministic, so malformed context never waits
    for an agent to discover it during CONTEXT, OUTLINE, EVIDENCE, CONTENT, or CHECK.
    """
    for finding in audit_related_rows(path, text):
        level = ERROR if finding.level == "ERROR" else WARN
        rep.add(level, finding.code, f"{name}:{finding.line}", finding.message)


def check_comment_form(text, name, rep):
    """A sentence comment is written `> Comment WHO …` (JL 260802).

    The bare-initial form `> JL: …` still RENDERS, so nothing already written
    breaks, but it is not the form to write: beside `> Citation:` and
    `> Value:` a pair of initials tells a newcomer nothing about what the row
    is. Only Content is checked. `## Discussion` keeps `> JL:` / `>> CC0726:`
    deliberately: that is a THREAD with nested replies, a different grammar in
    a different section, and 156 rows across the boards use it.
    """
    content = section_text(text, "Content") or ""
    fence = False
    for i, ln in enumerate(content.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^>\s*([A-Z]{1,4}\d{0,4})\s*[「\"]?.*?[:：]", ln)
        # `Card` joins the named lanes (JL 260802). Without it, `> Card SPAN
        # of words: …` matched the bare-initials shape as author "C", so every
        # span card on the board reported itself as a legacy comment.
        if m and not re.match(r"^>\s*(Citation|Value|Display|Supporting Run|Check|Q-consumer|"
                              r"Link|Source|Note|Comment|Card)\b", ln, re.I):
            rep.add(WARN, "old-comment-form", f"{name} · Content",
                    f"`> {m.group(1)}:` is the legacy sentence-comment form; "
                    f"write `> Comment {m.group(1)} …` (QB4 §3.3.3)")


# One marker pair per generator, so two blocks can share a page: `form:` is
# section-stats.py, `units:` is dash.py, `evidence:` is evidence.py. They shared
# one pair until 260806, when dash.py silently deleted both other blocks from
# three pages on its first run. The checker reads whichever names it finds.
GEN_BEGIN = re.compile(r"^# --- (\w+):begin \(generated\) ---$", re.M)
GEN_MEASURED = re.compile(r"MEASURED\s+(20\d\d-\d\d-\d\d|\b2\d{5}\b)")
GEN_REGEN = re.compile(r"(?m)^\s*regenerate:\s*(\S+)")
ANY_DATE = re.compile(r"(20\d\d-\d\d-\d\d|\b2\d{5}\b)")


def _ymd(token):
    """`260727` and `2026-07-27` are both in use; compare them as one shape."""
    t = token.replace("-", "")
    return t[2:] if len(t) == 8 else t


def check_generated_block(text, name, rep, path=None):
    """A measured block must say when it was measured, and not be older than
    the page it measures.

    Every other page type closes on an event: a display is accepted, a stage
    passes its gate, a skill's unit ships. A measured block has no such moment,
    which is why `for-dashboard` failed the admission test's fourth question on
    260806. What it has instead is FRESHNESS, and freshness is checkable, so the
    thing that would have been a closing rule becomes this.

    The page's own newest Log date is the reference rather than the file's
    mtime, because a clone resets every mtime and the Log travels with the file.

    Measured on the MISQ board the day the rule was written: seven of eight
    section pages carried a block measured 2026-07-27 whose page had logged work
    through 260803, and the S-Main dashboard was still reporting a section that
    had been archived. Its own prose is the argument for this check: a wrong
    measurement is worse than none, because it reads as measured.
    """
    blocks = []
    for m in GEN_BEGIN.finditer(text):
        tag = m.group(1)
        tail = text[m.end():].split(f"# --- {tag}:end ---", 1)
        blocks.append((tag, tail[0]))
    if not blocks:
        return
    # The Log may live on the page OR, since workbench-task-draft 0.16.0, in
    # `draft/records/<stem>-log.md`. Reading only the page made this check lose its
    # input the moment a page migrated: `latest` went "" for ever and a stale
    # form block could never be reported again. A finding count dropping because
    # a check lost its input is worse than the finding (field test, JL 260830).
    log = section_text(text, "Log")
    if path is not None:
        side = record_path(plan_dir(path.parent), path.stem, "log")
        if side.exists():
            log += "\n" + side.read_text(encoding="utf-8", errors="replace")
    latest = max((_ymd(d) for d in ANY_DATE.findall(log)), default="")
    for tag, block in blocks:
        _one_generated_block(tag, block, latest, name, rep)


def _one_generated_block(tag, block, latest, name, rep):
    stamp = GEN_MEASURED.search(block)
    if not stamp:
        rep.add(WARN, "generated-block-undated", name,
                "a generated block carries no `MEASURED <date>` line, so nothing "
                "can tell whether it describes the page as it stands")
    if not GEN_REGEN.search(block):
        rep.add(WARN, "generated-block-no-command", name,
                "a generated block carries no `regenerate:` line, so a reader who "
                "finds it stale has no way to refresh it")

    if stamp and latest and _ymd(stamp.group(1)) < latest:
        rep.add(WARN, "generated-block-stale", f"{name} · {tag}",
                f"the block was measured {_ymd(stamp.group(1))} and this page has "
                f"logged work through {latest}, so it measures a version that no "
                "longer exists")



def check_evidence_file(path, name, rep):
    """`draft/<stem>-evidence.md` is DERIVED (workbench-task-draft 0.22.0):
    the typed table (`<stem>-evidence-items.md`, specified at SHAPE and planned
    at SURVEY) joined to local Results, one record per Evidence Item, its Status
    one word of the item ladder,
    written only by `cli/evidence-status.py`. Two things can go wrong with a derived
    file and both are silent: it is older than the evidence it describes, or
    someone typed into it. A stale status that reads as measured is worse than
    no file (JL 260831)."""
    if path is None:
        return
    ev = plan_dir(path.parent) / f"{path.stem}-evidence.md"
    if not ev.exists():
        return
    text = ev.read_text(encoding="utf-8", errors="replace")
    stamp = re.search(r"MEASURED\s+(2\d{5})(?:\s+(\d{4}))?", text)
    if not stamp or "GENERATED; do not hand-edit" not in text:
        rep.add(WARN, "evidence-hand-edited", name,
                "`%s` carries no `MEASURED <date>` + GENERATED line; a status "
                "nobody generated is a status somebody typed" % _plan_rel(ev))
        return
    import datetime as _dt
    measured = _dt.datetime.strptime(stamp.group(1) + (stamp.group(2) or "0000"), "%y%m%d%H%M").timestamp()
    newest, newest_name = 0.0, ""
    lanes = [plan_dir(path.parent), path.parent / "probe", path.parent / "bibex",
             path.parent / "display"]
    for lane in lanes:
        if not lane.is_dir():
            continue
        for f in lane.rglob("*"):
            if f.is_file() and f != ev and f.stat().st_mtime > newest:
                newest, newest_name = f.stat().st_mtime, f.relative_to(path.parent).as_posix()
    if newest > measured + 60:
        rep.add(WARN, "evidence-stale", name,
                "`%s` was measured %s %s but `%s` changed later; regenerate "
                "with `cli/evidence-status.py`" % (_plan_rel(ev), stamp.group(1), stamp.group(2) or "", newest_name))


def check_discussion_file(path, name, rep):
    """`draft/records/<stem>-discussion.md` holds OPEN questions only (workbench-
    outline 0.18.0, JL 260831: "the solved one go to logs, and only leave the
    one we have not solved"). A thread that is settled, decided or dropped has
    moved: its ruling is one `### YYMMDD · D<nn> …` record in `-log.md`. A
    settled thread still sitting here is the old shape, and the file it makes
    is the one nobody could read."""
    if path is None:
        return
    f = record_path(plan_dir(path.parent), path.stem, "discussion")
    if not f.exists():
        return
    text = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"(?ms)^### (D\d+) · [^\n]*\n(.*?)(?=^### |\Z)", text):
        body = m.group(2)
        if re.search(r"(?m)^\s*(?:status:|- \*\*Status\*\*:)\s*(✅|🚫)", body) \
                or re.search(r"(?m)^\s*(?:settled:|- \*\*Settled\*\*:)", body) \
                or re.search(r"(?m)^\s*status:\s*✅", body):
            rep.add(WARN, "discussion-settled-thread", name,
                    f"thread `{m.group(1)}` is settled and still in `{_plan_rel(f)}`; the discussion "
                    f"holds open questions only, so its ruling belongs in `draft/records/{path.stem}-log.md` "
                    f"as one dated record (workbench-task-draft 0.18.0)")


def check_requirement_file(text, path, name, rep):
    """`draft/records/<stem>-requirement.md` holds a generated venue V block and an
    authored page-writing W block. `cli/requirement.py` refreshes only V. A
    Section that binds a venue division and has no file shows no 📏 chip; a V
    block without its GENERATED line has lost its ownership boundary."""
    if path is None or not re.search(r"(?m)^page-type:\s*section\b", text[:800]):
        return
    if not re.search(r"(?m)^structure-source:\s*\S", text[:3000]):
        return
    f = record_path(plan_dir(path.parent), path.stem, "requirement")
    if not f.exists():
        rep.add(WARN, "requirement-missing", name,
                f"this page binds a venue division and `{_plan_rel(f)}` "
                f"does not exist; run `cli/requirement.py {path.name}`")
        return
    if "GENERATED; do not hand-edit" not in f.read_text(encoding="utf-8", errors="replace"):
        rep.add(WARN, "requirement-hand-edited", name,
                f"`{_plan_rel(f)}` carries no GENERATED line for its venue V block; regenerate it without replacing authored W records")
        return
    # STALE: the venue desk (its one source) is newer than the stamp; a
    # requirement that outlives a moved desk reads as binding.
    ftxt = f.read_text(encoding="utf-8", errors="replace")
    stamp = re.search(r"MEASURED\s+(2\d{5})(?:\s+(\d{4}))?", ftxt)
    if not stamp:
        return
    import datetime as _dt
    measured = _dt.datetime.strptime(stamp.group(1) + (stamp.group(2) or "0000"), "%y%m%d%H%M").timestamp()
    from src.skill_paths import in_skills
    srcs = []
    m = re.search(r"(?m)^structure-source:\s*(\S+)", text[:3000])
    if m:
        srcs += [q for q in (in_skills(m.group(1)), path.parents[2] / m.group(1)) if q.exists()]
    for s in srcs:
        if s.exists() and s.stat().st_mtime > measured + 60:
            rep.add(WARN, "requirement-stale", name,
                    f"`{_plan_rel(f)}` was measured {stamp.group(1)} {stamp.group(2) or ''} but `{s.name}` changed "
                    f"later; regenerate with `cli/requirement.py {path.name}`")
            return


def check_section_writing_requirements(text, path, name, rep):
    """A Section's page-owned writing rules are authored W records in the
    mixed-ownership Requirement file. The generated V block and authored W
    block share one reader question but never one writer."""
    if path is None or not re.search(r"(?m)^page-type:\s*section\b", text[:800]):
        return
    if re.search(r"(?m)^#{2,3}\s+Writing Style\b", text):
        rep.add(WARN, "section-writing-in-page", name,
                "a manuscript Section stores writing rules in "
                f"`draft/records/{path.stem}-requirement.md` as W<n> records; remove the Page's "
                "`Writing Style` block after migrating each instruction to a W<n> record")
    retired = plan_dir(path.parent) / f"{path.stem}-writing.md"
    if retired.exists():
        rep.add(WARN, "writing-file-retired", name,
                f"`{_plan_rel(retired)}` is a redundant sidecar; move its W<n> "
                f"records into `draft/records/{path.stem}-requirement.md`")
    f = record_path(plan_dir(path.parent), path.stem, "requirement")
    if not f.exists():
        # check_requirement_file already reports the missing shared file.
        return
    ftxt = f.read_text(encoding="utf-8", errors="replace")
    records = list(re.finditer(r"(?ms)^###\s+(W\d+)\s*·\s*([^\n]+)\n(.*?)(?=^###\s+|\Z)", ftxt))
    if not records:
        rep.add(WARN, "writing-shape", name,
                f"`{_plan_rel(f)}` has no authored `### W<n> · <preview>` records")
        return
    writing_begin = ftxt.find("# --- writing:begin (authored) ---")
    writing_end = ftxt.find("# --- writing:end ---")
    if writing_begin < 0 or writing_end <= writing_begin:
        rep.add(WARN, "writing-shape", name,
                f"`{_plan_rel(f)}` must bound W<n> records with authored writing markers")
    elif any(not (writing_begin < record.start() < writing_end) for record in records):
        rep.add(WARN, "writing-shape", name,
                f"every W<n> record in `{_plan_rel(f)}` must remain inside the authored writing block")
    for record in records:
        body = record.group(3)
        missing = [label for label in ("Rule", "Applies", "Source")
                   if not re.search(rf"(?m)^- \*\*{label}\*\*:\s*\S", body)]
        if missing:
            rep.add(WARN, "writing-shape", name,
                    f"`{record.group(1)}` in `{_plan_rel(f)}` lacks "
                    + ", ".join(missing))


def check_retired_blocks(text, name, rep):
    """`### Stage Record` is a leftover of the retired Submission-0 stage
    lifecycle ("Rollup: S Submission 0 Reconcile Unit: 1 of 9"). It renders
    as a fold that says nothing true about the page (JL 260831: "why we have
    this? we should not have this"). Delete it; nothing replaces it."""
    for m in re.finditer(r"(?m)^###\s+Stage Record\b", text):
        rep.add(WARN, "retired-block", name,
                "`### Stage Record` is a leftover of the retired stage lifecycle; delete the block")


def page_aims_text(text, path):
    """The page's Aims, wherever they live.

    Since `workbench-task-draft` 0.16.0 the Aims live in the page's PLAN and
    `page.md` keeps no copy, so sourcing them from the page alone made the law
    and this checker contradict each other: obeying the law produced
    `missing-section` + `no-aims` on every migrated page (field test, JL
    260830). Page first, so an unmigrated board is untouched; plan second.
    """
    on_page = section_text(text, "Done when")
    if on_page.strip() or path is None:
        return on_page, False
    d = plan_dir(path.parent)
    plan = latest_outline(d, path.stem)
    if plan is None:
        return on_page, False
    plan_text = plan.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(?m)^## Aims\b.*?$(.*)\Z", plan_text, re.S)
    return (m.group(1) if m else ""), bool(m)


_ROUND_CACHE = {}


def check_plan_arc(path, name, rep):
    """hai-draft-logic (ref/structure.md) §🚦 ⓪.1: `arc:` present is mechanical. It was
    parsed by nothing until NA01's field desk grepped for it (260831)."""
    if path is None:
        return
    for plan in sorted(plan_files(plan_dir(path.parent))):
        text = plan.read_text(encoding="utf-8", errors="replace")
        # the header block: everything before the first `## ` heading (run names grew, 260929)
        cut = re.search(r"(?m)^## ", text)
        head = text[:cut.start()] if cut else text[:3000]
        if not re.search(r"(?m)^arc:\s*\S", head):
            rep.add(WARN, "plan-no-arc", f"{name} · {plan.name}",
                    "the plan carries no `arc:` line; a division list with no "
                    "stated argument is a table of contents (§🚦 ⓪.1)")


def check_feedback_coverage(path, text, name, rep):
    """Both directions of the Round⇄page join (hai-draft-logic (ref/structure.md) ⓪ COLLECT).

    Forward: every §2B row a Round routes to this page appears in the page's
    draft/feedback/<RD>.md. Reverse: every register row names a real Round
    row. A page that never ran OUTLINE never collected, so G7 must not close on
    a Round whose targets carry no register (field test, JL 260831)."""
    if path is None or re.search(r"(?m)^page-type:\s*round\b", text[:600]):
        return
    board = path.parents[2]
    if board not in _ROUND_CACHE:
        _ROUND_CACHE[board] = [(rd, parse_round(rd)) for rd in _rounds(board)]
    pid = path.stem.split("-")[0]
    for rd, data in _ROUND_CACHE[board]:
        routed = {r["id"] for r in data["rows"].get(pid, [])}
        if not routed:
            continue
        reg = register_path(path)
        if not reg.exists():
            rep.add(WARN, "feedback-uncollected", name,
                    f"{rd.stem.split('-')[0]} routes {len(routed)} row(s) here and "
                    f"`{_plan_rel(reg)}` does not exist; run "
                    f"`cli/feedback.py collect` (OUTLINE ⓪)")
            continue
        have = register_ids(reg)
        # the OTHER direction the law promises (hai-draft-logic (ref/structure.md) ⓪): an
        # OPEN register row is served by a plan bullet carrying `Routed:` or
        # declined in the plan's header (`declined: <RD> <id> · <reason>`).
        # NA01's field desk (260831) found this tooth missing while the workbench
        # text claimed "both directions".
        latest = latest_outline(plan_dir(path.parent), path.stem)
        plan = latest.read_text(encoding="utf-8", errors="replace") if latest else ""
        rdid = rd.stem.split("-")[0]
        # One grammar with the Page's Feedback column (src/feedback.py):
        # `Routed: RD01 S3-PP2, S3-PP3` serves two rows, not `S3-PP2,`.
        served = {rid for _rd, rid in routed_rows(plan, rdid)}
        declined = set(re.findall(rf"(?m)^declined:\s*{rdid}\s+(\S+)", plan))
        open_rows = {r["id"] for r in data["rows"].get(pid, []) if r["state"] == "open"}
        for rid in sorted((open_rows & have) - served - declined):
            rep.add(WARN, "feedback-unserved", f"{name} · {reg.name}",
                    f"open row `{rid}` is served by no plan bullet (`Routed: {rdid} {rid}`) "
                    f"and not declined (`declined: {rdid} {rid} · <reason>`)")
        for rid in sorted(routed - have):
            rep.add(WARN, "feedback-coverage", f"{name} · {reg.name}",
                    f"Round row `{rid}` is routed here and missing from the register")
        for rid in sorted(have - routed):
            rep.add(WARN, "feedback-coverage", f"{name} · {reg.name}",
                    f"register row `{rid}` names no row the Round routes here")


def check_state_mirrors_aims(aims_text, states_text, name, rep):
    """Every Aim id carries exactly one status row in States.

    Aims say what should become true; States says what is true now, one row per
    Aim id. `aim_progress` reads the rows and defaults a missing one to ⬜, so a
    page that never wrote States renders as 0 of N and looks untouched. That is
    the failure this catches, and it was invisible until 260806, when writing
    the ten Page Type templates walked eight specimens and found five of them
    missing EVERY row: 11 of 11 on one page, 7 of 7, 6 of 6, 8 of 9, 3 of 3.

    The opposite direction is worse and this catches it too. A row for an id no
    Aim declares reads as progress on a target that does not exist; QA4 rendered
    P1 ✅ through P5 ✅ while zero of its seven slides had been accepted.

    Legacy checkbox pages are exempt: they carry their state in the box, which
    is why `aim_progress` reads them by a different path.
    """
    if re.search(r"(?m)^\s*[-*]\s*\[[ xX]\]", aims_text or ""):
        return                                  # legacy checklist, state in the box
    declared = aim_ids(aims_text)
    if not declared:
        return
    # Since the 260819 merge the tick sits on the Aim row itself; a page that
    # still carries `## States` is read the old way, so an unmigrated board
    # keeps its findings and a migrated one stops reading as "all ⬜".
    src = states_text if (states_text or "").strip() else aims_text
    rows = [aim_id for _emoji, aim_id in AIM_STATE_RE.findall(src or "")]
    seen = collections.Counter(rows)

    missing = [a for a in declared if not seen[a]]
    if missing:
        shown = " · ".join(missing[:6]) + (" …" if len(missing) > 6 else "")
        rep.add(WARN, "aim-without-state", name,
                f"{len(missing)} of {len(declared)} Aim(s) carry no tick, on the row or in States, "
                f"so each renders as ⬜ and the page reads less done than it is: {shown}")

    twice = sorted(a for a, n in seen.items() if n > 1 and a in declared)
    if twice:
        rep.add(WARN, "aim-stated-twice", name,
                "States carries two rows for the same Aim, so which one counts is "
                f"whichever the parser met last: {' · '.join(twice)}")

    stray = sorted(a for a in seen if a not in declared)
    if stray:
        rep.add(WARN, "state-without-aim", name,
                "States reports progress on an id no Aim declares, so the page "
                f"shows work against a target that does not exist: {' · '.join(stray)}")


def check_division_figures(text, name, rep):
    """Non-manuscript Content divisions open with a caption and figure.

    QB4 §3.3.1: caption, figure, short intro, in that order, before any prose.
    The figure is drawn with /diagram-ascii; the caption is `**Name**: what
    this diagram shows.` (JL 260801). Both are easy to forget on a new
    division, and neither failure reports itself at render.
    """
    # A manuscript Section owns displays through Bullet-local DISPLAY Evidence.
    # It does not owe one figure per subsection; that generic Board-page rule
    # would contradict an explicit one-display or no-display outline contract.
    if re.search(r"(?m)^page-type:\s*section\s*$", text):
        return
    content = section_text(text, "Content") or ""
    # `### §1 Demonstration` and `### 6.1 · x` are divisions too. Matching only
    # `### <digit> · ` made every §-numbered part INVISIBLE to this check, so
    # the board's figure count was understated (found by a fresh-context agent
    # on QB5, 260802, not by any check).
    parts = re.split(r"(?m)^### §?([\d.]+)(?: · | )(.+)$", content)
    for k in range(1, len(parts), 3):
        num, title, body_ = parts[k], parts[k + 1], parts[k + 2]
        lines = [l for l in body_.split("\n")]
        first = next((l for l in lines if l.strip()), "")
        fenced = any(l.lstrip().startswith("```") for l in lines)
        # A rendered media embed is a figure in the renderer's own vocabulary
        # (`img.fig`, `object.figpdf`, `.fightml`): a slide page's divisions
        # carry the live slide instead of an ascii fence, and that satisfies
        # the reader the same way (JL 260805, QA4). The caption rule below
        # still applies to it.
        media = any(re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", l.strip())
                    for l in lines)
        if not (fenced or media):
            rep.add(WARN, "division-no-figure", f"{name} · §{num}",
                    f"{title.strip()!r} opens with no figure (QB4 §3.3.1)")
        elif not re.match(r"^\*\*[^*]+\*\*\s*:", first.strip()):
            rep.add(WARN, "division-no-caption", f"{name} · §{num}",
                    f"{title.strip()!r} has a figure with no caption line above "
                    "it (QB4 §2.2: `**Name**: what this diagram shows.`)")


def check_one_canvas(text, name, rep):
    """A page attaches at most ONE Excalidraw canvas (JL 260801).

    Two forms exist and both are legal on their own: `/_excalidraw/?board=…`
    is the board's own scene, and `https://app.excalidraw.com/s/…` is a scene
    hosted elsewhere. The renderer embeds EVERY canvas URL it finds, so two
    lines silently produce two canvases and no reader can tell which is the
    current drawing.
    """
    dia = section_text(text, "Outline") or section_text(text, "Diagram") or ""
    urls, fence = [], False
    for ln in dia.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        s2 = ln.strip()
        if fence or not s2:
            continue
        if re.match(r"^(?:/_excalidraw/|https?://(?:app\.)?excalidraw\.com/)\S*$", s2):
            urls.append(s2)
    if len(urls) > 1:
        rep.add(WARN, "two-canvases", f"{name} · Outline",
                f"{len(urls)} canvas URLs; a page attaches one (QB4 §2.7). "
                f"Keep either the board scene or the hosted link, not both")


# ---- QB6 §5.1 rule 1: type resolution runs BEFORE any per-type rule ----
# The base contract (`hai-draft/SKILL.md`) resolves ① to ⑤ and stops
# at the first key that matches. Step ③ is REQUIRED on its declared types and BEATS
# the filename, which is what settles the two real collisions, `S-Display-4c`
# (a stage filename, a display page) and `QA4` (a Q filename, a slide deck).
#
# Only the ③ key can be wrong in a way a machine can see, so that is what this
# rule reads. The unit segment is `[A-Za-z0-9]+` because the live board's real
# units are `Pitch`, `Seed`, `C`, `C0`, `R1`, `1a` and `Dash`; a first version
# demanded a digit and reported 25 of 59 pages on the live MISQ paper as
# claimed by nothing, which was the pattern being wrong, not the board.
FENCE = "`" * 3
PAGE_TYPE_LINE = re.compile(r"(?m)^page-type:\s*(\S+)\s*$")
# `stage` joined 260815: the restructure reduced this family's kinds to stage
# and design, and QPs3's specimen declares `page-type: stage` explicitly.
# 260820, Application two-board split: `meta` joined as the InsightBoard head;
# `intervention` was renamed to the already-listed `design`, and `artifact` was
# absorbed into a per-division `accepted:` row. Both are dropped, so a page still
# carrying either key now reports page-type-unknown and gets migrated.
# 260907, current Paper layout: the Story page owns the paper's integrated
# control surface. Seed, Roadmap, Narrative, and Collection are content
# concepts or retired page keys, not current Page Types.
# 261007: `comments` is hai-paper-comments (renamed from hai-paper-round); `round` stays readable
# because Pages written before the rename still declare it.
PAGE_TYPE_VALUES = ("display", "slide", "design", "opening", "venue", "story",
                    "section", "comments", "round", "labeling", "dash", "task", "insight",
                    "meta", "question", "data", "information", "knowledge",
                    "wisdom", "brief", "view", "stage", "ideation")
STEP4_STAGE = re.compile(r"^S-[A-Za-z]+-[A-Za-z0-9]+(?:-.+)?$")


def check_page_type(path, text, name, rep):
    """Exactly one key claims a page, and step ③'s key is one the table knows."""
    head = text.split("\n## ", 1)[0]
    declared = PAGE_TYPE_LINE.findall(head)
    route = re.search(r"(?m)^route:\s*(outward|inward)\s*$", head)
    if len(declared) > 1:
        rep.add(WARN, "page-type-twice", name,
                f"{len(declared)} `page-type:` lines; exactly one step may "
                "claim a page")
    for value in declared:
        if value not in PAGE_TYPE_VALUES:
            rep.add(WARN, "page-type-unknown", f"{name} -> {value}",
                    f"step ③ defines {', '.join(PAGE_TYPE_VALUES)}; `{value}` "
                    "is in no step, so this page resolves by filename instead")
    if declared and route:
        # ② wins by order, so the ③ key is dead text and says otherwise.
        rep.add(WARN, "page-type-conflict", name,
                f"carries `route: {route.group(1)}` (step ②) AND "
                f"`page-type: {declared[0]}` (step ③); ② resolves first, so "
                "the page is not the type its own key names")


def check_group_names(text, name, rep):
    """An Aims or States group must carry its Content division's id AND name.

    JL 260801: "could they share the same name? like the division name in the
    Content can be used by the Aims and States as well." Five of QB4's six
    groups already did; the sixth was still named for a topic its division had
    stopped carrying, and nothing reported it because nothing compared the two
    lists. `P` is exempt: a page-level target belongs to no single division.
    """
    def groups(sec_name, pat):
        block = section_text(text, sec_name) or ""
        return dict(re.findall(pat, block, re.M))

    # ORDINAL, not the printed number (JL 260831, QPf12 row 2: Aims "should map
    # to the content"): `A<n>` is the n-th direct `###` division of Content,
    # whatever its label, because a section page numbers `### §3.1 · …` and a
    # paper page writes `### Title`, and the 🧭 tab's `C<n>` addresses count the
    # same way. On a `### 1 · …` page ordinal and printed number coincide, so
    # nothing an older board reports changes there.
    content = section_text(text, "Content") or ""
    divs, fence = {}, False
    for ln in content.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if fence or not re.match(r"^### \S", ln):
            continue
        title = re.sub(r"^### (?:§?[\d.]+(?: · | ))?", "", ln).strip()
        divs[str(len(divs) + 1)] = title
    if not divs:
        return
    for sec_name in ("Aims", "States"):
        # `A<n>` is the id (JL 260802): the group holds A-records, so naming it
        # `C3` made the reader translate one letter into another for no gain.
        # `C<n>` still resolves, since older boards are full of it.
        found = groups(sec_name, r"^### A(\d+) · (.+)$")
        found.update(groups(sec_name, r"^### C(\d+) · (.+)$"))
        for gid, gname in found.items():
            want = divs.get(gid)
            # The contract says a group takes the NUMBER, NAME and EMOJI of its
            # Content part (hai-draft §241), so the part may carry one too:
            # strip both sides or an emoji'd division reads as drift (JL 260816).
            gname = re.sub(r"^\W+\s*", "", gname)   # the group's own emoji
            if want is not None:
                want = re.sub(r"^\W+\s*", "", want)
            if want is None:
                rep.add(WARN, "group-no-division", f"{name} · {sec_name} A{gid}",
                        f"there is no Content division #{gid} on this page (ordinal: the {gid}th `###` heading under Content)")
            elif want.strip() != gname.strip():
                rep.add(WARN, "group-name-drift", f"{name} · {sec_name} A{gid}",
                        f"reads {gname.strip()!r}; Content division #{gid} is "
                        f"{want.strip()!r} (QB4 §0.5: same id, same name)")
