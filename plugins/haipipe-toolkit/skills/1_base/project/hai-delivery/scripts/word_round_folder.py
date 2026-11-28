"""A co-author round as one folder (JL 261122, Pp-AgreeableRx-Discrention): the working Word files at the top, and
four subfolders that say where each copy came from. word_round.py passes these verbs here.

    RoundN-vMMDD/
    ├─ 1-<Name>-vMMDD-manuscript.docx      working files only, Track Changes on: what co-authors open and edit
    ├─ 2-<Name>-vMMDD-cover-letter.docx
    ├─ 3-<Name>-vMMDD-portal.docx
    ├─ previous/    where the round started: the earlier version of each file, each with its own vMMDD
    ├─ track/       a marked copy of a working file, saved before any clean (and the red/blue diff PDFs)
    ├─ clean/       the LaTeX PDF and the LaTeX-made Word of each file, no marks, named ...-<kind>-clean.docx
    └─ submission/  only the portal uploads, numbered by portal slot; frozen after Submit

    python word_round_folder.py open-round <rounds-dir> [--date MMDD] [--file N=<built.docx>]...
    python word_round_folder.py settle <round-dir> <N|all> [--clean N=<docx>[,<pdf>]]... [--rebuild CMD]
                                       [--draft N=<docx>]... [--version MMDD] [--report <md>] [--dry-run]
                                       [--working keep|accept|each [--pick 1,3-5]]
    python word_round_folder.py adopt-round <flat-dir> --name <Name> --date MMDD --file N=<file>:<kind>... [--into <paper>]
    python word_round_folder.py refresh <round-dir> <N|all> [--clean N=<docx>[,<pdf>]]... [--config <toml>]
                                        a working file nobody edited becomes the clean build (old copy to track/)
    python word_round_folder.py take-clean <round-dir> <N> --clean N=<docx>[,<pdf>] [--dry-run]   (round_clean.py)
                                        a co-author edited clean/'s Word: their marked copy becomes the working file
    python word_round_folder.py clean-names <round-dir> [--dry-run]   an older clean/: names gain -clean
    python word_round_folder.py submit <round-dir> --config <paper-build.toml> [--date MMDD]
    python word_round_folder.py status <round-dir>          (also round-status, the name word_round.py passes)

One number per document, the same in every folder. No PDF at the top. Every subfolder written gets one marker,
`last-update-YYYY-MM-DD HH.MM.txt` (a dot: SharePoint refuses a colon), listing its files with their times; the
writer replaces the old one. Nothing here writes into previous/ after open-round, or into submission/ after submit.
Rejected names (JL): changes/ (a log nobody reads), diff/ (the diffs are in track/), final/ (clean/ is not frozen).
"""
import argparse
import datetime
import difflib
import re
import shutil
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # word_marks.py beside it
ROUND = re.compile(r"^Round(\d+)-v(\d{4})$")
WORKING = re.compile(r"^(\d+)-(.+)-v(\d{4})-(.+?)\.(docx|pdf)$")
STAMP = "%Y-%m-%d %H.%M"
FROZEN = "frozen: submitted"
# CT_Settings children that come BEFORE w:trackRevisions (ECMA-376 order), so the new element lands where Word reads it
BEFORE_TRACK = ("writeProtection", "view", "zoom", "removePersonalInformation", "removeDateAndTime",
                "doNotDisplayPageBoundaries", "displayBackgroundShape", "printPostScriptOverText",
                "printFractionalCharacterWidth", "printFormsData", "embedTrueTypeFonts", "embedSystemFonts",
                "saveSubsetFonts", "saveFormsData", "mirrorMargins", "alignBordersAndEdges",
                "bordersDoNotSurroundHeader", "bordersDoNotSurroundFooter", "gutterAtTop", "hideSpellingErrors",
                "hideGrammaticalErrors", "activeWritingStyle", "proofState", "formsDesign", "attachedTemplate",
                "linkStyles", "stylePaneFormatFilter", "stylePaneSortMethod", "documentType", "mailMerge",
                "revisionView")
SOURCES = {"manuscript": "the Section drafts (the Section whose text holds it)",
           "cover-letter": "t31_cover-letter", "portal": "portal-values.yaml"}
PLACED = ".placed-{n}.docx"   # in track/: the clean Word last placed at the top, settle's baseline
SHUT = ("previous", "submission")   # never written after they are made
CLEAN = "-clean"   # clean/ names end so, never the working name (AgreeableJama 261123: a co-author edited clean/'s same-named copy)


