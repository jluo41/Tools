"""The marks in a working Word file, numbered, and accepting the ones a person picks (word_round_folder.py settle
--working each, JL 261122: "when I say settle, you ask me how to deal with the changes in the working file").

A mark is a tracked insertion (w:ins), a tracked deletion (w:del) or a comment. Accepting an insertion keeps its
words without the mark; accepting a deletion drops its words; accepting a comment closes it (the comment, its range
and its reference go). A mark not picked stays as it is.
"""
import re
import zipfile
from pathlib import Path

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
Q = lambda t: f"{{{W}}}{t}"


def _words(e, tag):
    return "".join(t.text or "" for t in e.iter(Q(tag)))


def listing(docx):
    """[(n, kind, author, words)] of every mark, in reading order then the comments; n counts from 1."""
    with zipfile.ZipFile(docx) as z:
        doc = etree.fromstring(z.read("word/document.xml"))
        com = etree.fromstring(z.read("word/comments.xml")) if "word/comments.xml" in z.namelist() else None
    out = []
    for e in doc.iter(Q("ins"), Q("del")):
        kind = etree.QName(e).localname
        words = _words(e, "t" if kind == "ins" else "delText")
        if words.strip():
            out.append([kind, e.get(Q("author")) or "?", words])
    if com is not None:
        for c in com.iter(Q("comment")):
            out.append(["comment", c.get(Q("author")) or "?", " ".join(_words(c, "t").split()), c.get(Q("id"))])
    return [(i, *m) for i, m in enumerate(out, 1)]


def accept(docx, picks):
    """Accept the marks numbered in `picks` (from listing) in place; returns how many were accepted."""
    docx = Path(docx)
    marks = listing(docx)
    want = {m[0] for m in marks if m[0] in picks}
    with zipfile.ZipFile(docx) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    names = [i.filename for i, _ in items]
    doc = etree.fromstring(items[names.index("word/document.xml")][1])
    n, gone_comments = 0, set()
    for e in list(doc.iter(Q("ins"), Q("del"))):
        kind = etree.QName(e).localname
        if not _words(e, "t" if kind == "ins" else "delText").strip():
            continue
        n += 1
        if n not in want:
            continue
        parent = e.getparent()
        if kind == "ins":
            at = parent.index(e)
            for child in list(e):
                parent.insert(at, child)
                at += 1
        parent.remove(e)
    for m in marks:
        if m[1] == "comment" and m[0] in want:
            gone_comments.add(m[4])
    for tag in ("commentRangeStart", "commentRangeEnd"):
        for e in list(doc.iter(Q(tag))):
            if e.get(Q("id")) in gone_comments:
                e.getparent().remove(e)
    for e in list(doc.iter(Q("commentReference"))):
        if e.get(Q("id")) in gone_comments:
            run = e.getparent()
            (run.getparent().remove(run) if len(run) <= 2 and run.tag == Q("r") else run.remove(e))
    new = {"word/document.xml": etree.tostring(doc, xml_declaration=True, encoding="UTF-8", standalone=True)}
    if "word/comments.xml" in names and gone_comments:
        com = etree.fromstring(items[names.index("word/comments.xml")][1])
        for c in list(com.iter(Q("comment"))):
            if c.get(Q("id")) in gone_comments:
                c.getparent().remove(c)
        new["word/comments.xml"] = etree.tostring(com, xml_declaration=True, encoding="UTF-8", standalone=True)
    tmp = docx.with_name(docx.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in items:
            out.writestr(info, new.get(info.filename, data))
    tmp.replace(docx)
    return len(want)


def picks(text):
    """'1,3-5' -> {1, 3, 4, 5}."""
    out = set()
    for part in re.split(r"[,\s]+", (text or "").strip()):
        if "-" in part:
            a, b = part.split("-", 1)
            out |= set(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out
