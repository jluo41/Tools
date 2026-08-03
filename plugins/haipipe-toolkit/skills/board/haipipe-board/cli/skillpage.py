#!/usr/bin/env python3
"""One skill folder -> one Q page on a board (QC5, opened by JL 260726).

    python3 skillpage.py new  <board> <skill-dir> --group QC   # -> Skill-<n>-<slug>.md
    python3 skillpage.py sync <board> <page-id>          # refresh the managed block
    python3 skillpage.py sync <board> --all
    python3 skillpage.py check <board>                   # report staleness, never write

WHAT THIS IS A SECOND COPY OF. `stage.py`, deliberately. It already solves
"generate a page from a source that lives somewhere else, then keep it in sync
without ever touching what a human typed", and it has held since 260725. A
second mechanism for the same problem is how the two drift.

THE SPLIT, which is the whole ruling (QC5 §1-§2):

    DERIVED, and this script owns it     name · version · last_updated ·
    (inside the managed markers)         summary · allowed-tools · path ·
                                         the two ![[embeds]]

    AUTHORED, and this script never      ## Opening · ## Aims ·
    touches it                           ## States · ## Log

`state:` is NOT derived (QC5 §3). A version cannot say whether a skill is
stable, in flux, or abandoned: 0.1.0 may be finished and 0.9.4 may be mid
rewrite. `new` seeds 🔴 OPEN like every other page and a person rules on it.
The version rides after the emoji as readable detail, which the renderer and
checker already allow.

ZERO COPY. The page embeds `SKILL.md` and `CHANGELOG.md` with `![[...]]`, read
at BUILD time, so the page cannot go stale between two syncs. Only the derived
header can, which is what `check` is for (QC5 §4).
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))

# page_files, not the Q-only glob (JL 260731): a skill page is now
# `Skill-<unit>-<slug>.md`, which starts with S. page_files carries both eras,
# so older boards with Q-Skill-* pages keep syncing.
from src.common import page_files  # noqa: E402

# Three managed spans, because the derived material belongs in three different
# sections and one block cannot straddle them (JL 260726: the tree goes in
# Diagram, the skill's content in Content, the changelog in Log).
PARTS = ("tree", "body", "log")


def start_of(part):
    return f"<!-- haipipe:skill:{part}:start"


def end_of(part):
    return f"<!-- haipipe:skill:{part}:end -->"


START = start_of("body")
END = end_of("body")
# The marker only counts at the start of a line. QC5, the page that RULES this
# mechanism, quotes the marker inside its own prose; a plain substring test read
# that as a managed block and reported the ruling page as a broken skill page.
# The marker carries the hash AND the skill folder. `sync` used to recover the
# folder from the page's `![[…/SKILL.md]]` line, which vanished the moment the
# skill file became real subsections instead of an embed. A machine span should
# not depend on rendered content to know its own source.
MARKER = re.compile(r"^" + re.escape(START) + r"\s+([0-9a-f]{16})(?:\s+(\S+))?", re.M)
SKIP = {"__pycache__", ".git", "node_modules"}
DOC = {".md", ".txt"}


def _span_at_line_start(text, marker):
    """Index of `marker` where it BEGINS A LINE, or -1.

    A skill's own SKILL.md may quote these markers, in prose or inside a figure
    that draws the page anatomy. Such a quote is indented or mid-line, and only
    a line-anchored search can tell it from the real span.
    """
    at = 0
    while True:
        i = text.find(marker, at)
        if i < 0:
            return -1
        if i == 0 or text[i - 1] == "\n":
            return i
        at = i + 1


def has_block(page):
    return bool(MARKER.search(page.read_text(encoding="utf-8")))


def unit(target):
    """-> (definition_md, changelog_md|None, folder_for_the_tree|None).

    A page's subject is one SHIPPED UNIT, and this family ships two kinds
    (JL 260727: "and also the agent as well"): a skill, which is a folder whose
    definition is `SKILL.md`, and an agent, which is ONE `.md` file whose
    changelog belongs to its `agents/` folder and is shared with its siblings.

    The frontmatter is identical in both (`name`, `metadata.version`,
    `last_updated`, `summary`), which is why one generator covers both instead
    of a second script that would drift. Only the tree differs: a folder has one
    to draw and a single file does not.
    """
    target = Path(target).resolve()
    if target.is_dir():
        return target / "SKILL.md", target / "CHANGELOG.md", target
    return target, target.parent / "CHANGELOG.md", None


def frontmatter(skill_md):
    """-> {key: value} from the SKILL.md front matter, metadata flattened.

    A hand parser rather than PyYAML because build.py is standard-library only
    and this file must run under the same interpreter (`python3`, 3.9 is fine).
    Only scalar keys are read; the values here are all scalars.
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    block = text[3:end if end > 0 else len(text)]
    out, indent = {}, False
    for ln in block.split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)([A-Za-z][\w-]*):\s*(.*)$", ln)
        if not m:
            continue
        pad, key, val = m.group(1), m.group(2), m.group(3).strip()
        if key == "metadata" and not val:
            indent = True
            continue
        if pad and not indent:
            continue
        val = val.strip('"').strip("'")
        if val in (">-", "|", ">"):
            val = ""
        out[key] = val
    return out


