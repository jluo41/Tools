"""The evidence chain: from the insight rows a design acts on down to the data, each row
quoted from its page, with links to the Insight workbench.

Split out of design_page.py; design_page.py re-exports every name here."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live.design import (
    _BECAUSE, _LEVEL_WORD, _SIGNED, _board_page, _cited_page, _escape, _nearest_board, _read, because_rule, name_refs,
)


def _insight_href(root: Path | None, page: Path) -> str:
    """The Insight workbench's view of one page, when this server can serve it; '' when the
    page lies outside the server root (the label then shows without a link, audit N1)."""
    board = page.parent.parent.parent
    if root is None or not (board / "board.md").is_file():
        return ""
    try:
        rel_board = board.resolve().relative_to(Path(root).resolve()).as_posix()
        rel_page = page.resolve().relative_to(board.resolve()).as_posix()
    except (OSError, ValueError, RuntimeError):
        return ""
    return ("/_board/insight?path=" + quote("/" + ("" if rel_board == "." else rel_board + "/") + "board.md", safe="")
            + "&file=" + quote(rel_page, safe=""))


_LEVEL_ID = re.compile(r"^([A-Z])([DIKW])(\d{2})\b")


# ------------------------------------------------------------ evidence chain --
# The Rationale column says why a design is what it is, in two folds: the
# evidence chain, from the insight rows the design acts on down to the data, and each
# element of the design with what supports it. Every line is a row quoted from an insight
# page by its id, and every link between rows is one the insight pages already record.

_LINEAGE = re.compile(r"^(?:([DIKW]\d+(?:\.\.[DIKW]\d+)?)|\s+)\s*←\s+(.+?)\s*$")
_REF_TOKEN = re.compile(r"(?<![\w-])(?:([DIKW]\d{2}-[a-z]+)(?![a-z0-9])|([DIKW]\d+(?:\.\.[DIKW]?\d+)?)(?![\w-]))")
_PAGE_STEM_ID = re.compile(r"^([DIKW]\d{2}-[a-z]+|[A-Z][DIKW]\d{2})-")
_STEP_WORD = {"K": "because", "I": "shown by", "D": "counted from"}


def _page_id(page: Path) -> str:
    """`W01-full-send-salience.md` -> `W01-full`; the older `FW01-send-salience.md` -> `FW01`."""
    hit = _PAGE_STEM_ID.match(page.stem)
    return hit.group(1) if hit else page.stem


def _level(pid: str) -> str:
    return pid[0] if re.match(r"^[DIKW]\d", pid) else pid[1:2]


def _expand(token: str) -> list[str]:
    """`I4..I12` -> I4 … I12; any other token as it is."""
    hit = re.match(r"^([DIKW])(\d+)\.\.[DIKW]?(\d+)$", token)
    if not hit or not 0 <= int(hit.group(3)) - int(hit.group(2)) <= 60:
        return [token]
    return [f"{hit.group(1)}{n}" for n in range(int(hit.group(2)), int(hit.group(3)) + 1)]


def _row_lineage(text: str) -> dict[str, list[tuple[str, list[str]]]]:
    """`K1  ←  I02-full · I1, I2, I13-full   note` lines: row id -> [(page id, [row ids])].
    A line that starts with `←` goes on with the row above; a whole page cited has no rows."""
    out: dict[str, list[tuple[str, list[str]]]] = {}
    ids: list[str] = []
    for line in text.splitlines():
        hit = _LINEAGE.match(line)
        if not hit:
            ids = []
            continue
        if hit.group(1):
            ids = _expand(hit.group(1))
        found, cur = [], None
        for page, row in _REF_TOKEN.findall(re.split(r"\s{2,}", hit.group(2))[0]):
            if page:
                cur = (page, [])
                found.append(cur)
            elif cur is not None:
                cur[1].extend(_expand(row))
        for rid in ids:
            out.setdefault(rid, []).extend(found)
    return out


def _row_texts(text: str) -> dict[str, str]:
    """Row id -> its words on the page. A row of a fenced grid, its wrapped lines joined; a
    table row (one line, numbers in its cells) is read with its column names; else a
    paragraph that opens with the id in bold (`**D8, the cell grid.**`)."""
    rows: dict[str, str] = {}
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        header, last, col, raw = [], None, 0, {}
        for line in block.splitlines():
            if re.match(r"^id\s{2,}", line):
                header = re.split(r"\s{2,}", line.strip())[1:]
                continue
            hit = re.match(r"^([DIKW]\d+)\s{2,}(.+?)\s*$", line)
            if hit and "←" not in line:
                last = None
                if hit.group(1) in rows or hit.group(1) in raw:
                    continue
                raw[hit.group(1)] = {"cells": re.split(r"\s{2,}", hit.group(2)), "more": [], "header": header}
                last, col = hit.group(1), hit.start(2)
            elif last and "←" not in line and line.strip() and not line[:col].strip() and line[col:col + 1].strip():
                raw[last]["more"].append(re.split(r"\s{2,}", line[col:].strip())[0])
            else:
                last = None
        for rid, r in raw.items():
            cells, head = r["cells"], r["header"]
            numbers = all(re.search(r"\d|^[—✅❌🟡🚫⬜]$", c) for c in cells[1:])
            if not r["more"] and len(cells) >= 3 and len(head) == len(cells) and numbers:
                pairs = [f"{h} {c}" for h, c in zip(head[1:], cells[1:])
                         if h.lower() not in ("file", "from", "source", "run")]
                rows[rid] = " · ".join([cells[0], *pairs])
            else:
                rows[rid] = " ".join([cells[0], *r["more"]])
    for hit in re.finditer(r"\*\*`?([DIKW]\d+)`?([^*\n]*)\*\*", text):
        rows.setdefault(hit.group(1), (hit.group(1) + hit.group(2)).strip())
    return rows


def _compact(rows: list[str]) -> str:
    """[I2, I3, I4, I7] -> `I2..I4, I7`: a run of rows said as a range, as the pages write it."""
    out, i = [], 0
    while i < len(rows):
        j = i
        while (j + 1 < len(rows) and re.match(r"^[DIKW]\d+$", rows[j]) and rows[j + 1][:1] == rows[j][:1]
               and rows[j + 1][1:].isdigit() and int(rows[j + 1][1:]) == int(rows[j][1:]) + 1):
            j += 1
        out.append(f"{rows[i]}..{rows[j]}" if j - i >= 2 else ", ".join(rows[i:j + 1]))
        i = j + 1
    return ", ".join(out)


def because_rows(item: dict, missing: list[str] | None = None) -> list[dict]:
    """Every insight row the `because:` line names, in order (`W01-full · W1, W3`; pages
    split by `;`): {page, pid, id, do, text}, `do` None for a row that is not counsel.
    A named row not found on its page is left out and, given `missing`, listed there."""
    from live.design_actions import counsel_lines
    out = []
    for part in (item.get("because") or "").split(";"):
        part = part.strip()
        if not part or part.lower() in ("none", "no insight", "-"):
            continue
        hit = _BECAUSE.match(part)
        page = _cited_page(item, hit.group(1)) if hit else None
        if page is None:
            missing is not None and missing.append(part)
            continue
        text = _read(page)
        counsel, rows = {c["id"]: c for c in counsel_lines(text)}, _row_texts(text)
        for rid in re.split(r"\s*,\s*", hit.group(2)):
            c = counsel.get(rid)
            words = (("DO " if c["do"] else "DO NOT ") + c["text"]) if c else rows.get(rid, "")
            if words:
                out.append({"page": page, "pid": hit.group(1), "id": rid, "do": c["do"] if c else None, "text": words})
            elif missing is not None:
                missing.append(f"{hit.group(1)} · {rid}")
    return out


def _chain_heads(item: dict) -> tuple[list[dict], bool]:
    """The rows a chain starts from: the `because:` rows, else the DO rows of the cited
    Wisdom pages (False: the register names no rows)."""
    named = because_rows(item)
    if named or (item.get("because") or "").strip():
        return named, True
    from live.design_actions import counsel_lines
    heads = []
    for r in item.get("evidence_rows", []):
        if r["role"] == "handoff" and r["exists"]:
            heads += [{"page": r["file"], "pid": _page_id(r["file"]), "id": c["id"], "do": True,
                       "text": "DO " + c["text"]} for c in counsel_lines(_read(r["file"])) if c["do"]]
    return heads, False


def _walk(page: Path, rid: str, limit: int = 5) -> list[dict]:
    """One row and its first-cited parents down to the data, the way the insight board walks
    a cell: [{page, pid, id, text, also}], `also` the other parents of each row as
    (page id, page file or None, its rows)."""
    board, out, seen = _nearest_board(page), [], set()
    while page is not None and len(out) < limit and (page, rid) not in seen:
        seen.add((page, rid))
        text = _read(page)
        node = {"page": page, "pid": _page_id(page), "id": rid, "also": [],
                "text": _row_texts(text).get(rid, "") if rid else ""}
        out.append(node)
        nxt = None
        for ref, rows in (_row_lineage(text).get(rid, []) if rid else []):
            target = _board_page(board, ref)
            if nxt is None and target is not None:
                nxt = (target, rows[0] if rows else "")
                node["also"] += [(ref, target, _compact(rows[1:]))] if rows[1:] else []
            else:
                node["also"].append((ref, target, _compact(rows)))
        if nxt is None:
            break
        page, rid = nxt
    return out


def _code(escaped: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def _page_link(root: Path | None, page: Path) -> str:
    name = _escape(_page_words({"name": page.name}))
    href = _insight_href(root, page)
    signed = _SIGNED.search(_read(page))
    mark = " · signed" if signed and signed.group(1) == "✅" else ""
    return (f'<a href="{_escape(href)}">{name}</a>' if href else name) + f'<span class=mut>{mark}</span>'


def evidence_chain(item: dict) -> dict:
    """{chains: [[node]], limits: [row], named, also: [evidence row]} for the Rationale column."""
    heads, named = _chain_heads(item)
    missing: list[str] = []
    because_rows(item, missing)
    chains, limits = [], []
    for h in heads:
        if h["do"] is False:
            limits.append(h)
            continue
        nodes = _walk(h["page"], h["id"])
        if nodes:
            nodes[0]["text"] = h["text"]
            chains.append(nodes)
    on_chain = {n["page"].resolve() for c in chains for n in c} | {h["page"].resolve() for h in limits}
    also = [r for r in item.get("evidence_rows", []) if r["role"] in _SUPPORT_ROLES
            and r["exists"] and r["file"].resolve() not in on_chain]
    return {"chains": chains, "limits": limits, "named": named, "also": also, "missing": missing,
            "backing": [h for h in heads if h["do"]]}


def _chain_html(item: dict, root: Path | None, ev: dict) -> tuple[str, str]:
    """(summary, body) of the Evidence chain fold."""
    bad = "".join(f'<div class=bad>{_escape(m)} · no such row on the cited page</div>' for m in ev["missing"])
    if not ev["chains"] and not ev["limits"] and bad:
        return "row not found", bad
    if not ev["chains"] and not ev["limits"]:
        b = item.get("because_rule") or because_rule(item)
        if b["state"] == "ai":
            return "none", '<div class=mut>An AI idea, not from an insight: no insight row stands behind it.</div>'
        return "none", ('<div class=mut>No insight row named yet. A line '
                        '<code>because: &lt;page&gt; · &lt;row&gt;</code> for this design starts the chain.</div>')
    parts = [bad] if bad else []
    if not ev["named"]:
        parts.append('<div class=mut>No row is named for this design, so these are the DO rows of the cited Wisdom pages.</div>')
    if item.get("stance") == "challenge":
        parts.append('<div class=mut>Written to test this rule: if it loses, the rule holds.</div>')
    for chain in ev["chains"]:
        steps = []
        for i, n in enumerate(chain):
            step = (f'<div class=step>▲ {_STEP_WORD.get(_level(n["pid"]), "rests on")}</div>' if i else "")
            says = f'<span class=says>{_code(name_refs(_escape(n["text"]), n["page"]))}</span>' if n["text"] else ""
            rid = f'<span class=rid>{_escape(n["id"])}</span>' if n["id"] else ""
            also = ('<div class=also>also rests on ' + " · ".join(
                (_page_link(root, page) if page else _escape(ref)) + (f" {_escape(rows)}" if rows else "")
                for ref, page, rows in n["also"]) + '</div>' if n["also"] else "")
            steps.append(f'{step}<div class=node>{rid}{says}<div class=pg>{_page_link(root, n["page"])}</div>{also}</div>')
        parts.append(f'<div class=chain>{"".join(steps)}</div>')
    if ev["limits"]:
        parts.append('<h4 class=colh>Limits</h4>' + "".join(
            f'<div class="node limit"><span class=rid>{_escape(h["id"])}</span>'
            f'<span class=says>{_code(name_refs(_escape(h["text"]), h["page"]))}</span>'
            f'<div class=pg>{_page_link(root, h["page"])}</div></div>' for h in ev["limits"]))
    if ev["also"]:
        parts.append('<div class=also><b>Also cited</b> · ' + " · ".join(
            f'{_page_link(root, r["file"])} <span class=mut>({_LEVEL_WORD.get(_level_of(r), "source")})</span>'
            for r in ev["also"]) + '</div>')
    chains = ev["chains"]
    summary = (" → ".join(n["id"] or _page_id(n["page"]) for n in chains[0]) if len(chains) == 1
               else f'{len(chains)} chains' if chains else "limits only")
    return summary, "".join(parts)


_SUPPORT_ROLES = ("handoff", "evidence", "inspiration", "reference", "avoid")


def _page_words(row: dict) -> str:
    """An insight page by its name in words: `FW01-send-salience` -> `Send salience`."""
    # both page-id schemes: `FW01-send-salience` and `W01-full-send-salience`
    words = re.sub(r"^(?:[A-Z][DIKW]\d{2}|[DIKW]\d{2}-[a-z0-9]+)-", "", Path(row["name"]).stem).replace("-", " ").strip()
    return words[:1].upper() + words[1:]


def _level_of(row: dict) -> str:
    stem = Path(row["name"]).stem
    hit = _LEVEL_ID.match(stem) or re.match(r"^()([DIKW])\d{2}-[a-z0-9]+-", stem)
    return hit.group(2) if hit else "?"
