"""wordtc.py · a co-author Word round: read their marks, build ours as tracked changes, render in Word, check.

    wordtc.py read   <file.docx> [--author NAME] [--changes] [--text]
                     comments and tracked changes per author; --changes their words; --text every paragraph
                     as Word shows it (accepted view, W<nnnn> | text), the words a `find` must match;
                     words struck by formatting (not a tracked deletion) are listed, since they stay in the text
    wordtc.py build  <base.docx> <edits.yaml> <out.docx> --author "Junjie Luo"   each edit a tracked change (track_changes.py)
    wordtc.py try    <base.docx> <edits.yaml>              which edits locate on their own (find missing, not unique)
    wordtc.py render <file.docx> [--out file.pdf]          PDF by Microsoft Word (AppleScript), else LibreOffice
    wordtc.py check  <base.docx> <out.docx> --author NAME  everyone else's marks and comments kept; ours counted
    wordtc.py diff   <sent.docx> <now.docx>                what a reader changed since we sent it: paragraphs whose
                     text changed, comments added or removed, tracked changes added, accepted or rejected

edits.yaml: {edits: [{id, find, new?, comment?, anchor?, why}]} (fields: track_changes.py's docstring).
Nothing here sends a file: word_round.py import / push does, on the person's word.
"""
import argparse, collections, contextlib, io, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "excalidraw" / "excalidraw-draft" / "ref"))
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORD_BOX = Path.home() / "Library/Containers/com.microsoft.Word/Data/Documents/word-track-change"


def marks(path):
    """{'ins': Counter(author), 'del': Counter(author), 'comments': [(author, text)]}"""
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        com = ET.fromstring(z.read("word/comments.xml")) if "word/comments.xml" in z.namelist() else None
    out = {"ins": collections.Counter(), "del": collections.Counter(), "comments": [], "changes": []}
    for kind in ("ins", "del"):
        for e in doc.iter(W + kind):
            a = e.get(W + "author") or "?"
            out[kind][a] += 1
            words = "".join(t.text or "" for t in e.iter(W + ("t" if kind == "ins" else "delText")))
            if words.strip():
                out["changes"].append((kind, a, words))
    if com is not None:
        for c in com.iter(W + "comment"):
            out["comments"].append((c.get(W + "author") or "?",
                                    " ".join("".join(t.text or "" for t in c.iter(W + "t")).split())))
    return out


def struck(path):
    """Words with strike-through FORMATTING outside a tracked deletion: a co-author's 'delete this' that
    Word keeps in the accepted text."""
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
    out = []
    for r in doc.iter(W + "r"):
        rpr = r.find(W + "rPr")
        s = rpr.find(W + "strike") if rpr is not None else None
        if s is not None and s.get(W + "val", "true") not in ("0", "false"):
            words = "".join(t.text or "" for t in r.iter(W + "t"))
            if words.strip():
                out.append(words)
    return out


def cmd_read(a):
    if a.text:
        from track_changes import paragraphs, para_text
        import docx
        body = docx.Document(a.file).element.body
        for n, p in enumerate(paragraphs(body)):
            if para_text(p).strip():
                print(f"W{n:04d} | {para_text(p)}")
        return
    m = marks(a.file)
    for w in struck(a.file):
        print(f"  struck by formatting (still in the text): {w[:120]}")
    print(f"tracked insertions {dict(m['ins'])}\ntracked deletions  {dict(m['del'])}\ncomments {len(m['comments'])}")
    for who, text in m["comments"]:
        if not a.author or who == a.author:
            print(f"  [{who}] {text}")
    if a.changes:
        for kind, who, words in m["changes"]:
            if not a.author or who == a.author:
                print(f"  {kind} [{who}] {words[:160]}")


def load(edits):
    return (yaml.safe_load(Path(edits).read_text()) or {}).get("edits") or []


def cmd_try(a):
    from track_changes import write_tracked
    bad = 0
    ids = [e.get("id") for e in load(a.edits)]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        bad += 1
        print(f"✗ duplicate id {i}: every edit needs its own id")
    with tempfile.TemporaryDirectory() as tmp:
        for e in load(a.edits):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    write_tracked(a.base, [e], Path(tmp) / "t.docx", author="try")
            except SystemExit as x:
                bad += 1
                print(f"✗ {x}")
    print(f"{len(load(a.edits)) - bad} locate, {bad} do not")
    sys.exit(1 if bad else 0)


def cmd_build(a):
    from track_changes import write_tracked
    r = write_tracked(a.base, load(a.edits), a.out, author=a.author)
    print(f"{Path(a.out).name}: {r['edits']} edits, {r['comments']} comments by {a.author}")


