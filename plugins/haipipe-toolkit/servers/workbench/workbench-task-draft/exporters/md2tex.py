#!/usr/bin/env python3
"""md2tex.py -- one or more accepted Board Pages become LaTeX sections.

QC5's central open item was "there is no generator, and that is the real
finding": no `.py` or `.sh` in the family turned a page into a section, so
"generated, one way" was a rule an agent was asked to obey rather than a step
something performed. This is that step.

It is the SIBLING of md2docx.py and reads the same `## Content` by the same
rules, which is the point: Word and LaTeX are two projections of one source, so
they must not disagree about what the source says.

    python3 md2tex.py <page.md> [...] --paper-root DIR [-o OUTDIR]

WHAT IT READS, and what it drops (QC5's read-and-drop table)
    ###   -> \\section / \\subsection, by the depth of its number
    ####  -> a paragraph boundary; the `(job)` line under it is scaffolding
    prose -> one paragraph per #### block, sentences joined
    \\citep{} \\ref{} kept verbatim: they are already LaTeX
    > lanes DROPPED. In Word they become comments; here they have nowhere to go.

A Page whose head says `content-format: latex` holds LaTeX source in Content
(a Section migrated from a manuscript): its lines pass through unescaped, one
LaTeX paragraph per heading block (`build_latex_section`).

REFUSE TO REGRESS, which QC5 demands by name. Sync runs one way, so a page whose
Content lost a citation would silently empty that section's bibliography. Before
writing over an existing section the generator compares the citation KEYS in
both and REFUSES if a key would leave. Measured 2026-07-27: all nine pages carry
real `\\citep{}` in prose (110 total, 0 plain-text author-year), so the check
passes today. It exists for the day one of them does not.

A REFUSAL IS A FAILURE, not a note (261103, the MISQ paper): the old fragment
stays on disk, so the paper build printed three Sections' OLD words with no
warning. A refused Section now prints `❌ REFUSED` with the dropped keys and the
old fragment's date, and the script exits 2. An INTENDED drop (a rewrite, a
paragraph moved to another Section) passes with `--accept-dropped-keys`, one key
at a time, and only when the key is still cited by another Section of the paper
(`--paper-pages`, else the Section Pages beside this one) or a revise card in
`draft/records/<stem>-revise.md` removed it (its Original cites the key, its
Expected does not). A key that fails both stays refused, named.

WHERE IT WRITES. The caller supplies `--outdir`; without one, the first Page's
local `latex/` folder is used. This writer emits Page TeX only. The Board export
door owns the standalone wrapper and LuaLaTeX run; whole-paper assembly belongs
to the thin Paper composer.
"""
import argparse
import os
import pathlib
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# The parts of this module live in their own files; every name still answers here.
from md2tex_prose import (  # noqa: F401
    CODE_SPAN, CONTENT_FORMAT, DISPLAY_PLACEHOLDER, ESTABLISHES, EXPORT_SCAFFOLD, GROUP_TITLE, LEVEL, REF,
    SECTION_TITLE, _BADGE, _FENCE_MAP, _PLAIN_SPECIALS, _SEQSPLIT_MIN, _TEX_SPECIALS, badge_sub, code_span_tex,
    content_format_of, display_placeholder_tex, escape_prose, fence_verbatim, keywords_text_of, render_prose,
    section_title_of, strip_number,
)

from importlib import util as _util           # noqa: E402

_spec = _util.spec_from_file_location("md2docx", os.path.join(HERE, "md2docx.py"))
md2docx = _util.module_from_spec(_spec)
_spec.loader.exec_module(md2docx)             # reuse the SAME reader

CITE = re.compile(r"\\cite[tp]?\*?\{([^}]*)\}")
# The first line of every fragment this script writes; a file without it is not ours.
GENERATED_MARK = "% GENERATED from"


def keys_of(text):
    """every citation KEY in this text. A \\citep{a,b} is two keys, not one citation."""
    out = set()
    for group in CITE.findall(text):
        out |= {k.strip() for k in group.split(",") if k.strip()}
    return out


# ── a dropped key: which ones a person meant (--accept-dropped-keys) ─────────
# A Section Page is `<group>/<name>/<name>.md`; its revise cards are
# `<name>/draft/records/<name>-revise.md`. TOADD is a placeholder, never a work.
OLD_GROUP = re.compile(r"^B[a-z]-")          # Ba-<venue>-Main, Bb-<venue>-Appendix
CARD_FIELD = re.compile(r"^\s*(?:-\s*)?([A-Z][A-Za-z ]{0,30}):\s?(.*)$")


