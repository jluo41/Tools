"""The Story and Ideation readers: a Story page or topic read into its tables, divisions and Section Narrative
records; the Ideation page read into Idea cards; Story prose set for a reading cell.
Moved from paper.py, which re-exports the names its callers import from there (`from live.paper import ...`)."""
import re

from src.outline_version import latest_outline, plan_dir
from src.plan_shape import iter_plan_bullets

from live.paper_text import SECTION_ROW, _DIV_RE, _EV_RE, clean, divisions, esc, read, scalar, table_rows


def idea_divisions(text):
    """`### N · Idea <n>: <research question>` divisions under Content → {n: {"title", "fields"}}
    where fields are the division's `**Field**` blocks in page order, each a
    list of paragraphs (a `- ` line stays a list item)."""
    out, cur, field = {}, None, None
    inside = False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            cur = None
            continue
        if not inside:
            continue
        m = re.match(r"^###\s+§?\d+\s*·\s*Idea\s+(\d+)\s*:\s*(.*?)\s*$", line)
        if m:
            cur = {"title": m.group(2), "fields": []}
            out[int(m.group(1))] = cur
            field = None
            continue
        if line.startswith("### ") or line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        fm = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", line.strip())
        if fm:
            field = [fm.group(1).strip(), []]
            cur["fields"].append(field)
            if fm.group(2).strip():
                field[1].append(fm.group(2).strip())
            continue
        if field is not None and line.strip():
            field[1].append(line.rstrip())
    return out


def _table_headers(text, first_cell):
    """The header cells of the table whose first data row matches first_cell."""
    pat = re.compile(first_cell)
    header = None
    for line in (text or "").splitlines():
        s_ = line.strip()
        if not s_.startswith("|"):
            header = None
            continue
        cells = [clean(c) for c in s_.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c or "-") for c in cells):
            continue
        if header is None:
            header = cells
            continue
        if cells and pat.fullmatch(cells[0]):
            return header
    return None


def ideation(d):
    """The Idea Cards of Story00, one collapsed card each (JL 260916: "like the
    evidence card in workbench-page, I can open and hide it")."""
    p = d["story00"]
    if p is None:
        return {"present": False}
    b = d["board"]
    folder = (b / p["rel"]).parent if p["rel"] else None
    out = {"present": True, "stem": p["stem"], "rel": p["rel"],
           "state": clean(scalar(p["text"], "state", "⬜ no state line")),
           "ideas": [], "source": "", "items": [], "receipts": []}
    # ① the page's own Ideas (ranked) table, when Content carries one; its ids are `i01` or `IDEA-01`
    # (ScalingGlucose's s01-ideation writes IDEA-NN, and its ideas showed as "No idea yet")
    idea_id = r"i\d+|IDEA-\d+"
    rows = table_rows(p["text"], idea_id)
    if rows:
        out["source"] = "Content · Ideas (ranked) table"
        headers = _table_headers(p["text"], idea_id) or []
        named = [h.strip().lower() for h in headers]        # the contract orders novelty · pilot · venue fit ·
        vi = next((k for k, h in enumerate(named) if h.startswith("verdict")), 4)   # verdict · target · went to;
        wi = next((k for k, h in enumerate(named) if h.startswith("went")), 5)      # read those two by name
        for c in rows:
            fields = [(headers[i] if i < len(headers) else "col %d" % (i + 1), c[i])
                      for i in range(2, len(c)) if c[i] and c[i] not in ("—", "-")]
            out["ideas"].append({"id": c[0], "title": c[1] if len(c) > 1 else "",
                                 "verdict": c[vi] if len(c) > vi else "⬜ open",
                                 "went": c[wi] if len(c) > wi else "",
                                 "address": "", "chips": [], "bullets": [],
                                 "fields": fields, "items": []})
    # ② else the plan's `Idea <n>: <research question>` divisions (an Ideation Page before Content)
    plan = latest_outline(plan_dir(folder), p["stem"]) if folder else None
    if plan is not None:
        ptext = read(plan)
        if not out["ideas"]:
            out["source"] = "outline plan · Idea divisions (page has no Content yet)"
            seen = {}
            for blk in iter_plan_bullets(ptext):
                m = re.match(r"^Idea\s+(\d+)\s*:\s*(.*)$", blk["division_title"])
                if not m:
                    continue
                key = blk["division"]
                if key not in seen:
                    seen[key] = {"id": "i%02d" % int(m.group(1)), "title": m.group(2),
                                 "address": key, "chips": [], "bullets": [],
                                 "verdict": "⬜ open", "went": "", "fields": [], "items": []}
                    out["ideas"].append(seen[key])
                notes = [x for x in blk["continuation"] if re.match(r"^(Note|Annotation|More):", x)]
                evidence = next((x for x in blk["continuation"] if x.startswith("Evidence:")), "")
                seen[key]["bullets"].append({
                    "address": blk["address"], "bullet": blk["bullet"], "head": blk["head"],
                    "notes": [re.sub(r"^\w+:\s*", "", n) for n in notes],
                    "evidence": re.sub(r"^Evidence:\s*", "", evidence)})
                seen[key]["chips"] += [c for c in _EV_RE.findall(blk["body"])
                                       if c not in seen[key]["chips"]]
    # ③ the idea itself: the page's Idea <n> division, when Content carries one
    divs = idea_divisions(p["text"])
    for idea in out["ideas"]:
        n = re.search(r"\d+", idea["id"])
        div = divs.get(int(n.group(0))) if n else None
        idea["substance"] = div["fields"] if div else []
        if div and not idea.get("title"):
            idea["title"] = div["title"]
    # ④ the authored Evidence Item contract, with its Verified tick
    if folder:
        items = read(plan_dir(folder) / (p["stem"] + "-evidence-items.md"))
        for m in re.finditer(r"^###\s+(E\d{2}-[A-Z]+-[\w-]+)\s*·\s*(\S+)\s*·\s*(.*)$", items, re.M):
            tail = items[m.end():]
            nxt = tail.find("\n### ")
            body = tail if nxt < 0 else tail[:nxt]
            v = re.search(r"\*\*Verified\*\*:\s*(\S+)", body)
            item = {"id": m.group(1), "target": m.group(2), "desc": m.group(3).strip(),
                    "verified": v.group(1) if v else "⬜"}
            out["items"].append(item)
            for idea in out["ideas"]:
                if idea["address"] and item["target"].startswith(idea["address"] + "."):
                    idea["items"].append(item)
        # ⑤ the I3 receipt and handoff files haipipe-paper-ideation names
        for rel, what in (("workflow/selection.yaml", "I3 selection receipt"),
                          ("handoff/paper-ideation.yaml", "final handoff"),
                          ("projection/paper-ideation-sync.yaml", "working sync packet")):
            out["receipts"].append({"what": what, "rel": rel,
                                    "state": "present" if (folder / rel).is_file() else "absent"})
    return out


