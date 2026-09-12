"""Is the page's EVIDENCE actually on disk, and did the projections take it?

WHY THIS EXISTS. Until 260816 the board checked the Markdown and nothing else,
so a page could pass every check while the thing a person opens was missing half
its content. QV2-lbp-regression-results is the case that named the gap: the
display tab counted five unit FOLDERS, three of them held nothing but a README
and an empty ``recipe/``, and the LaTeX export correctly embedded the two that
had rendered. Every layer behaved as specified and the reader still got a report
with three tables missing (JL 260816: "You have five displays in the display
plugins, but only two in the latex, why? Is it the workflow issue?").

It was. Nothing owned the step between "the answer came back" and "the float
exists", so nothing reported that it had not been taken. These checks report it.

WHAT IT DOES NOT DO. It never renders, never edits a unit, and never ticks
``accepted:``. Step ⑤ of the display walk is a person's and stays a person's
(`page-plugins/haipipe-plugin-outline/ref/evidence/displays.md`). This module only says which step a unit
is stuck on, in the same vocabulary the 🖼 tab uses, so the tab and the checker
cannot disagree about what "rendered" means.

THREE COUNTS, NEVER ONE. `declared` is a unit folder, `rendered` is a winning
asset plus a preview, `accepted` is a human tick. Folder count is not completed
work, and the whole failure above is what collapsing them looks like.
"""
from __future__ import annotations

import re
from pathlib import Path


# The winning render, by the display family's unit contract. A unit is RENDERED
# when one of these exists AND `preview.pdf` was compiled from it: the asset
# alone is what a half-run renderer leaves behind.
WINNING_ASSETS = ("table-body.tex", "figure.pdf", "figure.png", "figure.svg")

# `<stem>-Display<N>-<slug>` — the page-side unit address. The board's own
# citation index keys on the same shape (`src/dialect_paper.py`).
UNIT_DIR_RE = re.compile(r"^(?P<stem>.+)-Display(?P<n>\d+)-(?P<slug>.+)$")

# BOTH citation forms resolve to the same unit and both exporters place it once
# (`haipipe-plugin-outline/ref/evidence/displays.md`, "Citation"): the bare Page-local id inside its own
# page, and the fully qualified `<stem>-DisplayN` in cross-page prose. Matching
# only the bare form called seven correctly-cited units uncited on
# CMSStoreBoard, because `QC2-cancer-Display3` is preceded by a hyphen.
#
# The trailing `(?![\w-])` keeps a FOLDER name out: `Display3-method-workflow`
# inside a path is filing, not a sentence citing evidence. Code spans and fences
# are stripped before matching, because a backticked id QUOTES instead of
# chipping and a page documenting the citation move must not report itself.
CITE_RE = re.compile(r"(?<!\w)Display(\d+)(?![\w-])")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")

# BOTH row forms are in the wild and both are the unit contract's rows: QV2's
# units write `- claim: ...` and every CMSStoreBoard unit writes a bare
# `claim: ...`. Requiring the bullet read ZERO rows off 25 real units, which
# means no claim, no kind, and no `accepted:` tick was visible on any of them.
# The leading `-` is optional for that reason, and the key is length-capped so a
# prose sentence containing a colon cannot pose as a row.
#
# ⚠️ `live/plugview.py:122 _readme_rows` has the same bullet-only rule and the
# same blind spot, so the 🖼 tab currently shows those 25 units with no claim,
# kind, or acceptance state. Not fixed here: that file is another session's open
# work, and the tab and this checker must not be allowed to disagree about what
# a row IS — they should share one parser once it lands.
# Four dialects on disk, and the bold marker lands on either side of the colon:
#   `- claim: x`  ·  `claim: x`  ·  `**Claim**: x`  ·  `- **Kind:** x`
README_ROW_RE = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}([A-Za-z][\w -]{0,24}?)\*{0,2}\s*:\s*\*{0,2}\s*(.*?)\s*$",
    re.M)

# The unit contract fixes five rows: claim / kind / caption-job / fragility /
# status (`display/ref/display-unit-output-contract.md`). Three dialects exist
# on disk and all three MEAN those rows, so all three are read and the drift is
# reported separately. Reading only one dialect and calling the others litter is
# how a checker teaches people to ignore it.
ROW_ALIASES = {
    "reader job": "caption-job",
    "caption job": "caption-job",
    "job": "caption-job",
    "evidence": "intake",
    "source": "intake",
    "what it shows": "claim",
    "shows": "claim",
}


def _rows(unit: Path) -> dict[str, str]:
    readme = unit / "README.md"
    if not readme.is_file():
        return {}
    text = readme.read_text(encoding="utf-8", errors="replace")
    rows = {}
    for key, value in README_ROW_RE.findall(text):
        key = key.strip().lower()
        rows.setdefault(ROW_ALIASES.get(key, key), value)
    return rows


