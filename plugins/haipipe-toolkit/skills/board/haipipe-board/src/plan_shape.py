"""`plan-shape-off-type` · does a plan obey its Folder Page Face?

Phase-owned Folder contracts and legacy Page Types declare a mode in an
`outline:` block under `metadata:`. Workflow phases resolve first; Page-Type
folders remain the compatibility fallback for families not yet migrated.

NO `page-type:` KEY IS THE FLEXIBLE DEFAULT, which is 247 of this repo's 274
pages: those owe the base section order and nothing more, so this check returns
clean for them rather than inventing an expectation.
"""
from __future__ import annotations

import pathlib
import re

from .common import evidence_lane_dirs
from .folder_contract import resolve as resolve_folder_contract

_DIV = re.compile(r"(?m)^##\s+C\d+\s*·\s*(.+?)\s*$")


def _probe_cards(page_src: pathlib.Path):
    seen = set()
    for lane in evidence_lane_dirs(page_src.parent, "probe"):
        for card in sorted(lane.glob("PP*/card.md")):
            key = card.parent.name
            if key not in seen:
                seen.add(key)
                yield card


def page_type(page_src: pathlib.Path) -> str:
    """-> the `page-type:` value from the page's own head, or ""."""
    head = page_src.read_text(encoding="utf-8", errors="replace")[:1200]
    m = re.search(r"(?m)^page-type:\s*(\S+)\s*$", head)
    return m.group(1) if m else ""


def folder_kind(page_src: pathlib.Path) -> str:
    """Return the current `folder-kind:` identity from a Folder head."""
    head = page_src.read_text(encoding="utf-8", errors="replace")[:1200]
    m = re.search(r"(?m)^folder-kind:\s*(\S+)\s*$", head)
    return m.group(1) if m else ""


def type_outline(kind: str, skills_root: pathlib.Path) -> dict:
    """Read Page-Face outline metadata from its semantic owner.

    The block is INDENTED under `metadata:`, which is why a `^outline:` grep
    finds nothing and reported all eleven types as having none (260819)."""
    if not kind:
        return {}
    phase = resolve_folder_contract(
        skills_root, folder_kind=kind, legacy_page_type=kind
    )
    hits = ([phase.path] if phase else
            list(skills_root.glob("*/page-types/haipipe-page-for-%s/SKILL.md" % kind))
            # paper ships its types as journey-phase skills since 260831
            or list(skills_root.glob("*/workflow-phases/haipipe-paper-%s/SKILL.md" % kind))
            or list(skills_root.glob("paper/haipipe-paper-%s/SKILL.md" % kind)))
    if not hits:
        return {"missing": kind}
    t = hits[0].read_text(encoding="utf-8", errors="replace")
    blk = re.search(r"(?ms)^  outline:\s*$(.*?)(?=^  \S|^---)", t)
    if not blk:
        return {"no_block": str(hits[0])}
    body = blk.group(1)

    def row(name):
        m = re.search(r"(?m)^\s+%s:\s*(.*?)\s*(?:#.*)?$" % name, body)
        return (m.group(1).strip().strip('"') if m else "")

    out = {
        "mode": row("mode"),
        "source": row("source"),
        "marker": row("marker"),
        "fallback": row("fallback"),
        "shape": row("shape"),
        "type_path": str(hits[0]),
    }
    words = re.findall(r"\{([^}]*)\}", out["shape"])
    out["words"] = [w.strip() for w in words[0].split(",")] if words else []
    return out


def _declared_source(page_src: pathlib.Path) -> str:
    """Return one Section's explicit structure-source, when present."""
    text = page_src.read_text(encoding="utf-8", errors="replace")[:6000]
    match = re.search(r"(?m)^structure-source:\s*(\S.*?)\s*$", text)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def _resolve_source(
    value: str, skills_root: pathlib.Path, type_path: str = ""
) -> pathlib.Path | None:
    """Resolve a declared structure source without guessing a latest file."""
    raw = value.strip().lstrip("./")
    if not raw:
        return None
    path = pathlib.Path(raw).expanduser()
    candidates = [path] if path.is_absolute() else [skills_root / path]
    if not path.is_absolute():
        candidates.append(skills_root / "paper" / path)
        if type_path:
            candidates.append(pathlib.Path(type_path).parent / path)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def _is_venue_page(path: pathlib.Path) -> bool:
    """True when the chosen structure source is itself a venue Page: filename
    QBv<n>- (the engine's own venue resolution rule) or a `page-type: venue`
    line in its head."""
    if re.match(r"QBv\d+-", path.name):
        return True
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except OSError:
        return False
    return bool(re.search(r"^page-type:\s*venue\s*$", head, re.M))


