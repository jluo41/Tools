"""`plan-shape-off-type` · does a plan obey the shape its Page Type declares?

Every surviving Page Type declares a mode in an `outline:` block under
`metadata:`, and until 260819 nothing read it, so a plan's division shape was
whatever its author felt like (`haipipe-page-outline` 0.2.0 made it an exit).

NO `page-type:` KEY IS THE FLEXIBLE DEFAULT, which is 247 of this repo's 274
pages: those owe the base section order and nothing more, so this check returns
clean for them rather than inventing an expectation.
"""
from __future__ import annotations

import pathlib
import re

_DIV = re.compile(r"(?m)^##\s+C\d+\s*·\s*(.+?)\s*$")


def page_type(page_src: pathlib.Path) -> str:
    """-> the `page-type:` value from the page's own head, or ""."""
    head = page_src.read_text(encoding="utf-8", errors="replace")[:1200]
    m = re.search(r"(?m)^page-type:\s*(\S+)\s*$", head)
    return m.group(1) if m else ""


def type_outline(kind: str, skills_root: pathlib.Path) -> dict:
    """-> {mode, source, shape, words} read from the Page Type's own frontmatter.

    The block is INDENTED under `metadata:`, which is why a `^outline:` grep
    finds nothing and reported all eleven types as having none (260819)."""
    if not kind:
        return {}
    hits = list(skills_root.glob("*/page-types/haipipe-page-for-%s/SKILL.md" % kind))
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
    """-> [finding] · empty means the plan's shape is consistent with its type."""
    kind = page_type(page_src)
    if not kind:
        return []                      # the flexible default: nothing to check
    decl = type_outline(kind, skills_root)
    if decl.get("missing"):
        return ["page-type `%s` names no Page Type on disk" % kind]
    if decl.get("no_block"):
        return ["page-type `%s` declares no `outline:` block" % kind]

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
    for card in sorted(page_src.parent.glob("probe/PP*/card.md")):
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
            if re.match(r"^\s+(Note|More|Answered|Drawn):", lines[j]):
                folded = True
                break
            j += 1
        if not folded:
            out.append("C%d.P%d.B%d has no Note:/Answered:/Drawn: line"
                       % (cn, max(pn, 1), sn))
    return out


# 🧮 = value since 260819; 🔢 accepted as the pre-260819 legacy alias.
_MARKS = {"📮": "probe", "🧮": "value", "🔢": "value", "🖼": "display", "📚": "citation"}


def check_coverage(page_src: pathlib.Path, plan_text: str):
    """-> [finding] · every OWING mark is served by at least one card or unit.

    Self-consistency test ① of `haipipe-page-outline` §🚦. The PROBE receipt
    reports `coverage: n of n`, and nothing recomputed it, so a receipt could
    claim a coverage its own disk did not have.

    🎯 aim and ✅ have it are NOT owing marks and are skipped. A 📚 whose key is
    already known needs no card either, so an unserved 📚 is reported as a note
    rather than a gap: a person lands a bib entry by hand."""
    served = set()
    for card in sorted(page_src.parent.glob("probe/PP*/card.md")):
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

    _PATS = {"probe": r"PP\d+", "value": r"PP\d+(?:\.v\d+)?",
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
                    hit = any(page_src.parent.glob("probe/%s-*" % base))
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
