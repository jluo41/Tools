"""📃 Page · reading the plan file: its latest version, the next Shape tag, the typed Evidence Item join, and the plain-text passes plan_card runs first.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
import re

from src.outline_version import plan_dir, latest_outline, version_tag
from src.item_table import (
    ITEM_TYPES,
    LADDER as ITEM_LADDER,
    bullets as typed_bullets,
    cycle_now as item_cycle,
    evidence_none_targets,
    item_status,
    read_items,
    repo_root,
)
from live.outline_preview import reader_prose


# ---------------------------------------------------------------- the plan
# The structure Run's own file, `<page>/draft/<stem>-draft-v<G>.<S>[.<E>].md`
# (`<page>/outline/<stem>-outline-v...` on a Page not yet moved to draft/)
# (workbench-task-draft §🗂, JL 260817). It is AUTHORED, frozen once its
# `approved:` line is ticked, and progress is NEVER written back into it.
# An explicit Bullet editor write creates a new unapproved Shape first; that
# working copy is the only plan this renderer is allowed to update.
# So this card renders two things side by side: what the plan SAID, and what
# is on disk NOW. The gap between them is the whole point of the card.

# 🧮 = value since 260819 (JL; the glyph's proof meaning died that morning).
# 🔢 stays accepted as the pre-260819 legacy alias so old plans keep parsing.
# The ✅ "have it" mark was RETIRED 260819: it named nothing a machine could
# recheck, an unmarked bullet already means "plain point, nothing owed", and
# the glyph already works two other jobs (tick syntax, the check gate). It
# confused JL three separate times, and a mark that needs explaining fails
# its only job. Zero plans carried it at retirement.
# 📮 probe and 🧮 value SEPARATED 260819 (JL: "I want to separate them"):
# 📮 = this point needs a QUESTION answered (the card, any answer shape);
# 🧮 = this point QUOTES one value, PP<NN>.v<n>, out of an answered card.
# 📮 doubles as Run ②'s glyph ON PURPOSE (same concept) and is END-ANCHORED
# in the hit scan, so prose ABOUT the Run can never grow a phantom chip
# (the ✅ lesson).
_MARK = {"🎯": "aim", "📚": "cite", "📮": "probe",
         "🧮": "value", "🔢": "value", "🖼": "display"}


def _latest_plan(page_src):
    """-> (Path, version) of the highest outline file, or (None, '')."""
    d = plan_dir(page_src.parent)
    best = latest_outline(d, page_src.stem)
    if best is None:
        return None, ""
    return best, version_tag(best) or best.stem.split("-outline-")[-1]


_PLAN_VERSION_RE = re.compile(r"^v(?P<generation>\d+)(?:\.(?P<shape>\d+))?(?:\.(?P<evidence>\d+))?$")


def _next_shape_version(tag):
    """Return the next bounded Shape version for a plan tag.

    A Bullet edit is a Shape change, never an evidence-only fold.  Legacy
    integer plans remain readable, but the first working edit gives them an
    explicit Shape component (``v1`` -> ``v1.1``).
    """
    m = _PLAN_VERSION_RE.fullmatch(tag or "")
    if not m:
        return "v1.1"
    generation = int(m.group("generation"))
    shape = int(m.group("shape") or 0)
    return "v%d.%d" % (generation, shape + 1)


def _typed_item_review(page_src, plan, plan_text, approved):
    """Read the typed Evidence Item table once for the plan-card join.

    The authored plan says *which* bullet owes an item; the authored item table
    says how that item will be surveyed and run; the status ladder derives the
    live state.  Keeping that join here (rather than re-parsing the evidence
    projection) lets a reader inspect Shape and Survey together without making
    either source authoritative over the other.
    """
    table = read_items(page_src)
    page_text = page_src.read_text(encoding="utf-8", errors="replace")
    page_accepted = bool(re.search(r"^accepted:\s*✅", page_text, re.M))
    root = repo_root(page_src.parent)
    by_target, active_rows, values, statuses = {}, {}, [], []
    counts = {word: 0 for word in ITEM_LADDER}
    types = {item_type: 0 for item_type in ITEM_TYPES}

    for item_id, target, head, item_type, expected, acceptance, folded in typed_bullets(plan_text):
        row = table.get(item_id)
        status = item_status(
            row, folded, page_accepted, plan.stat().st_mtime, root, page_src.parent
        )
        counts[status] += 1
        types[item_type] += 1
        statuses.append(status)
        if row is not None:
            active_rows[item_id] = row
        value = {
            "id": item_id,
            "target": target,
            "head": head,
            "name": ((row or {}).get("name")
                     or item_id.split("-", 2)[-1].replace("-", " ")),
            "label": (row or {}).get("label") or "",
            "type": item_type,
            "expected": (row or {}).get("expected") or expected,
            "acceptance": (row or {}).get("acceptance") or acceptance,
            "supporting_runs": (row or {}).get("supporting_runs") or "— not surveyed",
            "local_input": (row or {}).get("local_input") or "— not surveyed",
            "local_run": (row or {}).get("local_run") or "— not surveyed",
            "action": (row or {}).get("action") or "",
            "address": (row or {}).get("address") or "",
            "result": (row or {}).get("result") or "— no local Result bound",
            "decide": (row or {}).get("decide") or "☐ make / defer / drop",
            "decision": (row or {}).get("decision") or "",
            "status": status,
            "folded": folded,
        }
        by_target.setdefault(target, []).append(value)
        values.append(value)

    decided = sum(1 for value in values if value["decision"])
    return {
        "items": values,
        "by_target": by_target,
        "none_by_target": evidence_none_targets(plan_text),
        "counts": counts,
        "types": types,
        "decided": decided,
        "cycle": item_cycle(approved, active_rows, statuses, len(values)),
    }


def _paragraph_display(txt):
    """Local `C<n>.P<m>` -> the Page-global paragraph address plan_card prints."""
    paragraph_display = {}
    # Opening is reader orientation, not a paragraph in the Content Shape.
    # Page-global Content identities therefore begin at P1.
    next_page_paragraph = 1
    for match in re.finditer(r"(?m)^### C(\d+)\.P(\d+)\b", txt):
        local = "C%s.P%s" % match.groups()
        paragraph_display[local] = "C%s.P%d" % (match.group(1), next_page_paragraph)
        next_page_paragraph += 1
    return paragraph_display


def _source_realizations(page_text):
    """-> (Bullet address -> realized Page prose, Bullet address -> its `.S<n>` scaffolds)."""
    scaffolds = {}
    source_realizations = {}
    for m in re.finditer(r"(?m)^([^\n]*?)<!--\s*realizes:\s*"
                         r"(C\d+\.P\d+\.[BS]\d+)\s*-->\s*$", page_text):
        address = re.sub(r"\.S(\d+)$", r".B\1", m.group(2))
        prose = reader_prose(m.group(1)).strip()
        if prose:
            source_realizations.setdefault(address, []).append(prose)
        sm = re.search(r"\b(C\d+\.P\d+\.S\d+)\b", m.group(1))
        if sm:
            # canonical B key: a slot plan's realizes may say .S<n>; slot
            # number == position, so it is the same bullet (JAMA repro 260831)
            scaffolds.setdefault(address, []).append(sm.group(1))
    return source_realizations, scaffolds


def _join_wrapped(txt):
    """The plan's lines with each wrapped Bullet joined back onto one line."""
    # A bullet may WRAP, and its mark often sits on the continuation line.
    # Reading line-by-line called those bare, which is a false 🕳 on a bullet
    # the author did mark (found by driving it, 260817).
    lines, joined = txt.splitlines(), []
    i = 0
    while i < len(lines):
        cur = lines[i]
        if cur.startswith("- "):
            j = i + 1
            while (j < len(lines) and lines[j].startswith("  ")):
                continuation = lines[j].strip()
                # Keep an indented dash annotation distinguishable after the
                # legacy compatibility join.  A normal ASCII dash cannot be
                # used as the separator: prose such as "cases - and" would
                # then be mistaken for a Point annotation.  The presentation
                # parser consumes this private sentinel before rendering.
                if continuation.startswith("- "):
                    cur += " \u241e " + continuation[2:].strip()
                else:
                    cur += " " + continuation
                j += 1
            i = j
        else:
            i += 1
        joined.append(cur)
    return joined