def digest(target):
    """Hash the DERIVED facts only, so prose edits never look like drift."""
    h = hashlib.sha256()
    fm = frontmatter(unit(target)[0])
    for k in ("name", "version", "last_updated", "summary", "allowed-tools"):
        h.update(f"{k}={fm.get(k, '')}\0".encode("utf-8"))
    return h.hexdigest()[:16]


def rel(board, target):
    """The token `![[...]]` will actually resolve, by the embed's own ladder.

    `page_stage._find` REFUSES `..` and absolute paths on purpose, and instead
    tries the token against the board folder and then each ancestor, stopping
    at a `.git` or `pyproject.toml`. So a skill outside the board is named by
    the path an ancestor sees, `board/haipipe-board/SKILL.md`, not by a `../`
    walk. Emitting `../../board/...` produced two visible `⚠ embed not found`
    blocks on the first generated page, which is the embed contract working:
    it never fails silently, so the wrong token was on screen in one build.
    """
    board, target = board.resolve(), target.resolve()
    here = board
    for _ in range(8):
        try:
            token = target.relative_to(here).as_posix()
        except ValueError:
            token = ""
        if token and (here / token).is_file() or (token and (here / token).is_dir()):
            # only report it if the ladder would find THIS file first
            probe, walk = board, None
            for _ in range(8):
                if (probe / token).exists():
                    walk = probe
                    break
                if (probe / ".git").exists() or (probe / "pyproject.toml").exists():
                    break
                if probe.parent == probe:
                    break
                probe = probe.parent
            if walk is not None and (walk / token).resolve() == target:
                return token
        if (here / ".git").exists() or (here / "pyproject.toml").exists():
            break
        if here.parent == here:
            break
        here = here.parent
    return target.as_posix()


def purpose(path):
    """One line saying what a file is for, taken FROM THE FILE.

    A module docstring's first line, a markdown H1, or the first `/* … */` or
    `#` comment. Derived, never invented: a manifest that guesses is worse than
    one that says nothing, because a wrong purpose is read as a true one.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return ""
    if path.suffix == ".py":
        m = re.search(r'^\s*(?:#!.*\n)?(?:"""|\'\'\')(.+?)$', text, re.M)
        if m:
            return m.group(1).strip().rstrip('"\'')
    if path.suffix in DOC:
        if text.startswith("---"):          # skip YAML front matter, or every
            cut = text.find("\n---", 3)     # SKILL.md reports "name: <itself>"
            text = text[cut + 4:] if cut > 0 else text
        for ln in text.split("\n"):
            if ln.startswith("# "):
                return ln[2:].strip()
            if ln.strip() and not ln.startswith(("---", "=")):
                return ln.strip()[:110]
    if path.suffix in (".js", ".css"):
        m = re.search(r"/\*+\s*(?:[─\s]*)?(.+?)$", text, re.M)
        if m:
            return m.group(1).strip().rstrip("*/ ").strip("─ ")
    return ""