def sibling_sections(page):
    """The other Section Pages of this page's paper, the default "elsewhere".

    On the ladder they sit in the same version Job (`jNN_writing_*/tNN_*/tNN_*.md`);
    in the older layout the Main and Appendix groups (`Ba-*`, `Bb-*`, `Bc-*`) are
    one paper, so every `B?-` group beside this one counts."""
    group = os.path.dirname(os.path.dirname(os.path.abspath(page)))
    groups = [group]
    if OLD_GROUP.match(os.path.basename(group)):
        parent = os.path.dirname(group)
        groups = [os.path.join(parent, g) for g in sorted(os.listdir(parent))
                  if OLD_GROUP.match(g) and os.path.isdir(os.path.join(parent, g))]
    out = []
    for g in groups:
        for name in sorted(os.listdir(g)):
            cand = os.path.join(g, name, name + ".md")
            if (not name.startswith((".", "_")) and os.path.isfile(cand)
                    and os.path.realpath(cand) != os.path.realpath(page)):
                out.append(cand)
    return out


def section_keys(page, root):
    """The keys a Section prints now, read by this script's own reader; the raw
    text's keys if the page cannot be read as a Section."""
    try:
        return keys_of(build_section(page, md2docx.Displays(root), []))
    except (Exception, SystemExit):
        try:
            return keys_of(pathlib.Path(page).read_text(encoding="utf-8", errors="replace"))
        except OSError:
            return set()


def revise_cards(page):
    """[(heading, original, expected)] from `draft/records/<stem>-revise.md`.

    A card is a `###` block; `Original:` and `Expected:` may run over several
    lines until the next field or heading. A card without an Expected removed
    its Original outright."""
    stem = os.path.splitext(os.path.basename(page))[0]
    path = os.path.join(os.path.dirname(os.path.abspath(page)), "draft", "records", stem + "-revise.md")
    if not os.path.isfile(path):
        return []
    cards, card, field = [], None, None
    for line in pathlib.Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#"):
            if card:
                cards.append(card)
            card = {"heading": line.lstrip("#").strip(), "Original": "", "Expected": ""}
            field = None
            continue
        if card is None:
            continue
        m = CARD_FIELD.match(line)
        if m:
            field = m.group(1) if m.group(1) in ("Original", "Expected") else None
            if field:
                card[field] = m.group(2)
        elif field and line.strip():
            card[field] += " " + line.strip()
    if card:
        cards.append(card)
    return [(c["heading"], c["Original"], c["Expected"]) for c in cards if c["Original"]]


def explain_drops(page, lost, others, root):
    """{key: why it may leave, or None}. A key passes when another Section of the
    paper still cites it, or when a revise card's Original cites it and its
    Expected does not. `page` is the Section's own path (its records live there)."""
    lost, why = list(lost), {}
    for other in others:
        if os.path.realpath(other) == os.path.realpath(page):
            continue
        hit = section_keys(other, root) & set(lost)
        for k in hit:
            why.setdefault(k, "cited in %s" % os.path.splitext(os.path.basename(other))[0])
    cards = revise_cards(page)
    for k in lost:
        if k in why:
            continue
        card = next((h for h, o, e in cards if k in keys_of(o) and k not in keys_of(e)), None)
        why[k] = ("removed by revise card '%s'" % " · ".join(card.split(" · ")[:3])) if card else None
    return why


def drop_check(page, fragment, root, accept=False, others=None, origin=None):
    """Would this script refuse to replace `fragment` with `page`'s Section now?

    -> {"lost": [...], "accepted": {key: why}, "refused": [...]}. Without
    `accept` every lost key is refused. `origin` is the Section's own path when
    `page` is a temporary copy (the LaTeX lane rewrites display tokens in one)."""
    if not os.path.isfile(fragment):
        return {"lost": [], "accepted": {}, "refused": []}
    had = keys_of(pathlib.Path(fragment).read_text(encoding="utf-8", errors="replace"))
    lost = sorted(had - section_keys(page, root) - {"TOADD"})
    if not lost or not accept:
        return {"lost": lost, "accepted": {}, "refused": lost}
    home = origin or page
    why = explain_drops(home, lost, sibling_sections(home) if others is None else others, root)
    return {"lost": lost, "accepted": {k: why[k] for k in lost if why[k]},
            "refused": [k for k in lost if not why[k]]}