def _has_marker(path: pathlib.Path, marker: str) -> bool:
    """Marker rows count only before the first Markdown heading."""
    text = path.read_text(encoding="utf-8", errors="replace")
    head = re.split(r"(?m)^#\s", text, maxsplit=1)[0]
    key, sep, value = marker.partition(":")
    if not sep:
        return False
    return bool(
        re.search(
            rf"(?m)^{re.escape(key.strip())}:\s*{re.escape(value.strip())}\s*$",
            head,
        )
    )


def check(page_src: pathlib.Path, plan_text: str, skills_root: pathlib.Path):
    """Return findings when a plan violates its Folder's Page Face shape."""
    current = folder_kind(page_src)
    legacy = page_type(page_src)
    current_contract = (
        resolve_folder_contract(skills_root, folder_kind=current)
        if current else None
    )
    kind = current if current_contract else legacy
    if not kind:
        return []                      # the flexible default: nothing to check
    decl = type_outline(kind, skills_root)
    key_name = "folder-kind" if current_contract else "page-type"
    if decl.get("missing"):
        return ["%s `%s` names no Page Face contract on disk" % (key_name, kind)]
    if decl.get("no_block"):
        return ["%s `%s` declares no `outline:` block" % (key_name, kind)]

    if current_contract and legacy:
        legacy_contract = resolve_folder_contract(
            skills_root, legacy_page_type=legacy
        )
        if legacy_contract and legacy_contract.path != current_contract.path:
            return [
                "folder-kind `%s` and legacy page-type `%s` resolve to different phases"
                % (current, legacy)
            ]

    titles = _DIV.findall(plan_text)
    mode, out = decl.get("mode", ""), []

    if mode == "grammar" and decl["words"]:
        allowed = decl["words"]
        for i, ti in enumerate(titles, 1):
            first = ti.split()[0].rstrip(":·,").strip() if ti.split() else ""
            if first not in allowed:
                out.append("C%d first word %r is outside the closed set %s"
                           % (i, first, allowed))
        last = decl["shape"]
        m = re.search(r"(\w+) is one page-level division, always last", last) or \
            re.search(r"(\w+)\(last\)", last)
        if m and titles:
            want = m.group(1)
            got = titles[-1].split()[0].rstrip(":·,") if titles[-1].split() else ""
            if got != want:
                out.append("the last division is %r; %s declares %r must be last"
                           % (got, kind, want))

    elif mode == "resolved":
        src = decl.get("source", "")
        if not src:
            out.append("mode is `resolved` and the type names no `source:`")
        elif not list(skills_root.glob(src.lstrip("./"))):
            out.append("`source:` %r resolves to nothing on disk; a missing "
                       "source is a HOLE, never a licence to invent one" % src)
        marker = decl.get("marker", "")
        fallback = decl.get("fallback", "")
        if marker or fallback:
            chosen_raw = _declared_source(page_src)
            chosen = _resolve_source(chosen_raw, skills_root, decl.get("type_path", ""))
            fallback_path = _resolve_source(
                fallback, skills_root, decl.get("type_path", "")
            )
            if not chosen_raw:
                out.append(
                    "resolved Page Type requires an explicit `structure-source:`"
                )
            elif chosen is None:
                out.append("`structure-source:` %r resolves to nothing" % chosen_raw)
            elif fallback_path is not None and chosen == fallback_path:
                pass
            elif _is_venue_page(chosen):
                # a QBv venue Page is the CURRENT desk authority by
                # construction (the bank is maintained); the marker gate is
                # for loose template files, whose era nothing else dates
                pass
            elif marker and not _has_marker(chosen, marker):
                out.append(
                    "`structure-source:` %r lacks required marker `%s`; use the "
                    "declared fallback instead" % (chosen_raw, marker)
                )
            if fallback and fallback_path is None:
                out.append("declared fallback %r resolves to nothing" % fallback)

    elif mode == "fixed" and decl.get("shape"):
        # A fixed type LISTS its divisions; the shape row is that list.
        want = [w.strip() for w in re.split(r"[·→|,]", decl["shape"]) if w.strip()]
        if want and len(titles) and len(titles) != len(want):
            out.append("mode is `fixed` with %d declared divisions; the plan has %d"
                       % (len(want), len(titles)))
    return out