def walk(skill_dir):
    """-> [(depth, name, path|None)] for the whole folder, dirs before files."""
    rows = []

    def rec(d, depth):
        kids = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for k in kids:
            if k.name in SKIP or k.name.startswith("."):
                continue
            if k.is_dir():
                rows.append((depth, k.name + "/", None))
                rec(k, depth + 1)
            else:
                rows.append((depth, k.name, k))

    rec(skill_dir, 0)
    return rows


def tree_block(board, skill_dir):
    """The folder, drawn, with each file's own one-line purpose beside it.

    A single-file unit has no tree, so the span is emitted empty rather than
    skipped: `sync` replaces spans it can find, and a missing one would report
    as an older page needing repair every time.
    """
    if not Path(skill_dir).is_dir():
        return "\n".join([f"{start_of('tree')} {digest(skill_dir)} "
                           f"{rel(board, Path(skill_dir))} -->", "", end_of("tree")])
    rows = walk(skill_dir)
    width = max((len("  " * d + n) for d, n, _ in rows), default=0)
    width = min(max(width, 18), 34)
    out = [f"{skill_dir.name}/"]
    for depth, name, path in rows:
        lines = ""
        why = ""
        if path is not None:
            n = sum(1 for _ in path.open("rb"))
            lines = f"{n:>5} ln"
            why = purpose(path)
        label = "  " * (depth + 1) + name
        out.append(f"{label:<{width + 2}} {lines:>8}  {why}".rstrip())
    body = "\n".join(out)
    # QB4 §2: EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT. The caption lives
    # INSIDE the managed span on purpose. A caption a person writes inside the
    # span is erased by the next `sync`, and one written just outside it survives
    # but is generated by nothing, so every new page starts non-compliant and the
    # rule is enforced only by whoever remembers. A derived figure owes a derived
    # caption. (JL 260802, reading Skill-0: "for the diagram, it doesn't follow
    # the Rule in QB4".)
    return "\n".join([
        f"{start_of('tree')} {digest(skill_dir)} {rel(board, skill_dir)} -->",
        "",
        f"**What `{skill_dir.name}` ships**: every file in the folder, "
        f"with the one-line purpose each one states for itself.",
        "",
        "```",
        body,
        "```",
        "",
        end_of("tree"),
    ])


CL_HEAD = re.compile(
    r"^##\s*\[?v?([0-9][0-9.]*)\]?\s*[—\-–·]*\s*(\d{4})-(\d{2})-(\d{2})"
    r"\s*[—\-–·]*\s*(.*)$")


def join_wrapped(lines):
    """Re-join a `**bold**` that the source wrapped across two lines.

    The board gives every prose line its own row, so a row ending mid-marker
    renders a literal `**` and the next row opens one that never closes. That is
    not a bug in the source: `SKILL.md` is written one sentence per line and a
    long bold phrase legitimately spans two of them. It only becomes visible once
    the file is rendered as board content.

    Joining is the honest repair, because the two halves ARE one sentence. The
    alternative, editing `SKILL.md` to satisfy the renderer, would let a display
    concern dictate how a shipped skill is written.
    """
    out, fence = [], False
    for ln in lines:
        if ln.lstrip().startswith("```"):
            fence = not fence
            out.append(ln)
            continue
        if (not fence and out and not out[-1].lstrip().startswith("```")
                and out[-1].count("**") % 2 and ln.strip()):
            out[-1] = out[-1].rstrip() + " " + ln.strip()
            continue
        out.append(ln)
    return out