def top_name(clean_file):
    """The working file's name for a clean/ copy: N-<Name>-vMMDD-<kind>-clean.docx -> N-<Name>-vMMDD-<kind>.docx."""
    p = Path(clean_file)
    return p.stem[:-len(CLEAN)] + p.suffix if p.stem.endswith(CLEAN) else p.name


def now():
    return datetime.datetime.now()


def parse(p):
    """(number, name, MMDD, kind) of a round file, or None."""
    m = WORKING.match(Path(p).name)
    return (int(m[1]), m[2], m[3], m[4]) if m else None


def working(round_dir):
    """{number: path} of the working Word files at the top of a round."""
    return {parse(p)[0]: p for p in sorted(Path(round_dir).glob("*.docx")) if parse(p) and not p.name.startswith("~$")}


def guard(dst, round_dir, allow=()):
    """Refuse a write into a folder that is shut (previous/ after open-round, submission/ after submit)."""
    rel = Path(dst).resolve().relative_to(Path(round_dir).resolve())
    if rel.parts and rel.parts[0] in SHUT and rel.parts[0] not in allow:
        raise SystemExit(f"refused: {rel} is in {rel.parts[0]}/, which this step never writes")


def marker(folder, purpose="", made=None):
    """Replace the folder's last-update marker with one listing its files and their times. `made` maps a file name to
    how it was made (LaTeX PDF, Word from the LaTeX sources, a python writer, a converter), printed under its line, so
    a reader knows which copy came from where (JL 261123: "how could we know which one is the latex generated?")."""
    folder = Path(folder)
    if folder.name == "previous" and any(folder.glob("last-update-*.txt")):   # written once (AgreeableJama 261123)
        raise SystemExit(f"refused: {folder.parent.name}/previous/ keeps the marker open-round wrote; it is never rewritten")
    kept, name = {}, None              # a file keeps the note the last marker gave it, unless a new one is given
    for old in folder.glob("last-update-*.txt"):
        for line in old.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d  (.+)$", line)
            if m:
                name = m[1]
            elif name and line.strip().startswith("made by: "):
                kept[name] = line.strip()[len("made by: "):]
    made = {**kept, **(made or {})}
    for old in folder.glob("last-update-*.txt"):
        old.unlink()
    t = now()
    files = sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith((".", "~$")))
    lines = [f"{folder.parent.name}/{folder.name}: last updated {t:%Y-%m-%d %H:%M} {t.astimezone():%Z}".rstrip(), ""]
    if purpose:
        lines += [purpose, ""]
    for p in files:
        lines.append(f"{datetime.datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d %H:%M}  {p.name}")
        if made.get(p.name):
            lines.append(f"                  made by: {made[p.name]}")
    out = folder / f"last-update-{t:{STAMP}}.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def track_on(docx):
    """Switch Track Changes on (w:trackRevisions in word/settings.xml); True when the file changed."""
    docx = Path(docx)
    with zipfile.ZipFile(docx) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    names = [i.filename for i, _ in items]
    if "word/settings.xml" not in names:
        return False
    k = names.index("word/settings.xml")
    s = items[k][1].decode("utf-8")
    m = re.search(r"<w:trackRevisions\b[^>]*/>", s)
    if m and not re.search(r'w:val="(?:0|false|off)"', m[0]):
        return False
    if m:
        s = s[:m.start()] + "<w:trackRevisions/>" + s[m.end():]
    else:
        at = re.search(r"<w:settings\b[^>]*>", s).end()
        for tag in BEFORE_TRACK:
            for e in re.finditer(rf"<w:{tag}\b[^>]*/>|<w:{tag}\b[^>]*>.*?</w:{tag}>", s, flags=re.S):
                at = max(at, e.end())
        s = s[:at] + "<w:trackRevisions/>" + s[at:]
    items[k] = (items[k][0], s.encode("utf-8"))
    tmp = docx.with_name(docx.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in items:
            out.writestr(info, data)
    tmp.replace(docx)
    return True


def tracking(docx):
    with zipfile.ZipFile(docx) as z:
        s = z.read("word/settings.xml").decode("utf-8") if "word/settings.xml" in z.namelist() else ""
    m = re.search(r"<w:trackRevisions\b[^>]*/>", s)
    return bool(m) and not re.search(r'w:val="(?:0|false|off)"', m[0])


def in_use(docx):
    """Why the file cannot be touched now (open in Word: AutoSave writes over any outside change), or ''."""
    docx = Path(docx)
    for lock in docx.parent.glob("~$*"):
        if len(lock.name) > 2 and docx.name.endswith(lock.name[2:]):
            return f"Word's lock file {lock.name} is beside it"
    try:
        pids = subprocess.run(["lsof", "-t", "--", str(docx)], capture_output=True, text=True).stdout.split()
    except FileNotFoundError:
        pids = []
    return f"open in process {', '.join(pids)}" if pids else ""


# ── open-round ───────────────────────────────────────────────────────────────────────────────────────────────────
def rounds(parent):
    return sorted((int(ROUND.match(p.name)[1]), p) for p in Path(parent).iterdir() if p.is_dir() and ROUND.match(p.name))


def open_round(parent, mmdd, built):
    """A new RoundN-vMMDD/: the last round's working files into previous/, the new working files at the top."""
    have = rounds(parent)
    if not have:
        raise SystemExit(f"no RoundN-vMMDD folder in {parent}: make the first round with adopt-round <flat-dir>")
    last_n, last = have[-1]
    new = Path(parent) / f"Round{last_n + 1}-v{mmdd}"
    if new.exists():
        raise SystemExit(f"{new.name} exists")
    start = working(last)
    if not start:
        raise SystemExit(f"{last.name} has no working files at its top")
    (new / "previous").mkdir(parents=True)
    for n, p in start.items():
        shutil.copy2(p, new / "previous" / p.name)
    marker(new / "previous", "Where this round started: the earlier version of each file.")
    for n, p in start.items():
        num, name, _, kind = parse(p)
        dst = new / f"{num}-{name}-v{mmdd}-{kind}.docx"
        shutil.copy2(built.get(n, p), dst)
        track_on(dst)
        print(f"{dst.name}  (from {Path(built.get(n, p)).name}, Track Changes on)")
    for n, src in built.items():
        if n not in start:
            raise SystemExit(f"--file {n}: no file {n} in {last.name}; numbers stay the same across rounds")
    return new


# ── settle ───────────────────────────────────────────────────────────────────────────────────────────────────────
def accepted_text(docx):
    """The paragraphs as Word shows them with every mark accepted."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "draw/hai-draw/gallery/draft/ref"))
    from track_changes import paragraphs, para_text
    import docx as _docx
    return [t for t in (para_text(p).strip() for p in paragraphs(_docx.Document(str(docx)).element.body)) if t]


def original_text(docx):
    """The paragraphs as they were before any mark: inserted text left out, deleted text kept. Two files compared
    this way differ only by edits typed with Track Changes off (an insertion inside a paragraph is not one)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "draw/hai-draw/gallery/draft/ref"))
    from track_changes import W, paragraphs
    import docx as _docx
    out = []
    for p in paragraphs(_docx.Document(str(docx)).element.body):
        words = [t.text or "" for t in p.iter(W("w:t"), W("w:delText"))
                 if not any(a.tag == W("w:ins") for a in t.iterancestors()) and
                 not any(a.tag == W("w:txbxContent") for a in t.iterancestors())]
        if "".join(words).strip():
            out.append("".join(words).strip())
    return out