def _newest(root: Path) -> float:
    """The newest mtime under a folder, 0.0 when it holds no file."""
    times = [p.stat().st_mtime for p in root.rglob("*") if p.is_file()]
    return max(times) if times else 0.0


def unit_state(unit: Path) -> dict:
    """One display unit's position on the five-step walk.

    The step names and their order are the unified Evidence display lane's, adopted
    verbatim: ① INTAKE 🧑 → ② RENDER ⚙️ → ③ PICK 🧑 → ④ BUILD ⚙️ → ⑤ ACCEPT 🧑.
    """
    rows = _rows(unit)
    inputs = unit / "intake" / "inputs"
    has_intake = ((unit / "intake" / "manifest.yaml").is_file()
                  and inputs.is_dir()
                  and any(p.is_file() for p in inputs.rglob("*")))
    recipe = unit / "recipe"
    has_recipe = recipe.is_dir() and any(p.is_file() for p in recipe.rglob("*"))
    assets = unit / "assets"
    has_asset = assets.is_dir() and any(
        p.is_file() and p.name in WINNING_ASSETS for p in assets.rglob("*"))
    has_preview = (unit / "preview.pdf").is_file()
    accepted_text = rows.get("accepted", "").strip().lower()
    accepted = accepted_text.startswith(("✅", "yes", "true", "accepted"))

    rendered = has_asset and has_preview

    # TWO INDEPENDENT AXES, and conflating them mislabels real units. The tab's
    # "first missing step" walk is a to-do list; a CHECKER must say which of two
    # different things is wrong, because they have different consequences and
    # different fixes. Seven units on CMSStoreBoard are rendered and cited and
    # print correctly while carrying an `intake/manifest.yaml` whose
    # `intake/inputs/` was never frozen: calling those "not rendered" would send
    # someone to re-run a renderer that already worked.
    if not rendered:
        if not has_intake:
            missing = "① INTAKE · no frozen intake/manifest.yaml + inputs"
        elif not has_recipe:
            missing = "② RENDER · no renderer-owned recipe/"
        elif not has_asset:
            missing = "② RENDER · recipe/ produced no winning asset in assets/"
        else:
            missing = "④ BUILD · no preview.pdf"
    else:
        missing = ""            # a rendered candidate awaiting ⑤ is not a defect

    # Visible but untraceable: the render exists, the snapshot it was drawn from
    # does not, so no reader can get from a printed number back to its source.
    unfrozen = rendered and not has_intake

    # A tick binds a render to the inputs it was accepted WITH, so an intake
    # touched afterwards silently un-accepts the unit.
    stale_accept = bool(accepted and has_intake
                        and _newest(unit / "intake") > _newest(assets)
                        and _newest(assets) > 0)

    # DRAFT may PROPOSE a unit in owed state, and a proposal SAYS WHAT IT WILL
    # HOLD: `claim:` is what separates a promise from an empty folder someone
    # left behind. Without it nobody downstream can render the unit, and nobody
    # can tell whether it was ever meant to exist.
    proposed = bool(rows.get("claim", "").strip())

    return {
        "name": unit.name,
        "kind": rows.get("kind", ""),
        "proposed": proposed,
        "declared": True,
        "rendered": rendered,
        "accepted": accepted,
        "stale_accept": stale_accept,
        "unfrozen": unfrozen,
        "missing": missing,
    }


def display_units(page_source: Path) -> list[Path]:
    """Every declared unit folder beside one Page source, in id order.

    A unit is DECLARED by its folder, not by holding a float.tex: the empty
    shells are exactly what must be reported, so the selector cannot be the
    thing they are missing.
    """
    folder = page_source.parent / page_source.stem
    root = folder / "display" if folder.is_dir() else page_source.parent / "display"
    if not root.is_dir():
        return []

    def key(path: Path) -> tuple:
        m = UNIT_DIR_RE.match(path.name)
        return (int(m.group("n")), path.name) if m else (10**6, path.name)

    return sorted((d for d in root.iterdir()
                   if d.is_dir() and not d.name.startswith((".", "_"))),
                  key=key)


def cited_ids(text: str) -> set[str]:
    """Every display unit id the page's prose cites, in either legal form."""
    prose, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            prose.append(CODE_SPAN_RE.sub(" ", line))
    return {n.lstrip("0") or "0" for n in CITE_RE.findall("\n".join(prose))}


def _projection(page_source: Path, kind: str) -> Path | None:
    folder = page_source.parent / page_source.stem
    root = folder / kind if folder.is_dir() else page_source.parent / kind
    if not root.is_dir():
        return None
    suffix = ".tex" if kind == "latex" else ".docx"
    hit = root / f"{page_source.stem}{suffix}"
    return hit if hit.is_file() else None