def skill_sections(skill_dir):
    """SKILL.md -> ONE `### SKILL.md` division whose insides are its sections.

    JL 260727: the file is a subsection of Content and the file's own sections
    are sub-sub sections. So there is one wrapper division, and every heading in
    the skill moves two levels down inside it.

    The board renders exactly two Content levels: `###` folds, `####` does not,
    and `#{4,6}` all render identically. Depth therefore has to be carried by
    NUMBERING, which is the rule QA4 already fixed for manuscript sections (`§6`
    against `§6.1`) and the reason a third heading level was refused there. So
    the skill's `##` becomes `#### N ·` and its `###` becomes `##### N.M ·`:
    same size on the page, unambiguous hierarchy in the text.

    Fences pass through byte for byte. `SKILL.md` holds a page-anatomy figure
    whose lines start with `## `, and treating those as headings would rewrite
    14 lines of a diagram.
    """
    text = unit(skill_dir)[0].read_text(encoding="utf-8")
    if text.startswith("---"):
        cut = text.find("\n---", 3)
        text = text[cut + 4:] if cut > 0 else text
    text = "\n".join(join_wrapped(text.split("\n")))
    # EVERY numbered section is an ITEM, at one level, with the number carrying
    # the depth (JL 260727: "2 · 🧭 Session attachment ... I still collapse this").
    #
    # Why not two nested levels: the board has exactly one folding level inside
    # Content. `###` is a division and `####`/`#####` are `.ph` paragraph
    # headings, which never fold, and items do not nest either (an indented `- `
    # inside an item body is absorbed as that item's text). So a `##` rendered as
    # a heading could not be collapsed at all, which is the bug being fixed here.
    #
    # The item form IS the fold, so both levels use it and `1 ·`, `2 ·`, `3 ·`,
    # `3.1 ·` … carry the hierarchy. That is not a workaround: QA4 already ruled
    # that depth is read off the numbering rather than the heading level, and
    # refused a third heading level for this exact reason.
    out = [f"### {unit(skill_dir)[0].name}", ""]
    fence, n, m, deep = False, 0, 0, False

    def emit(ln):
        # Inside an item, every line becomes its indented body, and a fence keeps
        # its own relative indent so an ascii figure survives the dedent.
        #
        # NO BLANK LINE MAY APPEAR IN AN ITEM BODY, anywhere. `body.py` calls
        # `flush()` on a blank line, which CLOSES the item, so the first blank
        # line ended the fold and dumped the rest of the section into the page as
        # literal `- ` and `**bold**` text. A first fix guarded only the line
        # right after the item head, which is why `1 · 🗂 形状` folded down to
        # its opening figure and nothing else.
        #
        # Dropping them costs nothing: the item body is a list of rows and each
        # row already renders as its own line. Blank lines INSIDE a fence are
        # kept, because there they are content.
        if deep and not fence and not ln.strip():
            return
        out.append(("      " + ln) if (deep and ln.strip()) else ln)

    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            emit(ln)
            continue
        if fence:
            emit(ln)
            continue
        if ln.startswith("## "):
            n, m, deep = n + 1, 0, True
            out += ["", f"- {n} · {ln[3:].strip()}"]
        elif ln.startswith("### "):
            m, deep = m + 1, True
            out += ["", f"- {n}.{m} · {ln[4:].strip()}"]
        elif ln.startswith("#### "):
            emit(f"**{ln[5:].strip()}**")
        elif ln.startswith("# "):
            continue                       # the page title already says this
        else:
            emit(ln)
    return out