def marks(docx):
    """wordtc.py's reader: tracked insertions and deletions and comments, each with its author."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "word-track-change/scripts"))
    from wordtc import marks as _marks
    return _marks(docx)


def last_seen(round_dir, n):
    """The last synced point of file n: the clean Word last placed at the top (track/.placed-<n>.docx), else its
    newest marked copy in track/ (a settle that kept the marks left them there, so they are not synced twice), else
    its clean Word, else where the round started."""
    # a copy keeps the working file's own time, so the marked copies are ordered by the stamp in their names
    stamp = lambda p: re.search(r"-tracked-(\d{4}-\d{2}-\d{2} \d{2}\.\d{2}(?:\.\d{2})?)\.docx$", p.name)
    marked = sorted((p for p in (Path(round_dir) / "track").glob(f"{n}-*-tracked-*.docx") if stamp(p)),
                    key=lambda p: stamp(p)[1].ljust(19, "0"))
    placed = Path(round_dir) / "track" / PLACED.format(n=n)
    if placed.is_file():   # the clean Word last placed at the top; a later marked copy removes it (Pp-AgreeableRx 261122)
        return placed
    if marked:
        return marked[-1]
    for sub in ("clean", "previous"):
        hit = sorted((Path(round_dir) / sub).glob(f"{n}-*.docx"), key=lambda p: (p.stat().st_mtime, p.name))
        if hit:
            return hit[-1]
    return None


def changes(docx, base):
    """Every change in a working file since `base`, with its author: tracked marks and comments that base did not
    hold, and the words that differ from base, which catches an edit typed with Track Changes off."""
    import collections
    m = marks(docx)
    old = marks(base) if base is not None else {"changes": [], "comments": []}
    fresh = collections.Counter(m["changes"]) - collections.Counter(old["changes"])
    out = [(k, a, w) for k, a, w in fresh.elements()]
    out += [("comment", a, t) for a, t in (collections.Counter(m["comments"]) - collections.Counter(old["comments"])).elements()]
    if base is not None:   # both with every mark left out: what remains differs only by untracked typing
        before, after = original_text(base), original_text(docx)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
            if op != "equal":
                out.append(("untracked", "?", f"{' / '.join(before[i1:i2])[:200]} -> {' / '.join(after[j1:j2])[:200]}"))
    return out


QUESTION = ("How should the working file {name} be dealt with? Run settle again with one of:\n"
            "  --working keep     it stays as it is, marks and comments included (the next settle starts from the "
            "track/ copy)\n"
            "  --working accept   it becomes the clean Word: no marks, comments closed, Track Changes still on\n"
            "  --working each     list each mark and comment; then --pick 1,3-5 accepts those, the rest are kept")


def settle_one(round_dir, docx, *, clean=None, draft=None, version=None, dry=False, rebuild=None,
               how=None, pick=None):
    """One working file, in order: refuse if open in Word; copy it marked into track/; list its changes since the
    last synced point; rebuild; place clean/; check draft == clean/; then ask how to deal with the working file."""
    num, name, old, kind = parse(docx)
    why = in_use(docx)
    if why:
        raise SystemExit(f"{docx.name}: {why}; close it in Word first (AutoSave writes over any outside change)")
    base = last_seen(round_dir, num)
    lines = [f"## {docx.name}", ""]
    t = now()
    track = Path(round_dir) / "track" / f"{num}-{name}-v{old}-{kind}-tracked-{t:{STAMP}}.docx"
    if track.is_file() and track.read_bytes() != docx.read_bytes():   # a second settle in the same minute
        track = track.with_name(f"{num}-{name}-v{old}-{kind}-tracked-{t:{STAMP}.%S}.docx")
    guard(track, round_dir)
    if base is not None and base.parent.name == "track" and base.read_bytes() == docx.read_bytes():
        track = base   # nothing changed since the last marked copy: it stays the one copy
    elif not dry:
        track.parent.mkdir(exist_ok=True)
        shutil.copy2(docx, track)
        (track.parent / PLACED.format(n=num)).unlink(missing_ok=True)   # the marked copy is the newest synced point
        marker(track.parent, "Before anyone accepts changes or closes comments in a working file, a marked copy of "
                             "it is saved here first.")
    if track.name.startswith("."):      # the placed clean Word, unchanged: there is nothing to save
        lines.append("marked copy: none needed (nothing changed since the clean Word placed at the top)")
    else:
        lines.append(f"marked copy: track/{track.name}" + (" (dry run: not written)" if dry else ""))
    found = changes(docx, base)
    lines.append(("since: the clean Word placed at the top" if base.name.startswith(".") else
                  f"since: {base.parent.name}/{base.name}") if base else "since: nothing (no track/, clean/ or previous/ copy)")
    lines += ["", f"each change goes to {SOURCES.get(kind, 'the source of ' + kind)} (a revise card each):"
              if found else "no changes since then", ""]
    for k, a, w in found:
        ask = "  🙋 a question: ask the person" if k == "comment" and w.rstrip().endswith("?") else ""
        ask = ask or ("  🙋 untracked: say who made it" if k == "untracked" else "")
        lines.append(f"- {k} [{a}] {w[:240]}{ask}")
    if rebuild:
        lines.append(f"\nrebuild: {rebuild}" + (" (dry run: not run)" if dry else ""))
        if not dry:
            r = subprocess.run(rebuild, shell=True)
            if r.returncode:
                raise SystemExit(f"rebuild failed ({r.returncode}); the working file is unchanged")
    placed = place_clean(round_dir, docx, clean, version, dry)
    if draft and placed.is_file():
        same = accepted_text(draft) == accepted_text(placed)
        lines.append(f"check: the draft's Word and clean/ {'hold the same words ✅' if same else 'differ ❗'}")
    lines.append("")
    if dry or how is None:
        lines.append(QUESTION.format(name=docx.name) if not dry else "working file: unchanged (dry run)")
        return lines
    if how == "keep":
        lines.append(f"working file: kept as it is, marks and comments included; the next settle starts from track/{track.name}")
        return lines
    if not track.is_file():
        raise SystemExit("no marked copy in track/: the working file is not changed")
    if how == "each":
        from word_marks import listing, accept
        if not pick:
            lines.append("each mark and comment (run again with --pick 1,3-5 to accept those; the rest are kept):")
            lines += [f"  {m[0]:>3}. {m[1]} [{m[2]}] {m[3][:200]}" for m in listing(docx)]
            return lines
        n = accept(docx, pick)
        lines.append(f"working file: {n} marks accepted, the others kept; Track Changes still on")
        return lines
    # accept: the clean Word replaces it, but only when every word a mark added is already in the drafts
    if not placed.is_file():
        raise SystemExit(f"--working accept needs clean/{placed.name}: rebuild and pass --clean first")
    clean_text = " ".join(accepted_text(placed))
    lost = [w for k, a, w in marks(docx)["changes"] if k == "ins" and " ".join(w.split()) not in clean_text]
    if lost:
        lines.append("refused: these marked words are not in the drafts yet, so accepting would lose them:")
        lines += [f"  - {w[:200]}" for w in lost]
        lines.append("sync them into the source and rebuild, or use --working each")
        return lines
    top = replace_top(round_dir, docx, placed)
    same = accepted_text(top) == accepted_text(placed)
    lines.append(f"working file: {top.name} is the clean Word now, Track Changes on; "
                 f"top and clean/ {'hold the same words ✅' if same else 'differ ❗'}")
    return lines


def replace_top(round_dir, docx, placed):
    """The clean Word becomes working file n, Track Changes on; track/.placed-<n>.docx keeps it as settle's
    baseline, so the next settle lists only what was changed after it."""
    top = Path(round_dir) / top_name(placed)
    shutil.copy2(placed, top)
    track_on(top)
    if top != docx:
        docx.unlink()
    base = Path(round_dir) / "track" / PLACED.format(n=parse(top)[0])
    base.parent.mkdir(exist_ok=True)
    shutil.copyfile(top, base)          # copyfile: its time is now, the time of the placing
    return top


def refresh_one(round_dir, docx, *, clean=None, version=None, dry=False):
    """A working file nobody changed since its last synced point becomes the clean build: the old one is saved to
    track/, clean/ is placed, the clean Word replaces it with Track Changes on, and every marker is the tool's
    (Pp-AgreeableRx 261122: the portal file still held old values after a portal rebuild)."""
    num, name, old, kind = parse(docx)
    why = in_use(docx)
    if why:
        raise SystemExit(f"{docx.name}: {why}; close it in Word first (AutoSave writes over any outside change)")
    lines = [f"## {docx.name}", ""]
    base = last_seen(round_dir, num)
    placed = place_clean(round_dir, docx, clean, version, dry)
    if not dry and not placed.is_file():
        raise SystemExit(f"refresh needs clean/{placed.name}: pass --clean {num}=<docx>[,<pdf>]")
    m = marks(docx)
    if not dry and not (m["changes"] or m["comments"]) and accepted_text(placed) == accepted_text(docx) \
            and top_name(placed) == docx.name:   # a clean Word placed by hand: record it, so settle starts from it
        base = Path(round_dir) / "track" / PLACED.format(n=num)
        base.parent.mkdir(exist_ok=True)
        shutil.copyfile(docx, base)
        return lines + ["working file: already holds the clean build's words; unchanged, and settle starts from it now"]
    if changes(docx, base) or m["changes"] or m["comments"]:
        since = ("the clean Word placed at the top" if base.name.startswith(".") else f"{base.parent.name}/{base.name}") \
            if base else "the round's start"
        lines.append(f"refused: it has marks, comments or edits since {since}; settle {num} deals with those first")
        return lines
    track = Path(round_dir) / "track" / f"{num}-{name}-v{old}-{kind}-tracked-{now():{STAMP}}.docx"
    guard(track, round_dir)
    if dry:
        return lines + [f"would save track/{track.name}, place clean/{placed.name}, and make it the working file"
                        " (dry run: nothing written)"]
    track.parent.mkdir(exist_ok=True)
    shutil.copy2(docx, track)
    top = replace_top(round_dir, docx, placed)
    marker(track.parent, "Before anyone accepts changes or closes comments in a working file, a marked copy of "
                         "it is saved here first.")
    same = accepted_text(top) == accepted_text(placed)
    return lines + [f"old copy: track/{track.name}",
                    f"working file: {top.name} is the clean build now, Track Changes on; "
                    f"top and clean/ {'hold the same words ✅' if same else 'differ ❗'}"]


# ── submit ───────────────────────────────────────────────────────────────────────────────────────────────────────
def place_clean(round_dir, docx, clean, version=None, dry=False):
    """clean/<n>-<Name>-v<MMDD>-<kind>-clean.docx (and .pdf) from the rebuild, written only when it changed; the marker
    is rewritten when anything was. Returns the clean Word's path."""
    num, name, old, kind = parse(docx)
    cdir = Path(round_dir) / "clean"
    stem = f"{num}-{name}-v{version or old}-{kind}"
    wrote = False
    for src in (clean or []) if not dry else []:
        dst = cdir / f"{stem}{CLEAN}{Path(src).suffix}"
        if dst.is_file() and dst.read_bytes() == Path(src).read_bytes():
            continue
        cdir.mkdir(exist_ok=True)
        for stale in cdir.glob(f"{num}-*{Path(src).suffix}"):
            stale.unlink()
        shutil.copy2(src, dst)
        wrote = True
    if wrote:
        marker(cdir, "The LaTeX PDF and the LaTeX-made Word of each file, no marks; rebuilt when the top changes.")
    return cdir / f"{stem}{CLEAN}.docx"