_ADDR = re.compile(r"C(\d+)\.P(\d+)\.B(\d+)")


def plan_addresses(plan_text: str) -> set:
    """-> every C<n>.P<n>.B<n> a plan actually HAS, counted by position.

    The same walk `live/outline.py` does, so the two cannot disagree about what
    an address is: `## C<n>` opens a division, any other `## ` ends the plan's
    divisions, `### ` opens a paragraph, `- B` is a bullet."""
    out, cn, pn, sn = set(), 0, 0, 0
    for line in plan_text.splitlines():
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            break
        if re.match(r"^## C\d+\b", line):
            cn += 1; pn = 0; continue
        if line.startswith("### "):
            pn += 1; sn = 0; continue
        if line.startswith("- B"):
            sn += 1
            out.add("C%d.P%d.B%d" % (cn, max(pn, 1), sn))
    return out


def check_serves(page_src: pathlib.Path, plan_text: str):
    """-> [finding] · every card and unit `serves:` names a REAL plan address.

    Self-consistency test ② of `haipipe-page-outline` §🚦. It exists because on
    260819 three of this board's own cards pointed at bullets that had been
    renumbered after the tick, and a person read all three out by eye before any
    tool noticed. An address is FROZEN before a card points at it, so a stale one
    means either the card is wrong or the plan was edited after `approved: ✅`.
    """
    have = plan_addresses(plan_text)
    if not have:
        return []
    out = []
    for card in _probe_cards(page_src):
        m = re.search(r"(?m)^serves:\s*(.+?)\s*$", card.read_text(
            encoding="utf-8", errors="replace"))
        for a in (_ADDR.findall(m.group(1)) if m else []):
            addr = "C%s.P%s.B%s" % a
            if addr not in have:
                out.append("%s serves %s, which this plan does not have"
                           % (card.parent.name.split("-")[0], addr))
    for readme in sorted(page_src.parent.glob("display/*/README.md")):
        m = re.search(r"(?m)^-?\s*serves:\s*(.+?)\s*$", readme.read_text(
            encoding="utf-8", errors="replace"))
        for a in (_ADDR.findall(m.group(1)) if m else []):
            addr = "C%s.P%s.B%s" % a
            if addr not in have:
                out.append("%s serves %s, which this plan does not have"
                           % (readme.parent.name, addr))
    return out


def check_bullet_grammar(plan_text: str):
    """-> [finding] · `bullet-missing-note`: a bullet with no folded detail line.

    The bullet grammar is `haipipe-plugin-outline` §✂️ (260819): a terse HEAD,
    then a `Note:`/`Answered:`/`Drawn:` continuation the surface folds, the
    mark last — every bullet carries one of the three. EVERY plan, approved or
    not (JL 260819: "remove all the legacy-grammar, I don't want to maintain
    the old things"): an old-grammar plan is rewritten on its next OUTLINE
    pass, as v<N+1> when a tick froze it. Found on `QC1-visitlbp` 260819: a
    fold pass appended Answered:/Drawn: onto 260817 long-sentence bullets and
    every check stayed green."""
    out, cn, pn, sn = [], 0, 0, 0
    lines = plan_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            break
        if re.match(r"^## C\d+\b", line):
            cn += 1; pn = 0; continue
        if line.startswith("### "):
            pn += 1; sn = 0; continue
        if not line.startswith("- B"):
            continue
        sn += 1
        j, folded = i + 1, False
        while (j < len(lines) and lines[j].startswith("  ")
               and not lines[j].lstrip().startswith("- ")):
            if re.match(r"^\s+(Note|Evidence|Accept|More|Answered|Drawn|Routed):", lines[j]):
                folded = True
                break
            j += 1
        if not folded:
            out.append("C%d.P%d.B%d has no Note:/Evidence:/Answered:/Drawn: line"
                       % (cn, max(pn, 1), sn))
    return out


# 🧮 = value since 260819; 🔢 accepted as the pre-260819 legacy alias.
_MARKS = {"📮": "probe", "🧮": "value", "🔢": "value", "🖼": "display", "📚": "citation"}