def log_block(board, skill_dir):
    """The CHANGELOG CONVERTED into `## Log` lines, not embedded as a file.

    JL 260727: "copy and convert the content of Changelog to the LOG as well."
    Convert, not embed, and the difference is the whole point. `## Log` has a
    grammar the board reads: `YYMMDD · what changed`, newest first, with
    indented continuation lines carried along by `sort_log`. A CHANGELOG entry
    is the same fact in a different notation, so translating it makes the
    skill's history first-class board content instead of a foreign document
    parked inside a page.

    What that buys, and it is not cosmetic: the ACTIVITY dashboard counts one
    update per dated `## Log` line, so a converted changelog puts every release
    this skill ever shipped onto the strip and into the Board -> Group -> Page
    ranking. An embedded file counts as zero.
    """
    src = unit(skill_dir)[1]
    if not src or not src.is_file():
        return ""
    lines = src.read_text(encoding="utf-8").split("\n")
    out, body, head = [], [], None

    def flush():
        if head is None:
            return
        ver, day, title = head
        out.append(f"{day} · `{ver}` · {title}".rstrip(" ·"))
        for b in body:
            out.append("      " + b)

    for ln in lines:
        m = CL_HEAD.match(ln.strip())
        if m:
            flush()
            ver, yyyy, mm, dd, title = m.groups()
            head, body = (ver, f"{yyyy[2:]}{mm}{dd}", title.strip(" —-–·")), []
        elif head is not None and ln.strip():
            if ln.startswith("## "):          # a dateless heading ends the entry
                flush()
                head, body = None, []
            else:
                body.append(ln.rstrip())
    flush()
    return "\n".join([
        f"{start_of('log')} {digest(skill_dir)} {rel(board, skill_dir)} -->",
        "",
        f"Converted from the skill's own `CHANGELOG.md`: {len(out) and sum(1 for x in out if not x.startswith('      '))} releases.",
        "",
    ] + out + ["", end_of("log")])


def block(board, skill_dir):
    skill_dir = Path(skill_dir)
    defn, _clog, folder = unit(skill_dir)
    fm = frontmatter(defn)
    base = rel(board, skill_dir)
    rows = [
        f"{START} {digest(skill_dir)} {base} -->",
        "",
        f"**{fm.get('name', skill_dir.name)}** · `{fm.get('version', '?')}`"
        f" · last shipped {fm.get('last_updated', '?')}",
        "",
        f"- folder   `{base}/`",
        f"- tools    {fm.get('allowed-tools', 'not declared')}",
    ]
    if fm.get("summary"):
        rows.append(f"- summary  {fm['summary']}")
    # NOTE: `|source` mode, not rendered (found the hard way on the FIRST page).
    # Embedding `haipipe-board`'s own SKILL.md rendered its documentation of
    # board syntax AS board syntax: `[写法](路径)`, written there to show what a
    # link looks like, became a real link and a permanent `dead-href` ERROR.
    # A skill file is instructions to an agent, so its BYTES are the artifact;
    # showing them raw is both more honest and immune to a page executing its
    # own examples. `board-form.md` §5 offers `|source` for exactly this.
    # The skill file becomes REAL BOARD SUBSECTIONS of `## Content` (JL 260727:
    # "I want to get the follow content of SKILL.md and presented in the Content
    # as the subsections in the Content section").
    #
    # An embed was one opaque block: one fold, one `⧉`, no per-section anchor,
    # and nothing a comment could be pinned to. Converted, every `## ` of the
    # skill is a division the reader can fold, copy, link to, and comment on,
    # and the Content heading counts them, so the page reports "📚 Content · 9
    # sections" the way every hand-written page does.
    #
    # This is a COPY, which the board normally refuses. It is safe here for the
    # same reason `stage.py`'s contract block is: it lives inside a managed span
    # whose hash `check` verifies, so drift is reported rather than possible.
    rows += [""] + skill_sections(skill_dir)

    # ── every OTHER file in the skill: DESCRIBED, not embedded ──────────
    # JL 260726: "we might only want to put the SKILL.md content to the Q page,
    # and for other we just make our descriptions."
    #
    # SKILL.md is the skill's content and is shown whole. Everything else is
    # named, sized, and given the purpose line the FILE ITSELF states, which is
    # a description rather than a copy. A page that reproduced every file would
    # be a slow mirror of a folder that already exists, and the reader would
    # scroll past the skill instead of reading it.
    others = [] if folder is None else [
        p for p in sorted(folder.rglob("*"))
        if p.is_file() and p.name not in ("SKILL.md", "CHANGELOG.md")
        and not any(x in SKIP or x.startswith(".")
                    for x in p.relative_to(folder).parts)]
    if not others:
        rows.append(END)
        return "\n".join(rows)
    rows += ["### The other files", "",
             f"{len(others)} files besides `SKILL.md` and `CHANGELOG.md`,"
             " each with the purpose it states about itself. They are"
             " described here, not reproduced: the folder is the copy.", ""]
    # A FENCE, not a bullet list. These purpose lines are verbatim quotes from
    # other files, so they carry those files' punctuation; as prose the checker
    # would rightly flag em-dashes JL banned, and "fixing" a quote falsifies it.
    width = min(max((len(f.relative_to(folder).as_posix()) for f in others),
                    default=18), 30)
    rows += ["```"]
    for f in others:
        r = f.relative_to(folder).as_posix()
        n = sum(1 for _ in f.open("rb"))
        rows.append(f"{r:<{width + 2}} {n:>5} ln  {purpose(f)}".rstrip())
    rows += ["```", ""]
    rows.append(END)
    return "\n".join(rows)