def slug(slot):
    words = re.sub(r"\([^)]*\)", "", slot).strip().lower()
    words = re.sub(r"\b(commitment|form|file)\b", "", words)
    return re.sub(r"[^a-z0-9]+", "-", words).strip("-")


def is_frozen(round_dir):
    sub = Path(round_dir) / "submission"
    return any(FROZEN in m.read_text(encoding="utf-8") for m in sub.glob("last-update-*.txt"))


def submit(round_dir, config, mmdd):
    """submission/: the portal uploads, numbered by their slot in paper-build.toml [portal]. Until the person presses
    Submit it always equals the newest build (every settle refreshes it); `submitted` freezes it (JL 261122: "for the
    clean and submission, they must be updated")."""
    sub = Path(round_dir) / "submission"
    if is_frozen(round_dir):
        raise SystemExit(f"{sub.name}/ is frozen: it was submitted; a resubmission is a new round")
    cfg = tomllib.loads(Path(config).read_text(encoding="utf-8"))
    uploads = cfg.get("portal", {}).get("upload", [])
    if not uploads:
        raise SystemExit(f"no [[portal.upload]] in {config}")
    names = {parse(p)[1] for p in working(round_dir).values()}
    name = names.pop() if len(names) == 1 else str(cfg.get("paper", {}).get("id", "paper"))
    base = Path(config).parent
    found = [(u, portal_files(base, u)) for u in uploads]
    missing = [u["from"] for u, fs in found if not fs]
    if missing:
        raise SystemExit("not built: " + ", ".join(missing))
    sub.mkdir(exist_ok=True)
    for i, (u, fs) in enumerate(found, 1):
        stem = f"{i}-{name}-v{mmdd}-{u.get('kind') or slug(u['slot'])}"
        dsts = [sub / (f"{stem}{src.suffix}" if len(fs) == 1 else f"{stem}-{k}{src.suffix}")
                for k, src in enumerate(fs, 1)]
        for stale in sub.glob(f"{i}-*"):
            if stale not in dsts:
                stale.unlink()
        for src, dst in zip(fs, dsts):
            shutil.copy2(src, dst)
            print(f"{dst.name}  ({u['slot']})")
    marker(sub, "The portal uploads, numbered by slot; the newest build until Submit is pressed, then frozen.")
    return sub


