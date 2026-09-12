"""Standalone Page Markdown parser; also used by Board."""
import re

def split_sections(txt):
    """split on `## ` headings — but NEVER inside a ``` fence, or a template
    block that shows what `## 问题` looks like would tear its own file apart."""
    out, cur, buf, fence = {}, None, [], False
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if ln.startswith("## ") and not fence:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = ln[3:].strip(), []
        else:
            buf.append(ln)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out



def strip_notes(md):
    """Drop `<!-- ... -->` author notes, BEFORE the text is cut into sections.

    `ref/page-template.md` has always told authors a note "is dropped at generation
    either way". It was not: the only strip lived in the Stage Contract path, and
    the template's own notes happen to sit above the first `## `, where nothing
    renders. Written anywhere else a note came out as escaped `&lt;!--` prose
    (found 260726, adding a menu of optional sections to the ＋ button's stub).

    Order matters and cost an attempt to learn: `split_sections` reads any line
    starting `## ` as a heading, including one INSIDE a comment, so a note that
    lists `## Diagram` used to be torn in half and left a phantom section behind.
    Stripping first is what makes such a menu writable at all.

    Fenced blocks are protected, so a figure may still show a comment on purpose,
    and `<!-- haipipe:... -->` is kept because stage_contract reads those markers.
    """
    if "<!--" not in md:
        return md
    parts = re.split(r"(```)", md)
    inside = False
    for i, seg in enumerate(parts):
        if seg == "```":
            inside = not inside
        elif not inside:
            parts[i] = re.sub(r"<!--(?!\s*haipipe:).*?-->", "", seg, flags=re.S)
    return "".join(parts)


def parse_page(qid, txt, group="", file="", kind="question", family=""):
    """One Board Page (title, metadata, and sections) -> data dict."""
    lines = txt.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    qt = lines[i].lstrip("# ").strip() if i < len(lines) else qid
    # A paper page titles itself `SD00 · Ideation · …`, and every surface that
    # shows the title already prints the id beside it (the h2's `.hid`, the
    # index row's `.i`, the tab title), so the id came out two or three times
    # per header (JL 260831: "make this cleaner"). Strip it ONCE, here.
    qt = re.sub(r"^" + re.escape(qid) + r"\s*[·•:\-–—]\s*", "", qt) or qt
    i += 1
    meta = {
        "state": "🔴",
        "owner": "",
        "method": "",
        # route: outward | inward is the evidence-page type key (JL 260806):
        # it sits in the head, right after owner:/method:, and resolves the
        # page to for-literature or for-value where the filename cannot.
        "route": "",
        # page-type: is the OTHER type key. `route:` resolves the two evidence
        # variants; this one names the variant outright, and a plugin surface
        # gates on it (JL 260807), so it has to reach the page dict and the DOM.
        "page_type": "",
        "folder_kind": "",
        "task": "",
        "task_type": "",
        "session": "",
        "requires": "",
        "style_from": "",
        "provides": "",
        "contract_source_hash": "",
        "source_content": "",
    }
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(
            r"^(state|owner|method|route|page-type|folder-kind|task|task-type|session|requires|style-from|provides|contract-source-hash|source-content):\s*(.*)$",
            lines[i].strip(),
        )
        if m:
            meta[m.group(1).replace("-", "_")] = m.group(2).strip()
        i += 1
    # Author notes are dropped ONCE, here, so every downstream renderer sees clean
    # text. Doing it per-renderer was the old shape and it missed paths: a comment
    # written under ## Question came out as escaped `&lt;!--` prose on the page,
    # while ref/page-template.md had always promised it "is dropped at generation
    # either way" (found 260726). Fenced blocks are protected so a figure may still
    # show one, and `<!-- haipipe:contract:* -->` is kept because stage_contract
    # reads those markers back out of the rendered section.
    body_md = strip_notes("\n".join(lines[i:]))
    return dict(id=qid, title=qt, group=group, file=file, kind=kind, family=family,
                sec=split_sections(body_md), **meta)