def check_coverage(page_src: pathlib.Path, plan_text: str):
    """Return findings for typed Evidence Items, with legacy mark fallback.

    Self-consistency test ① of `haipipe-page-outline` §④. A SURVEY receipt
    reports `items: n of n`, and nothing recomputed it, so a receipt could
    claim a coverage its own disk did not have.

    Current grammar requires a typed id, expectation, immediate Accept line,
    and exactly one matching record in ``<stem>-evidence-items.md``. Plans with
    no ``Evidence:`` line use the legacy icon/card check below during migration.
    """
    if re.search(r"(?m)^\s*Evidence:", plan_text):
        item_re = re.compile(
            r"^\s*Evidence:\s*(E\d+-(VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*)\s*·\s*(.+)$"
        )
        wanted, out, cn, pn, bn = {}, [], 0, 0, 0
        lines = plan_text.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"^## C(\d+)\b", line)
            if m:
                cn, pn, bn = int(m.group(1)), 0, 0
                continue
            m = re.match(r"^### C(\d+)\.P(\d+)\b", line)
            if m:
                cn, pn, bn = int(m.group(1)), int(m.group(2)), 0
                continue
            m = re.match(r"^- [BS](\d+)\s*·", line)
            if m:
                bn = int(m.group(1))
                continue
            m = item_re.match(line)
            if not m:
                continue
            item_id = m.group(1)
            target = f"C{cn}.P{pn}.B{bn}"
            if item_id in wanted:
                out.append(f"{item_id} appears more than once in the plan")
            wanted[item_id] = target
            if i + 1 >= len(lines) or not re.match(r"^\s*Accept:\s*\S", lines[i + 1]):
                out.append(f"{item_id} has no immediate Accept line")

        table = page_src.parent / "outline" / f"{page_src.stem}-evidence-items.md"
        records = {}
        if table.is_file():
            record_re = re.compile(
                r"^###\s+(E\d+-(?:VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*)"
                r"\s*·\s*(C\d+\.P\d+\.B\d+)\s*·"
            )
            for line in table.read_text(encoding="utf-8", errors="replace").splitlines():
                match = record_re.match(line)
                if match:
                    if match.group(1) in records:
                        out.append(f"{match.group(1)} appears more than once in the table")
                    records[match.group(1)] = match.group(2)
        for item_id, target in wanted.items():
            if item_id not in records:
                out.append(f"{item_id} has no Evidence Item record")
            elif records[item_id] != target:
                out.append(f"{item_id} targets {records[item_id]} in the table, expected {target}")
        for item_id in sorted(set(records) - set(wanted)):
            out.append(f"{item_id} is in the table but not the current plan")
        return out

    # Legacy icon/card grammar below, read-only during migration.
    served = set()
    for card in _probe_cards(page_src):
        m = re.search(r"(?m)^serves:\s*(.+?)\s*$", card.read_text(
            encoding="utf-8", errors="replace"))
        served |= {"C%s.P%s.B%s" % a for a in (_ADDR.findall(m.group(1)) if m else [])}
    for readme in sorted(page_src.parent.glob("display/*/README.md")):
        m = re.search(r"(?m)^-?\s*serves:\s*(.+?)\s*$", readme.read_text(
            encoding="utf-8", errors="replace"))
        served |= {"C%s.P%s.B%s" % a for a in (_ADDR.findall(m.group(1)) if m else [])}

    # ONE LAW IN TWO READERS, for real this time (260819 smoke): join wrapped
    # bullets the way live/outline.py does, so a mark on a continuation line
    # is not invisible; then THE MARK IS THE LAST EMOJI in the end-anchored
    # window, so a dual-emoji legacy tail (`📚 Gray2021 · 🧮 proof`) owes ONE
    # kind, not two.
    bullets, cn, pn, sn = [], 0, 0, 0
    lines = plan_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            break
        if re.match(r"^## C\d+\b", line):
            cn += 1; pn = 0; i += 1; continue
        if line.startswith("### "):
            pn += 1; sn = 0; i += 1; continue
        if not line.startswith("- B"):
            i += 1; continue
        sn += 1
        body, j = line, i + 1
        while (j < len(lines) and lines[j].startswith("  ")
               and not lines[j].lstrip().startswith("- ")):
            body += " " + lines[j].strip()
            j += 1
        bullets.append(("C%d.P%d.B%d" % (cn, max(pn, 1), sn), body))
        i = j

    # A 📚 whose key sits in this page's own bibex/ needs no card: a person
    # lands bib entries by hand (the docstring said so; the code now does).
    bib_keys = set()
    for bib in sorted(page_src.parent.glob("bibex/*.bib")):
        bib_keys |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)",
                                   bib.read_text(encoding="utf-8",
                                                 errors="replace")))

    # `PP<NN>` standing alone: `Routed: RD01 S1-PP5` is a Round row id, not a card

    _PATS = {"probe": r"(?<![A-Za-z0-9-])PP\d+", "value": r"(?<![A-Za-z0-9-])PP\d+(?:\.v\d+)?",
             "display": r"Display\d+",
             "citation": r"QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*"}
    out, cited = [], set()
    for addr, body in bullets:
        tail = body[-64:]
        # tail-wide credit for the reverse join: every kind named anywhere in
        # the window counts as cited, even on a multi-chip legacy tail.
        for emo, kind in _MARKS.items():
            at = tail.rfind(emo)
            if at >= 0:
                cited |= set(re.findall(_PATS[kind], tail[at:]))
        # the OWING mark is the last emoji in the window
        win, wat = None, -1
        for emo, kind in _MARKS.items():
            at = body.rfind(emo)
            if at > wat and len(body) - at <= 64:
                win, wat = kind, at
        if win is None:
            continue
        if win == "citation":
            keys = re.findall(_PATS["citation"], body[wat:])
            if not keys or not all(k in bib_keys for k in keys):
                out.append("%s owes citation and bibex/ lacks the key" % addr)
            continue
        # A mark WITH refs is satisfied by the refs RESOLVING (the named unit
        # or card exists on disk); only a BARE mark owes a serving backlink.
        # Without this, C4.P5.B6's worked example — `🖼 Display3`, a real,
        # rendered unit — read as owing, because Display3's README serves a
        # different bullet (double-citation is legal, the law is ≥1).
        refs = re.findall(_PATS[win], body[wat:])
        if refs:
            for ref in refs:
                base = ref.split(".")[0]
                if win == "display":
                    hit = any(page_src.parent.glob("display/*%s-*" % base)) \
                        or any(page_src.parent.glob("display/*%s" % base))
                else:
                    hit = any(any(lane.glob("%s-*" % base))
                              for lane in evidence_lane_dirs(page_src.parent, "probe"))
                if not hit:
                    out.append("%s names %s and no such %s exists on disk"
                               % (addr, ref, win))
            continue
        if addr not in served:
            out.append("%s owes %s and no card or unit serves it" % (addr, win))

    # The REVERSE join (JL 260819, on seeing Display4 orphaned: "you should
    # try to make every display to be used" and, when its README's serves:
    # back-pointer was offered as the fix, "you should cite it"): a unit
    # sitting in display/ that no bullet CITES BY MARK is COVERAGE debt, same
    # rank as an unserved mark — a serves: line in the README is not enough,
    # because the plan's reader never sees it. A README may carry a
    # `retired:` line to say the unit is deliberately out of the plan.
    for readme in sorted(page_src.parent.glob("display/*/README.md")):
        name = readme.parent.name
        txt = readme.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?m)^-?\s*retired:", txt):
            continue
        m = re.search(r"Display\d+", name)
        if (m.group(0) if m else name) not in cited:
            out.append("%s is on disk and no bullet cites it" % name)
    return out