def portal_files(base, upload) -> list[Path]:
    """A [[portal.upload]]'s files, read as build.py portal reads them (Paper-FairGlucose-preprint 261123: a dated zip
    named by a glob): `from` may be a glob, the newest match by time wins, every match with `all = true`."""
    import glob
    src = str(upload.get("from", ""))
    hits = sorted((Path(h) for h in glob.glob(str(Path(base) / src)) if Path(h).is_file()) if src else [],
                  key=lambda h: h.stat().st_mtime)
    return hits if upload.get("all") else hits[-1:]


def submitted(round_dir):
    """The person pressed Submit: submission/ is frozen, nothing writes it again."""
    sub = Path(round_dir) / "submission"
    if not sub.is_dir() or is_frozen(round_dir):
        raise SystemExit(f"{sub.name}/ is {'frozen already' if sub.is_dir() else 'missing: run submit first'}")
    marker(sub, f"{FROZEN} {now():%Y-%m-%d %H:%M}; nothing here is written again (a resubmission is a new round).")
    return sub


def status(round_dir):
    r = Path(round_dir)
    for p in sorted(r.iterdir()):
        if p.is_file() and not p.name.startswith("."):
            mark = "❗ a PDF at the top" if p.suffix == ".pdf" else ("Track Changes on" if p.suffix == ".docx" and tracking(p) else "Track Changes OFF ❗")
            busy = in_use(p) if p.suffix == ".docx" else ""
            print(f"{p.name}  {mark}{'  🔒 ' + busy if busy else ''}")
    if not any((r / sub).is_dir() for sub in ("previous", "track", "clean", "submission")):
        print("❗ old layout: no previous/ track/ clean/ submission/; start the round with open-round (ref/round-folder.md)")
    for sub in ("previous", "track", "clean", "submission"):
        d = r / sub
        if d.is_dir():
            m = sorted(d.glob("last-update-*.txt"))
            frozen = " 🔒 frozen" if m and FROZEN in m[-1].read_text(encoding="utf-8") else ""
            print(f"{sub}/  {len([f for f in d.iterdir() if f.is_file() and not f.name.startswith(('.', 'last-update-'))])} files"
                  f"  {m[-1].name if m else 'no marker ❗'}{frozen}")