def check_page_evidence(page_source: Path, text: str, name: str, rep,
                        error="ERROR", warn="WARN") -> None:
    """Report every gap between what the page promised and what it built.

    ``rep`` is `cli/check.py`'s report object; ``error``/``warn`` are its level
    constants, passed in so this module stays importable without the CLI.
    """
    units = display_units(page_source)
    if not units:
        return

    states = [unit_state(u) for u in units]
    rendered = sum(1 for s in states if s["rendered"])

    for state in states:
        if not state["proposed"]:
            rep.add(error, "display-declared-no-claim",
                    f"{name} -> {state['name']}",
                    "the README states no claim under any of the contract's row "
                    "names or their known aliases, so nothing says what this unit "
                    "would show: no renderer can draw it and no reader can miss "
                    "it. A folder without a claim is not a proposal.")
        if state["missing"]:
            rep.add(error, "display-declared-not-rendered",
                    f"{name} -> {state['name']}",
                    f"declared but not rendered; first missing step is "
                    f"{state['missing']}. A unit folder is not a display, and "
                    f"the projections embed only rendered units, so this one "
                    f"is invisible to every reader of the PDF or docx.")
        if state["unfrozen"]:
            rep.add(error, "display-intake-unfrozen",
                    f"{name} -> {state['name']}",
                    "rendered, but `intake/inputs/` holds no frozen snapshot, so "
                    "nothing carries a printed number back to the run that "
                    "produced it. The render is fine; the provenance is missing.")
        if state["stale_accept"]:
            rep.add(error, "display-accept-stale",
                    f"{name} -> {state['name']}",
                    "`accepted: ✅` but intake/ is newer than assets/; the tick "
                    "binds a render that no longer matches its inputs. Re-render, "
                    "then have a person accept it again.")

    # The QV2 defect itself: the prose names a unit and the PDF never carries it.
    tex = _projection(page_source, "latex")
    if tex is not None:
        tex_text = tex.read_text(encoding="utf-8", errors="replace")
        by_n = {}
        for unit, state in zip(units, states):
            m = UNIT_DIR_RE.match(unit.name)
            if m:
                by_n[m.group("n").lstrip("0") or "0"] = (unit, state)
        for n in sorted(cited_ids(text), key=lambda v: int(v)):
            pair = by_n.get(n.lstrip("0") or "0")
            if pair is None:
                rep.add(warn, "display-cited-unit-missing", f"{name} -> Display{n}",
                        "the prose cites this unit and no such folder exists "
                        "under display/")
                continue
            unit, state = pair
            if unit.name not in tex_text:
                detail = ("it never rendered, so the exporter skipped it"
                          if not state["rendered"]
                          else "it IS rendered, so this is an export fault")
                rep.add(error, "display-cited-not-embedded",
                        f"{name} -> Display{n}",
                        f"cited in the prose but absent from "
                        f"{tex.parent.name}/{tex.name}; {detail}.")

        # The mirror defect: a unit that rendered and that no sentence names.
        # The projections inherit the CITATION, so an uncited unit prints
        # nowhere however finished it is.
        cited = {n.lstrip("0") or "0" for n in cited_ids(text)}
        for n, (unit, state) in sorted(by_n.items(), key=lambda kv: int(kv[0])):
            if n not in cited and state["rendered"]:
                rep.add(warn, "display-rendered-not-cited",
                        f"{name} -> {unit.name}",
                        "rendered but no sentence cites `Display" + n + "`, and "
                        "the projections embed only cited units, so this render "
                        "reaches no reader.")

        # The Page's own H1 must reach the document as a title block.
        if not re.search(r"\\(title|section\*?)\{", tex_text):
            rep.add(error, "latex-untitled", f"{name} -> {tex.name}",
                    "the exported .tex carries no title block, so the PDF opens "
                    "on its first body question with nothing naming it.")

        if tex.stat().st_mtime < page_source.stat().st_mtime:
            rep.add(warn, "projection-stale", f"{name} -> {tex.name}",
                    "the .tex is older than the Page source it projects; REVISE "
                    "changed the page and did not rebuild.")

    docx = _projection(page_source, "word")
    if docx is not None and docx.stat().st_mtime < page_source.stat().st_mtime:
        rep.add(warn, "projection-stale", f"{name} -> {docx.name}",
                "the .docx is older than the Page source it projects; REVISE "
                "changed the page and did not rebuild.")

    if rendered < len(units):
        rep.add(warn, "display-counts-split", name,
                f"{len(units)} declared · {rendered} rendered · "
                f"{sum(1 for s in states if s['accepted'])} accepted. The three "
                f"counts are independent and folder count is never completed work.")