# ── the head and Note law (haipipe-plugin-outline ref/plan-grammar.md §3, §4) ──
_MARK_EMOJI = "🎯📚📮🧮🔢🖼"
NOTE_MAX = 30          # the specimen's longest Note is 27 words
_LABEL_RE = re.compile(r"^\s+(Note|Evidence|Accept|More|Answered|Drawn|Routed):")


def _head_words(head: str) -> list:
    """The words of a bullet head: the `S<n> ·` slot tag, a `Cut:`/`C<n>:` tag,
    the marks and their ids are not counted; a head is judged on what it SAYS."""
    h = re.sub(r"^(?:S\d+\s*·\s*)", "", head.strip())
    h = re.sub(r"^(?:Cut:|C\d+:)\s*", "", h)
    h = re.split(r"[%s]" % _MARK_EMOJI, h)[0]
    h = h.replace("·", " ")
    return [w for w in re.split(r"\s+", h.strip()) if w and not re.fullmatch(r"[\W_]+", w)]


def _bullets_with_notes(plan_text: str):
    """-> [(address, head, note_lines, extra_lines)] for every bullet: the head,
    the labelled continuation lines, and the indented lines that follow a Note
    WITHOUT a label (a Note that wrapped onto a second source line)."""
    out, cn, pn, sn = [], 0, 0, 0
    lines = plan_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            break
        mc = re.match(r"^## C(\d+)\b", line)
        if mc:
            cn = int(mc.group(1)); pn = 0; i += 1; continue
        if line.startswith("### "):
            mp = re.match(r"^### C\d+\.P(\d+)\b", line)
            pn = int(mp.group(1)) if mp else pn + 1; sn = 0; i += 1; continue
        m = re.match(r"^- (?:\[[ xX]\] )?B(\d+)\s*·\s*(.*)$", line)
        if not m:
            i += 1; continue
        sn = int(m.group(1))
        head = m.group(2)
        notes, extra, j, in_note = [], [], i + 1, False
        while j < len(lines) and lines[j].startswith("  ") and not lines[j].lstrip().startswith("- "):
            if _LABEL_RE.match(lines[j]):
                in_note = lines[j].lstrip().startswith("Note:")
                notes.append(lines[j].strip())
            elif in_note and lines[j].strip():
                extra.append(lines[j].strip())
            j += 1
        out.append(("C%d.P%d.B%d" % (cn, max(pn, 1), sn), head, notes, extra))
        i = j
    return out