STUB = """# {name} · v{version}
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
REPLACE THIS PARAGRAPH. Load `haipipe-board-page-for-skill` and write the three slots it names, in its order, in plain words: ❶ what `{name}` is and what it is FOR, ❷ when you reach for it rather than the ONE sibling you would otherwise pick, named, ❸ where it stands, meaning the one thing to know before trusting it.

NEVER open a skill page with a question. This stub used to seed `{{name}} is a shipped unit: what does it still owe, and is it healthy?`, and on 260802 five pages generated from it all opened with the same rhetorical question in the same four-slot shape, because a skill page DECIDES NOTHING and so has nothing to ask.
Delete these instructions once the paragraph is written; the FIRST BLANK LINE above is the split, and everything below it is the `More details` drawer, written as labelled parts.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
{tree}

**How `{name}` is used**: REPLACE THIS CAPTION with what your figure below actually shows.

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence AND the
caption line above it if the tree is the whole story.
```

## Content
{block}

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated {stamp}; nothing ruled yet.

## Log
{stamp} · page generated from `{base}/` by `skillpage.py new`

{log}
"""


def find_page(board, page_id):
    for p in page_files(board):
        stem = p.name[:-3]
        if re.match(r"^Q-[A-Z]", stem):
            pid = stem                        # a named family: the whole stem
        elif (m := re.match(r"^((?:Skill|Agent)-\d+)-", stem)):
            pid = m.group(1)                  # the skill/agent kind: `<Kind>-<unit>`
        else:
            pid = stem.split("-", 1)[0]
        if pid.casefold() == page_id.casefold():
            return p
    return None


def resolve_token(board, token):
    """The embed's ladder, walked the same way `page_stage._find` walks it.

    `sync` has to find the skill from the page's own embed line, so it must
    resolve that token exactly as the renderer will. Resolving it any other way
    means a page can render one file while sync reads another, which is a
    disagreement no test would catch because both halves work alone.
    """
    here = board.resolve()
    for _ in range(8):
        cand = here / token
        if cand.exists():
            return cand.resolve()
        if (here / ".git").exists() or (here / "pyproject.toml").exists():
            break
        if here.parent == here:
            break
        here = here.parent
    return None


def skill_of(board, page):
    """Recover the skill folder from the page's own managed marker."""
    m = MARKER.search(page.read_text(encoding="utf-8"))
    return resolve_token(board, m.group(2)) if m and m.group(2) else None