def story(d, p):
    from live.paper_story_tree import question_blocks
    t = p["text"]
    s = {"stem": p["stem"], "rel": p["rel"],
         "state": clean(scalar(t, "state", "⬜ no state line")),
         "divisions": divisions(t),
         "rq": table_rows(t, r"RQ\d+"), "rq_h": _table_headers(t, r"RQ\d+") or [],
         "e": table_rows(t, r"E-?\d+(?:\s*\(.*\))?"), "e_h": _table_headers(t, r"E-?\d+(?:\s*\(.*\))?") or [],
         "dd": table_rows(t, r"D\d+"), "dd_h": _table_headers(t, r"D\d+") or [],
         "tt": table_rows(t, r"[TB]\d+"), "tt_h": _table_headers(t, r"[TB]\d+") or [],
         "qq": table_rows(t, r"Q\d+"), "qq_h": _table_headers(t, r"Q\d+") or [],
         "pp": table_rows(t, r"P\d+"), "pp_h": _table_headers(t, r"P\d+") or [],
         "qb": question_blocks(t),
         "sections": [], "sec_h": [], "order": []}
    s["sec_h"] = _table_headers(t, SECTION_ROW) or []
    # the Spine is §1 Identity, §2 Pitch, §4 Stakes; matched by title so a legacy numbered
    # Story part (Story02-roadmap's `1 · Mission`) does not pose as an Identity
    s["spine"] = [(n, title, parse_division(division_body(t, n)))
                  for n, title in s["divisions"]
                  if re.match(r"(identity|pitch|stakes)\b", title.strip().lower())]
    seen = set()
    for c in table_rows(t, SECTION_ROW):
        # `S-<id>`, `S-<id> (label)` or `S-<id> · §0 label` (JL 260925: MISQ's main rows)
        sid = re.split(r"\s*[(·]", c[0], maxsplit=1)[0].strip()
        if sid in seen:              # the same Section listed again in a later table
            continue
        seen.add(sid)
        page = next((x for x in d["sections"] if x["stem"] == sid), None)
        s["sections"].append({"id": sid, "target": c[0][len(sid):].strip(" ()·"),
                              "question": c[1] if len(c) > 1 else "", "cells": c, "heads": s["sec_h"],
                              "rel": page["rel"] if page else None,
                              "page_state": clean(scalar(page["text"], "state", "")) if page else ""})
    # the same rows written as records (no pipe tables in a Story, JL): `**S-<id> (N) · job**`
    # then `- **Field**: value` lines, inside the Section Narrative division
    narrative = next((n for n, title in s["divisions"] if title.strip().lower().startswith("section narrative")), None)
    for rec in (section_records(division_body(t, narrative)) if narrative is not None else []):
        if rec["id"] in seen:
            continue
        seen.add(rec["id"])
        page = next((x for x in d["sections"] if x["stem"] == rec["id"]), None)
        s["sections"].append(dict(rec, rel=page["rel"] if page else None,
                                  page_state=clean(scalar(page["text"], "state", "")) if page else ""))
    m = re.search(r"<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->", t, re.S)
    if m:
        s["order"] = [l.strip()[2:].strip() for l in m.group(1).splitlines()
                      if l.strip().startswith("- ")]
    return s