def check_head_style(plan_text: str):
    """-> (fails, gaps) · the head and Note teeth of ref/plan-grammar.md.

    fails  `head-too-long`     a head over 11 words
           `note-too-long`     a Note over NOTE_MAX words, its wrapped source
                               lines joined (a hard wrap is still one Note)
    gaps   `head-too-short`    a head under 4 words (`Trait relevance`): the
                               code-word style, reported so the migration debt
                               is visible without failing every old plan"""
    fails, gaps = [], []
    for addr, head, notes, extra in _bullets_with_notes(plan_text):
        n = len(_head_words(head))
        if n > 11:
            fails.append("%s head-too-long: %d words (max 11): %r" % (addr, n, head[:60]))
        elif 0 < n < 4:
            gaps.append("%s head-too-short: %d word(s), a code-word head: %r" % (addr, n, head[:60]))
        note = " ".join([x[5:] for x in notes if x.startswith("Note:")] + extra)
        note = re.split(r"[%s]" % _MARK_EMOJI, note)[0]
        nw = len([w for w in re.split(r"\s+", note.strip()) if w])
        if nw > NOTE_MAX:
            fails.append("%s note-too-long: %d words (max %d)" % (addr, nw, NOTE_MAX))
    return fails, gaps


def _content_text(page_src: pathlib.Path) -> str:
    try:
        text = page_src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r"(?ms)^## Content\b[^\n]*\n(.*?)(?=^## |\Z)", text)
    body = m.group(1) if m else ""
    body = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith(">"))
    return re.sub(r"\s+", " ", body).lower()


def check_note_quotes_page(page_src: pathlib.Path, plan_text: str, window: int = 8):
    """-> [finding] · `note-quotes-page`: a head or Note that carries the page's
    own sentence (any run of `window` consecutive words found verbatim in the
    page's Content). The plan says what a sentence must DO; the sentence lives
    on the page."""
    content = _content_text(page_src)
    if not content:
        return []
    out = []
    for addr, head, notes, _extra in _bullets_with_notes(plan_text):
        texts = [head] + [re.sub(r"^(Note|More):\s*", "", n) for n in notes
                          if n.startswith(("Note:", "More:"))]
        for t in texts:
            t = re.split(r"[%s]" % _MARK_EMOJI, t)[0]
            words = [w for w in re.split(r"\s+", re.sub(r"\s+", " ", t).lower().strip()) if w]
            hit = None
            for k in range(0, max(0, len(words) - window + 1)):
                run = " ".join(words[k:k + window])
                if len(run) >= 40 and run in content:
                    hit = run; break
            if hit:
                out.append("%s note-quotes-page: %r appears verbatim in the page" % (addr, hit[:70]))
                break
    return out