def group_home(board, group):
    """Where that group lives, so a generated page lands with its siblings."""
    lines = (board / "board.md").read_text(encoding="utf-8").split("\n")
    # `## Pages` ENDS at the next `## ` heading. Walking to the end of the file
    # instead put a new page inside `## Links` when its group was the last one,
    # which the build then reported as unlisted. `structure_op` has always
    # bounded the section this way; this path had not.
    ps = next((i for i, ln in enumerate(lines)
               if re.match(r"^## (?:Pages|Roster)\b", ln)), None)
    pend = next((i for i in range((ps or 0) + 1, len(lines))
                 if lines[i].startswith("## ")), len(lines)) if ps is not None else len(lines)
    keys = [(i, m.group(1), m.group(2)) for i, ln in enumerate(lines)
            if (m := re.match(r"^###\s+(Q-[A-Z][A-Za-z]*|Q[0-9A-Za-z]+)\s*·\s*(.+?)\s*$",
                              ln.strip()))]
    hit = next((k for k in keys if k[1].casefold() == group.casefold()), None)
    if not hit:
        return None, None, lines, None
    i, key, title = hit
    end = next((j for j in range(i + 1, pend)
                if lines[j].strip().startswith("### ")), pend)
    listed = {ln.strip() for ln in lines[i + 1:end] if ln.strip().endswith(".md")}
    homes = {p.parent for p in page_files(board) if p.name in listed}
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:30].rstrip("-")
    default = key if re.match(r"^Q-[A-Z]", key) else f"{key}-{slug}"
    home = homes.pop() if len(homes) == 1 else board / default
    if re.match(r"^Q-[A-Z]", key):          # a named family takes no number
        return home, (key, None), lines, (i, end)
    nums = [int(m.group(1)) for p in page_files(board)
            if (m := re.match(rf"^{key}(\d+)", p.name))]
    return home, (key, max(nums, default=0) + 1), lines, (i, end)


def cmd_new(a):
    board, skill_dir = Path(a.board).resolve(), Path(a.skill).resolve()
    defn = unit(skill_dir)[0]
    if not defn.is_file():
        return f"{skill_dir} has no SKILL.md and is not a definition file"
    home, nxt, lines, span = group_home(board, a.group)
    if home is None:
        return f"no group {a.group!r} in board.md (heading must be `### Q<key> · title`)"
    fm = frontmatter(defn)
    name = fm.get("name", skill_dir.stem)
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    # A skill page is its OWN KIND, `Skill-<unit>-<slug>.md` (JL 260731: "remove
    # Q, from Q-Skill to be Skill ... Like Skill will be a special Page"). The
    # unit orders the roster, the slug says which skill it mirrors, and the id
    # is `Skill-<unit>`. It takes this name in WHATEVER group lists it: the kind
    # comes from what the page is, never from where it sits. (The 260727 named
    # family `Q-Skill-<name>.md` still parses on older boards; this tool just
    # stops minting it.)
    # An AGENT mirrors a single .md definition and gets its own prefix
    # (JL 260731: "we will call it Agent-1 ... Below the skill"): a skill is
    # LOADED, an agent is DISPATCHED, and the roster label says which. unit()
    # already discriminates: a folder is a skill, a lone file is an agent.
    kind = "Skill" if unit(skill_dir)[2] is not None else "Agent"
    used = [int(m.group(1)) for p in page_files(board)
            if (m := re.match(rf"^{kind}-(\d+)-", p.name))]
    start = 0 if kind == "Skill" else 1        # Agent numbering starts at 1 (JL)
    fname = f"{kind}-{max(used, default=start - 1) + 1}-{slug}.md"
    dest = home / fname
    if dest.exists():
        return f"{rel(board, dest)} already exists"
    stamp = a.stamp
    home.mkdir(parents=True, exist_ok=True)
    dest.write_text(STUB.format(name=name, version=fm.get("version", "?"),
                                block=block(board, skill_dir),
                                tree=tree_block(board, skill_dir),
                                log=log_block(board, skill_dir),
                                stamp=stamp, base=rel(board, skill_dir)),
                    encoding="utf-8")
    at = span[1]
    while at > span[0] + 1 and not lines[at - 1].strip():
        at -= 1
    lines[at:at] = [fname]
    (board / "board.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {rel(board, dest)}  (listed under {a.group})")
    return None