_RECORD = re.compile(r"^\*\*(S-[\w-]+|t\d{2}_[\w-]+)\s*(?:\(([^)]*)\))?\s*(?:·\s*(.*?))?\*\*\s*$")
_FIELD = re.compile(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.*)$")


def section_records(body):
    """§8 Section Narrative rows written as records → the table rows' shape: {id, target, question,
    cells, heads}. `**S-<id> (N) · one job**` opens a record; its `- **Field**: value`
    lines are its cells; the Reader question field is the question."""
    out, cur = [], None
    for line in (body or "").splitlines():
        m = _RECORD.match(line.strip())
        if m:
            cur = {"id": m.group(1), "target": (m.group(2) or "").strip(), "question": "",
                   "fields": [("One job", clean(m.group(3) or ""))] if m.group(3) else []}
            out.append(cur)
            continue
        if line.startswith("#"):
            cur = None
            continue
        f = _FIELD.match(line.strip()) if cur is not None else None
        if f:
            key, value = f.group(1).strip(), clean(f.group(2))
            if key.lower() == "reader question":
                cur["question"] = value[:1].upper() + value[1:]
            else:
                cur["fields"].append((key, value))
    for r in out:
        r["cells"] = [r["id"], r["question"]] + [v for _, v in r["fields"]]
        r["heads"] = ["Section", "Reader question"] + [k for k, _ in r.pop("fields")]
    return out


def division_body(text, n):
    """The Markdown between `### n · …` and the next `### ` inside Content."""
    lines = (text or "").splitlines()
    inside, grab, out = False, False, []
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            if grab:
                break
            continue
        if not inside:
            continue
        m = _DIV_RE.match(line)
        if m:
            if grab:
                break
            grab = int(m.group(1)) == n
            continue
        if grab:
            out.append(line)
    return "\n".join(out)


def parse_division(body):
    """A Story division → (face rows, subsections, paragraphs).
    face rows   the ```text block's `EMOJI LABEL   value` lines, continuation
                lines joined; the Story's compact identity card
    subsections `#### n.m · Title` with the paragraph under each
    paragraphs  loose prose before any subsection (the Pitch is written so)"""
    face, subs, paras = [], [], []
    in_fence, cur_sub, buf = False, None, []
    def flush():
        nonlocal buf
        t = " ".join(x.strip() for x in buf if x.strip())
        if t:
            (subs[-1][1].append(t) if cur_sub is not None else paras.append(t))
        buf = []
    for line in (body or "").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            m = re.match(r"^\s*([^\w\s]+)?\s*([A-Z][A-Z /-]{1,24}?)\s{2,}(.*)$", line)
            if m and m.group(2).strip():
                face.append([m.group(2).strip().title(), m.group(3).strip()])
            elif face and line.strip():
                face[-1][1] += " " + line.strip()
            continue
        m = re.match(r"^####\s+(.*?)\s*$", line)
        if m:
            flush()
            cur_sub = m.group(1)
            subs.append([cur_sub, []])
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith("**") and cur_sub is None and not paras:
            continue          # the division's bold lead line is a label, not content
        buf.append(line)
    flush()
    return face, subs, paras


_ABBR = ("e.g.", "i.e.", "et al.", "vs.", "cf.", "Fig.", "Eq.", "No.", "Dr.", "St.", "U.S.")


def sentences(text):
    """Split prose at sentence ends. A decimal (1.19) never splits, because the
    split needs white space after the mark; a known abbreviation rejoins."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z(\[“\"'])", (text or "").strip())
    out = []
    for part in parts:
        if out and out[-1].endswith(_ABBR):
            out[-1] += " " + part
        else:
            out.append(part)
    return [x for x in out if x]


def prose(paragraphs):
    """Story prose for a reading cell: paragraphs stay apart, and a long
    paragraph is set one sentence per line (display only; the source is untouched)."""
    paras = [paragraphs] if isinstance(paragraphs, str) else list(paragraphs)
    html_ = []
    for par in paras:
        sents = sentences(par)
        if len(par) > 300 and len(sents) > 1:
            html_.append('<span class="para">%s</span>' % " ".join('<span class="sent">%s</span>' % inline(x) for x in sents))
        else:
            html_.append('<span class="para">%s</span>' % inline(par))
    return " ".join(html_)


def inline(text):
    """Escape prose, then render the two inline marks a Story uses:
    `code` → <code>, **bold** → <b>. Nothing else is interpreted."""
    t = esc(text or "")
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t