def word_marks_picks(text):
    if not text:
        return None
    from word_marks import picks
    return picks(text)


def _pairs(values, many=False):
    out = {}
    for v in values or []:
        n, _, path = v.partition("=")
        out[int(n)] = [Path(x).resolve() for x in path.split(",")] if many else Path(path).resolve()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sp = ap.add_subparsers(dest="verb", required=True)
    p = sp.add_parser("open-round"); p.add_argument("parent", type=Path); p.add_argument("--date", default=f"{now():%m%d}")
    p.add_argument("--file", action="append", help="N=<built.docx>: file N starts from this build, not the last round's")
    p = sp.add_parser("settle"); p.add_argument("round", type=Path); p.add_argument("which")
    p.add_argument("--clean", action="append", help="N=<docx>[,<pdf>]: the rebuilt clean Word (and PDF) of file N")
    p.add_argument("--draft", action="append", help="N=<docx>: the build's own Word, checked word for word")
    p.add_argument("--rebuild", help="the paper's build command, run before the clean files are placed")
    p.add_argument("--version", help="MMDD of the clean files (default: the working file's own)")
    p.add_argument("--report", type=Path, help="also write the list of changes here")
    p.add_argument("--working", choices=["keep", "accept", "each"], help="how to deal with the working file; "
                   "with none, settle asks and stops")
    p.add_argument("--pick", help="with --working each: the marks to accept, e.g. 1,3-5")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--config", type=Path, help="paper-build.toml: after the rebuild, submission/ is refreshed too")
    p = sp.add_parser("adopt-round"); p.add_argument("flat", type=Path)
    p.add_argument("--name", required=True); p.add_argument("--date", required=True, help="MMDD of the round")
    p.add_argument("--round", type=int, help="its number (default: the one it has, else 1)")
    p.add_argument("--into", type=Path, help="make RoundN-vMMDD inside this paper folder (default: rename <flat>)")
    p.add_argument("--file", action="append", required=True, help="N=<file in it>:<kind>, e.g. 1=Paper-X.docx:manuscript")
    p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("refresh"); p.add_argument("round", type=Path); p.add_argument("which")
    p.add_argument("--clean", action="append", help="N=<docx>[,<pdf>]: the rebuilt clean Word (and PDF) of file N")
    p.add_argument("--version", help="MMDD of the clean files (default: the working file's own)")
    p.add_argument("--config", type=Path, help="paper-build.toml: submission/ is refreshed too")
    p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("take-clean"); p.add_argument("round", type=Path); p.add_argument("which", type=int)
    p.add_argument("--clean", action="append", help="N=<docx>[,<pdf>]: the build that refills clean/")
    p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("clean-names"); p.add_argument("round", type=Path); p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("submitted"); p.add_argument("round", type=Path)
    p = sp.add_parser("submit"); p.add_argument("round", type=Path); p.add_argument("--config", required=True, type=Path)
    p.add_argument("--date", default=f"{now():%m%d}")
    p = sp.add_parser("status", aliases=["round-status"]); p.add_argument("round", type=Path)
    a = ap.parse_args(argv)
    if a.verb == "open-round":
        made = open_round(a.parent, a.date, _pairs(a.file))
        status(made)
        _check(made)
    elif a.verb == "settle":
        files = working(a.round)
        pick = sorted(files) if a.which == "all" else [int(a.which)]
        clean, draft, out = _pairs(a.clean, many=True), _pairs(a.draft), []
        for n in pick:
            if n not in files:
                raise SystemExit(f"no working file {n} at the top of {a.round.name}")
            out += settle_one(a.round, files[n], clean=clean.get(n), draft=draft.get(n), version=a.version,
                              dry=a.dry_run, rebuild=a.rebuild if n == pick[0] else None, how=a.working,
                              pick=word_marks_picks(a.pick)) + [""]
        # after a rebuild, clean/ holds every file whose build changed, not only the settled one (JL 261122)
        for n in sorted(set(clean) - set(pick)):
            if n in files:
                place_clean(a.round, files[n], clean[n], a.version, a.dry_run)
                out.append(f"clean/: file {n} refreshed from the rebuild")
        if a.config and not a.dry_run and not is_frozen(a.round):
            submit(a.round, a.config, a.version or f"{now():%m%d}")
            out.append("submission/: refreshed from the newest build (frozen only by `submitted`)")
        print("\n".join(out))
        if a.report:
            a.report.write_text("\n".join(out) + "\n", encoding="utf-8")
    elif a.verb == "adopt-round":
        from round_adopt import adopt_round
        files = {int(k): tuple(v.rsplit(":", 1)) for k, v in (x.split("=", 1) for x in a.file)}
        made, lines = adopt_round(a.flat, a.name, a.date, files, a.round, a.dry_run, a.into)
        print("\n".join(lines))
        if not a.dry_run:
            _check(made)
    elif a.verb == "refresh":
        files, clean, out = working(a.round), _pairs(a.clean, many=True), []
        pick = sorted(set(clean) & set(files)) if a.which == "all" else [int(a.which)]
        for n in pick:
            if n not in files:
                raise SystemExit(f"no working file {n} at the top of {a.round.name}")
            out += refresh_one(a.round, files[n], clean=clean.get(n), version=a.version, dry=a.dry_run) + [""]
        if a.config and not a.dry_run and not is_frozen(a.round):
            submit(a.round, a.config, a.version or f"{now():%m%d}")
            out.append("submission/: refreshed from the newest build (frozen only by `submitted`)")
        print("\n".join(out))
    elif a.verb == "take-clean":
        from round_clean import take_clean
        print("\n".join(take_clean(a.round, a.which, _pairs(a.clean, many=True).get(a.which), a.dry_run)))
    elif a.verb == "clean-names":
        from round_clean import clean_names
        print("\n".join(clean_names(a.round, a.dry_run)))
    elif a.verb == "submit":
        submit(a.round, a.config, a.date)
        status(a.round)
    elif a.verb == "submitted":
        submitted(a.round)
        status(a.round)
    else:
        status(a.round)
    if a.verb in ("settle", "refresh", "take-clean", "clean-names", "submit", "submitted") and not getattr(a, "dry_run", False):
        _check(a.round)


def _check(round_dir):
    """Every verb ends with the layout check (check_round.py), so a round that drifted says so at once."""
    from check_round import report
    print()
    report(Path(round_dir).resolve())


if __name__ == "__main__":
    main()