def cmd_sync(a):
    board = Path(a.board).resolve()
    pages = []
    if a.all:
        pages = [p for p in page_files(board) if has_block(p)]
    else:
        p = find_page(board, a.page)
        if not p:
            return f"no page {a.page!r} on this board"
        pages = [p]
    for page in pages:
        skill_dir = skill_of(board, page)
        if not skill_dir or not unit(skill_dir)[0].is_file():
            print(f"⚠️  {page.name}: its source is gone")
            continue
        text = page.read_text(encoding="utf-8")
        maker = {"tree": tree_block, "body": block, "log": log_block}
        new, missing = text, []
        for part in PARTS:
            a, b = start_of(part), end_of(part)
            # A MARKER ONLY COUNTS AT THE START OF A LINE, and this loop used a
            # plain `find()` that did not. `has_block` was fixed for exactly this
            # in 260726 and this path was not, so the bug sat here until a skill
            # whose own SKILL.md DRAWS the page anatomy was mirrored on 260803:
            # the figure quoted `<!-- haipipe:skill:log:start …` inside a fence,
            # that text landed in the generated Content span, `find()` matched
            # the QUOTE instead of the real marker, and the splice deleted the
            # page's authored Aims, States and Log. Silently, and only on the
            # page most likely to document the mechanism.
            i, j = _span_at_line_start(new, a), _span_at_line_start(new, b)
            if i < 0 or j < 0:
                missing.append(part)
                continue
            new = new[:i] + maker[part](board, skill_dir) + new[j + len(b):]
        if missing == list(PARTS):
            print(f"⚠️  {page.name}: no managed block")
            continue
        if missing:
            print(f"⚠️  {page.name}: no {', '.join(missing)} span (older page)")
        # The version rides the TITLE and is DERIVED, so sync refreshes it. It
        # belongs there because the title is what the index row prints, so
        # `haipipe-board · v0.41.0` is legible from the front page without
        # opening anything (JL 260727). `state:` keeps only the health judgment;
        # putting both on one line made a machine value and a human one compete.
        # The FILENAME never carries it: a name that changed every release would
        # break every link to the page.
        ver = frontmatter(unit(skill_dir)[0]).get("version", "")
        if ver:
            new = re.sub(r"^#\s+(.+?)(?:\s*·\s*v[0-9][0-9.]*)?\s*$",
                         lambda m: f"# {m.group(1).rstrip()} · v{ver}", new,
                         count=1, flags=re.M)
        if new == text:
            print(f"·  {page.name} already current")
        else:
            page.write_text(new, encoding="utf-8")
            print(f"✅ {page.name} synced")
    return None


def cmd_check(a):
    board = Path(a.board).resolve()
    bad = 0
    for page in page_files(board):
        if not has_block(page):
            continue
        text = page.read_text(encoding="utf-8")
        saved = re.search(MARKER, text)
        skill_dir = skill_of(board, page)
        if not skill_dir or not unit(skill_dir)[0].is_file():
            print(f"❌ {page.name}: source missing"); bad += 1; continue
        now = digest(skill_dir)
        if not saved or saved.group(1) != now:
            was = saved.group(1) if saved else "none"
            print(f"❌ {page.name}: stale (saved {was}, current {now}) "
                  f"-> skillpage.py sync {board} {page.name.split('-')[0]}")
            bad += 1
        else:
            print(f"✅ {page.name}")
    return f"{bad} stale" if bad else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("board"); n.add_argument("skill")
    n.add_argument("--group", required=True); n.add_argument("--slug", default="")
    n.add_argument("--stamp", required=True, help="YYMMDD HHMM for the Log line")
    s = sub.add_parser("sync"); s.add_argument("board")
    s.add_argument("page", nargs="?", default=""); s.add_argument("--all", action="store_true")
    c = sub.add_parser("check"); c.add_argument("board")
    a = ap.parse_args(argv)
    err = {"new": cmd_new, "sync": cmd_sync, "check": cmd_check}[a.cmd](a)
    if err:
        print(f"❌ {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