def written_at(path):
    """A file's own time, as a reader reads it."""
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(path)))


def build_latex_section(page):
    """`content-format: latex`: `## Content` is LaTeX source, printed as written.

    Markdown headings (`###`, `####`) and `>` evidence lanes are Page structure,
    not manuscript, and are dropped; HTML comments (the `realizes:` tags) go
    too. A heading or a blank line ends a LaTeX paragraph; a `>` lane under a
    sentence does not. The lines inside a paragraph are kept, one per line,
    unescaped."""
    raw = pathlib.Path(page).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    lines = raw.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == "## Content"), None)
    if start is None:
        raise SystemExit(f"{page}: no ## Content section")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    paragraphs, current = [], []
    for line in lines[start + 1:end]:
        text = line.rstrip()
        if text.lstrip().startswith(">"):
            continue
        if not text.strip() or text.lstrip().startswith("#"):
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(text)
    if current:
        paragraphs.append(current)
    return "\n\n".join("\n".join(p) for p in paragraphs) + "\n"


def build_section(page, displays, report, keep_fences=False):
    if content_format_of(page) == "latex":
        return build_latex_section(page)
    blocks, nfenced = md2docx.parse_page(page, keep_fences=keep_fences)
    declared = section_title_of(page)
    # A structured abstract (JL 261021): its labels open their paragraphs as `\noindent\textbf{<label>}`
    # and its unnumbered divisions print as `\section*{Key Points}`, `\section*{Abstract}`, which is
    # the shape the paper's JAMA renderer reads (hai-paper-assemble latex_room_to_docx.py).
    abstract = md2docx.is_abstract_page(pathlib.Path(page).read_text(encoding="utf-8", errors="ignore"))
    label = None
    if nfenced and not keep_fences:
        report.append(f"{os.path.basename(page)}: {nfenced} fenced sketch(es) dropped")
    out, buf, seen = [], [], set()

    def flush():
        if buf:
            # A BLANK line, not a bare newline: LaTeX ignores a single "\n",
            # so every pbreak was flushing into the SAME printed paragraph and
            # a three-paragraph division read as one run-on (JL 260815, the
            # QPf3 comparison).
            out.append(" ".join(buf) + "\n\n")
            buf.clear()

    for b in blocks:
        if b[0] == "skipped-lane":
            continue
        if b[0] == "label":
            flush()
            label = b[1]
            continue
        if b[0] == "fence":
            flush()
            out.append(fence_verbatim(b[1]))
            continue
        if b[0] == "pbreak":
            flush()
            continue
        if b[0] == "table":
            flush()
            ncol = max(len(r) for r in b[1])
            cell = lambda c: badge_sub(CODE_SPAN.sub(code_span_tex, render_prose(c)))
            rows = [" & ".join(cell(c) for c in r + [""] * (ncol - len(r))) + r" \\" for r in b[1]]
            out.append("\\begin{center}\\small\\begin{tabular}{%s}\n\\toprule\n%s\n\\midrule\n%s\n\\bottomrule\n"
                       "\\end{tabular}\\end{center}\n\n" % ("l" * ncol, rows[0], "\n".join(rows[1:])))
            continue
        if b[0] == "h":
            flush()
            lvl = LEVEL[min(b[1], 3) - 1]
            name = strip_number(b[2])
            if b[1] == 1 and declared:
                name = declared
            star = "*" if abstract and not re.match(r"^\d", b[2]) else ""
            out.append("\n\\%s%s{%s}\n" % (lvl, star, escape_prose(name)))
            label = None
            continue
        line = b[1].strip()
        if ((line.startswith("<a ") and line.endswith("</a>"))
                or EXPORT_SCAFFOLD.match(line)):
            continue
        # Page Content uses bullets as its trace unit. The paper projection
        # keeps the sentence but not the Board-only list marker; otherwise a
        # paragraph exports as "- claim one. - claim two".
        line = re.sub(r"^[-*]\s+", "", line)
        if ESTABLISHES.match(line):
            continue
        if GROUP_TITLE.match(line):
            # Scaffolding on the PAPER path, where the sketch it captions was
            # dropped. On the keep-fences (board) path the sketch STAYS, so
            # dropping its caption gave the worst of both: an unnamed figure
            # (JL 260815, the QPf3 comparison). The caption rides as a bold
            # lede paragraph; the paper path is byte-identical to before.
            if not keep_fences:
                continue
            m = re.match(r"^\*\*([^*]+)\*\*\s*[:：]\s*(.*)$", line)
            if m:
                flush()
                out.append(badge_sub(
                    "\\textbf{%s}: %s" % (render_prose(m.group(1)),
                                          CODE_SPAN.sub(code_span_tex,
                                                        render_prose(m.group(2))))) + "\n\n")
            continue
        text = badge_sub(CODE_SPAN.sub(code_span_tex, render_prose(line)))
        if label:
            text, label = "\\noindent\\textbf{%s} %s" % (escape_prose(label), text), None
        buf.append(text)
        # A Display named in this sentence is \input right after the paragraph
        # that first mentions it, which is MISQ's stated rule: "embedded in the
        # body of the paper, following the first reference".
        for lab in REF.findall(b[1]):
            unit = displays.by_label.get(lab)
            if unit and unit["unit"] not in seen:
                seen.add(unit["unit"])
                flush()
                out.append("\\input{displays/%s/float}\n" % unit["unit"])
            elif not unit:
                report.append("%s: \\ref{%s} matches no display unit"
                              % (os.path.basename(page), lab))
    flush()
    body = "".join(out)
    # A $$ block arrives line by line, each line escaped as prose; inside it these are math (JL 261104: "Y\_ijc" printed).
    def _math_restored(m):
        s = m.group(0)
        for plain, escaped in _PLAIN_SPECIALS:
            s = s.replace(escaped, plain)
        return s
    body = re.sub(r"\$\$.+?\$\$", _math_restored, body, flags=re.S)

    # Keywords are manuscript metadata, not a numbered section.  The shared
    # reader drops their unnumbered heading but retains their prose, so restore
    # the conventional inline label and keep the terms out of the abstract's
    # paragraph.  Match the last exact occurrence so a later manuscript
    # division or a bullet-form keyword list remains valid, while ordinary
    # Sections with no Keywords division stay a no-op.
    keywords = keywords_text_of(page)
    if keywords:
        rendered = badge_sub(CODE_SPAN.sub(code_span_tex,
                                           render_prose(keywords)))
        at = body.rfind(rendered)
        if at >= 0:
            before = body[:at].rstrip()
            after = body[at + len(rendered):].lstrip()
            body = (before + "\n\n\\smallskip\n"
                    "\\noindent\\textbf{Keywords:} " + rendered + "\n\n"
                    + after)
        else:
            report.append("%s: Keywords division was not isolated in LaTeX"
                          % os.path.basename(page))
    return body


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="+")
    ap.add_argument("--paper-root", required=True)
    ap.add_argument("-o", "--outdir")
    ap.add_argument("--keep-fences", action="store_true",
                    help="render ``` sketches as verbatim blocks instead of "
                         "dropping them; the BOARD exporter's switch, a paper "
                         "keeps the drop (JL 260815)")
    ap.add_argument("--accept-dropped-keys", action="store_true",
                    help="let a citation key leave a Section when another Section "
                         "of the paper still cites it or a revise card removed it; "
                         "any other dropped key is still refused, by name")
    ap.add_argument("--paper-pages", nargs="+", metavar="PAGE",
                    help="the paper's Section Pages that count as 'cited elsewhere' "
                         "(default: the Section Pages beside each page, plus the "
                         "other pages of this call)")
    ap.add_argument("--origin", metavar="PAGE",
                    help="the Section's own .md when PAGE is a temporary copy "
                         "(its revise cards and sibling Sections are found from here)")
    a = ap.parse_args(argv)
    if a.origin and len(a.page) != 1:
        ap.error("--origin names the source of ONE page")

    root = os.path.abspath(a.paper_root)
    first_page = os.path.abspath(a.page[0])
    outdir = a.outdir or os.path.join(os.path.dirname(first_page), "latex")
    os.makedirs(outdir, exist_ok=True)
    displays = md2docx.Displays(root)
    report, refused, accepted, wrote, total_cites = [], [], [], [], 0

    for page in a.page:
        page = os.path.abspath(page)
        home = os.path.abspath(a.origin) if a.origin else page
        body = build_section(page, displays, report, keep_fences=a.keep_fences)
        n = len(CITE.findall(body))
        stem = os.path.splitext(os.path.basename(page))[0]
        dest = os.path.join(outdir, stem + ".tex")

        # REFUSE TO REGRESS (QC5). Compare against whatever this would replace.
        # It compares the SET OF KEYS, not the number of \citep COMMANDS. The
        # failure this guard exists to stop is a WORK disappearing from a section's
        # bibliography. Counting commands also stopped work that loses nothing:
        # joining two sentences that both cite Meyer_2009 drops one command and no
        # key, and on 260908 that blocked the humanizing rewrite of §1 while the
        # board's /_board/latex lane still answered ok:true, so the page silently
        # kept its old prose (20 commands vs 22, zero keys lost).
        prior = dest if os.path.exists(dest) else None
        # REFUSE TO REPLACE WORDS THIS SCRIPT DID NOT WRITE. A fragment without the
        # GENERATED header was written by hand or by a migration, so its words may
        # exist nowhere else. On 260930 an export of Paper-TimeEventDM replaced six
        # migrated Sections (404 lines of prose) with the Pages' planning notes.
        # Move the words into the Page (Draft, then `page.py adopt`) first, then
        # delete the old fragment to let this script own it.
        if prior:
            with open(prior, encoding="utf-8") as f:
                first = f.readline()
            if not first.startswith(GENERATED_MARK):
                refused.append("REFUSED %s: the existing %s.tex was not written by md2tex "
                               "(no GENERATED header), so its words may exist only there. "
                               "Move them into the Page and adopt, then delete the file."
                               % (stem, stem))
                continue
        if prior:
            had = keys_of(open(prior, encoding="utf-8").read())
            # TOADD is the placeholder for an owed citation, not a work: replacing
            # it with a checked key is the change this guard must let through
            # (261031: two checked keys replaced it in a Lancet appendix).
            lost = sorted(had - keys_of(body) - {"TOADD"})
            # A refusal keeps the OLD fragment, and a paper build prints it, so it
            # is a failure the caller must see (261103: three MISQ Sections printed
            # old words). An intended drop passes only when it is explained.
            why = {}
            if lost and a.accept_dropped_keys:
                others = a.paper_pages if a.paper_pages else (
                    sibling_sections(home) + [os.path.abspath(q) for q in a.page])
                why = explain_drops(home, lost, [os.path.abspath(q) for q in others], root)
            unexplained = [k for k in lost if not why.get(k)]
            if unexplained:
                since = written_at(prior)
                if a.accept_dropped_keys:
                    refused.append(
                        "REFUSED %s: --accept-dropped-keys cannot explain %d of %d dropped "
                        "citation key(s): %s (no other Section cites it and no revise card in "
                        "draft/records/%s-revise.md removed it). The old fragment %s "
                        "(written %s) stays, so a paper build prints its OLD words."
                        % (stem, len(unexplained), len(lost), ", ".join(unexplained),
                           stem, prior, since))
                else:
                    refused.append(
                        "REFUSED %s: %d citation key(s) would leave this Section: %s. "
                        "The old fragment %s (written %s) stays, so a paper build prints "
                        "its OLD words. If the drop is intended, rerun with "
                        "--accept-dropped-keys (a key passes when another Section still "
                        "cites it or a revise card removed it)."
                        % (stem, len(lost), ", ".join(lost), prior, since))
                continue
            accepted += ["%s: dropped key %s accepted, %s" % (stem, k, why[k]) for k in lost]
        with open(dest, "w", encoding="utf-8") as f:
            f.write("%s %s by md2tex.py. Do not hand-edit: sync is\n"
                    "%% one-way and the next run overwrites this file.\n%s"
                    % (GENERATED_MARK, os.path.relpath(home, root), body))
        wrote.append((stem, n))
        total_cites += n

    print("%s %s" % ("✅" if not refused else "❌", outdir))
    for stem, n in wrote:
        print("   %-34s %3d citations" % (stem + ".tex", n))
    print("   %d section(s) written · %d refused · %d citations total"
          % (len(wrote), len(refused), total_cites))
    for r in accepted:
        print("   ✅ " + r)
    if report:
        print("⚠️  %d note(s):" % len(report))
        for r in dict.fromkeys(report):
            print("    " + r)
    if refused:
        print("❌ %d Section(s) NOT rebuilt:" % len(refused))
        for r in refused:
            print("    " + r)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