def cmd_render(a):
    src = Path(a.file).resolve()
    pdf = Path(a.out).resolve() if a.out else src.with_suffix(".pdf")
    if Path("/Applications/Microsoft Word.app").exists():
        WORD_BOX.mkdir(parents=True, exist_ok=True)       # Word is sandboxed: it saves only inside its container
        inside, made = WORD_BOX / src.name, WORD_BOX / (src.stem + ".pdf")
        shutil.copy2(src, inside)
        made.unlink(missing_ok=True)
        script = f'''tell application "Microsoft Word"
  set d to open file name (POSIX path of "{inside}")
  delay 2
  save as d file name (POSIX path of "{made}") file format format PDF
  close d saving no
end tell'''
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=600)
        if made.is_file():
            shutil.move(made, pdf)
            inside.unlink(missing_ok=True)
            print(f"Word: {pdf} ({pages(pdf)} pages)")
            return
        print(f"Word export failed ({r.stderr.strip()[:200]}); using LibreOffice", file=sys.stderr)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf.parent), str(src)],
                   capture_output=True, check=True)
    made = pdf.parent / (src.stem + ".pdf")
    if made != pdf:
        shutil.move(made, pdf)
    print(f"LibreOffice: {pdf} ({pages(pdf)} pages; Word may paginate differently)")


def pages(pdf):
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    return m[1] if m else "?"


def cmd_check(a):
    b, o = marks(a.base), marks(a.out)
    ok = True
    for kind in ("ins", "del"):
        for who, n in b[kind].items():
            if who != a.author and o[kind][who] < n:
                ok = False
                print(f"✗ {who}: {kind} {n} -> {o[kind][who]}")
    lost = collections.Counter(b["comments"]) - collections.Counter(o["comments"])
    if lost:
        ok = False
        print(f"✗ {sum(lost.values())} comments lost: {list(lost)[:3]}")
    print(f"others kept: {'yes' if ok else 'NO'} · comments {len(b['comments'])} -> {len(o['comments'])} · "
          f"{a.author}: +{o['ins'][a.author] - b['ins'][a.author]} insertions, "
          f"+{o['del'][a.author] - b['del'][a.author]} deletions")
    sys.exit(0 if ok else 1)


def texts(path):
    from track_changes import paragraphs, para_text
    import docx
    return [t for t in (para_text(p).strip() for p in paragraphs(docx.Document(path).element.body)) if t]


def cmd_diff(a):
    import difflib
    before, after = texts(a.sent), texts(a.now)
    n = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        n += 1
        for t in before[i1:i2]:
            print(f"  - P{i1 + 1:04d} | {t[:200]}")
        for t in after[j1:j2]:
            print(f"  + P{j1 + 1:04d} | {t[:200]}")
    b, o = marks(a.sent), marks(a.now)
    added = collections.Counter(o["comments"]) - collections.Counter(b["comments"])
    gone = collections.Counter(b["comments"]) - collections.Counter(o["comments"])
    for who, text in added:
        print(f"  comment added [{who}] {text[:200]}")
    for who, text in gone:
        print(f"  comment removed [{who}] {text[:200]}")
    cb, co = collections.Counter(b["changes"]), collections.Counter(o["changes"])
    new = co - cb
    settled = collections.Counter(who for _, who, _ in (cb - co).elements())
    for kind, who, words in new:
        print(f"  {kind} added [{who}] {words[:160]}")
    print(f"text: {n} places changed · comments +{sum(added.values())} -{sum(gone.values())} · "
          f"tracked changes +{sum(new.values())}, accepted or rejected {dict(settled)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("read"); p.add_argument("file"); p.add_argument("--author"); p.add_argument("--changes", action="store_true"); p.add_argument("--text", action="store_true")
    p = sp.add_parser("try"); p.add_argument("base"); p.add_argument("edits")
    p = sp.add_parser("build"); p.add_argument("base"); p.add_argument("edits"); p.add_argument("out"); p.add_argument("--author", required=True)
    p = sp.add_parser("render"); p.add_argument("file"); p.add_argument("--out")
    p = sp.add_parser("diff"); p.add_argument("sent"); p.add_argument("now")
    p = sp.add_parser("check"); p.add_argument("base"); p.add_argument("out"); p.add_argument("--author", required=True)
    a = ap.parse_args()
    {"read": cmd_read, "try": cmd_try, "build": cmd_build, "render": cmd_render, "check": cmd_check, "diff": cmd_diff}[a.cmd](a)


if __name__ == "__main__":
    main()
