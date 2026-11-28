"""A paper version's views (one send, a Job on the ladder): build checks, Delivery, Sections, comments and the cover letter.
Moved from paper_theme.py, which re-exports every name here so `from live.paper_theme import version_spaces` keeps working."""
from __future__ import annotations

from src.common import delivery_dir
import re
from pathlib import Path

from host_paths import skill_dir
from live import paper as P
from live.frame import Space, delivery_view, esc, link, pop, reader, rel, table, work_tree
from live import paper_spaces_delivery as PD
from live.paper_theme import THEME, _data, _disk_version, _empty, _fold, _kv, _pick, _run_cards, _st, pv
from live.paper_theme_report import _HEAD, _base_rows, _brow
from live.paper_theme_section import _header


def _checks(d):
    """The build's checks, as paper.py's Checks view reads them from build-manifest.json."""
    man = d["delivery"]["manifest"] or {}
    if not man:
        return _empty("No build yet.")
    build, sub, rd = man.get("build") or {}, man.get("submission_readiness") or {}, man.get("readiness") or {}
    facts = [("main text", f'{build.get("main_text_words", "?")} words'
                           + (f' · from {build["main_text_words_from"]}' if build.get("main_text_words_from") else "")
                           + (f' · limit {build["main_text_word_limit"]}' if build.get("main_text_word_limit") else "")),
             ("citations", f'{build.get("citations", "?")} cited · {man.get("bib_entries", "?")} bib entries'),
             ("displays", f'{build.get("main_tables", "?")} main table(s) · {build.get("main_figures", "?")} main figure(s)'),
             ("pages ready", ("⬜ not ready: " + ", ".join(P._not_ready_ids(rd))) if rd.get("not_ready")
                             else "✅" if rd else ""),   # a mark and the names, never "N of M"
             ("submission", str(sub.get("status", "?")) + (" · " + "; ".join(sub.get("blockers") or []) if sub.get("blockers") else ""))]
    if d["delivery"]["stale"]:
        facts.append(("changed since build", ", ".join(d["delivery"]["stale"])))
    g4 = next((v for g, _, v in d.get("gates") or [] if g == "G4"), "")
    if g4:
        facts.append(("G4 compile", g4))
    mark = lambda v: _st(v, "✓" if v else "✗")
    checks = [(esc(k.replace("_", " ")), mark(v) if isinstance(v, bool) else esc(str(v)))
              for k, v in (build.get("checks") or {}).items()]
    render = man.get("render") or {}
    if render:
        checks += [("latexmk", mark(render.get("latexmk_rc") == 0)), ("docx", mark(render.get("docx_rc") == 0))]
    pages = [(esc(p["id"]), mark(p["frag"]), "—" if p["ready"] is None else mark(p["ready"]),
              esc("; ".join(list(p["reasons"]) + list(p["warnings"]) + (["changed since build"] if p["stale"] else []))))
             for p in d["delivery"]["pages"]]
    # engine ≥0.8 writes each unresolved \ref as {"page", "ref"}; older manifests wrote a bare string
    warns = [w if isinstance(w, str) else str(w) for w in man.get("warnings") or []] + [
        "unresolved \\ref: " + (x if isinstance(x, str) else f'{x.get("ref", "?")} ({x.get("page", "?")})')
        for x in man.get("unresolved_refs") or []]
    return (_kv([(k, esc(v)) for k, v in facts]) + table(("check", "result"), checks)
            + "<h3>Pages</h3>" + table(("page", "fragment", "ready", "notes"), pages)
            + ("<h3>Warnings</h3><ul>" + "".join(f"<li>{esc(w)}</li>" for w in warns) + "</ul>" if warns else ""))


def _frame(d, path, title):
    # src with loading=lazy: the frame's loader fills only a .topic row's first iframe, on open
    return f'<iframe class=st-frame title="{esc(title)}" src="{esc(P._tree_url(d, path))}" loading=lazy></iframe>'


def _preview(d, suffix):
    """The paper as built, embedded: the PDF, or for Word its PDF twin under one line naming the .docx
    (the old page's Preview, paper_spaces_delivery._preview_html)."""
    outs = [o for o in PD._outputs(d, suffix) if o["exists"]]
    if not outs:
        return _empty("Not built yet.")
    main = next((o for o in outs if "main" in o["what"]), outs[0])
    if suffix == ".pdf":
        return _frame(d, main["path"], main["rel"])
    twin = Path(main["path"]).with_suffix(".pdf")
    line = (f'<p class=mut>{P._file_link(d, main["path"], main["rel"])} · {esc(main["size"])} · {esc(main["stamp"])}'
            + (" · the preview is older than the .docx; rebuild" if twin.is_file() and twin.stat().st_mtime
               < Path(main["path"]).stat().st_mtime else "") + "</p>")
    return line + (_frame(d, twin, main["rel"]) if twin.is_file() else _empty("No preview yet: the next paper build draws it."))


def _built(d, suffix, checks=True):
    """LaTeX and Word: Preview, then Artifacts (JL 261007: "our previous style", s12); then Checks, unless
    the tab has a Checks view of its own (a version's)."""
    return pv('<h3 class="space-h">Preview</h3>' + _preview(d, suffix)          # the old page's Artifacts, Checks
              + '<h3 class="space-h">Artifacts</h3>' + PD._artifacts_html(d, suffix)
              + ('<h3 class="space-h">Checks</h3>' + PD._checks_html(d) if checks else ""))


def _cover(d):
    cover = PD._cover(d)
    if cover is None:
        return _empty("No cover letter built yet: add a [coverletter] block to delivery/paper-build.toml and run the build.")
    base = d["delivery"]["dir"]
    pdf = (cover.get("outputs") or {}).get("pdf")
    pdf = (base / pdf) if pdf and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
    head = (f'<p><b>{esc(cover.get("round") or "letter")}</b> · {"ready" if cover.get("ready") else "not ready"}'
            + (f' · {pop(P._tree_url(d, pdf), "cover letter", "Open the letter ↗")}' if pdf and pdf.is_file() else "") + "</p>")
    rows = [(esc(c.get("check", "")), _st(c.get("ok"), "✓" if c.get("ok") else "⚠"), esc(c.get("detail", "")))
            for c in cover.get("checks") or []]
    return head + table(("check", "", "detail"), rows)


def _rounds(d):
    return pv(PD._round_cards(d))                                   # the old Round cards (JL 261007)


def section_states(board: Path, version: Path) -> list:
    """Each Section of one version's build, from its build-manifest.json (JL 261011: "how could the delivery from
    the section level link back to the block level delivery"): (Section folder, ready, why not, fragment, state),
    state ✅ when the fragment is older than the build, ❗ when it changed after it, ⬜ when it was never exported."""
    import json
    from datetime import datetime
    man_path = delivery_dir(version) / "build-manifest.json"
    try:
        man = json.loads(man_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    try:
        built = datetime.fromisoformat(str(man.get("built") or "")).timestamp()
    except ValueError:
        built = None
    out = []
    for page in man.get("pages") or []:
        sid = str(page.get("id") or "")
        frag = board / str(page.get("fragment") or "") if page.get("fragment") else None
        if frag is None or not frag.is_file():
            state = "⬜ not exported"
        elif built is not None and frag.stat().st_mtime > built:
            state = "❗ changed after the build: rebuild"
        else:
            state = "✅ in the build"
        out.append((version / sid, bool(page.get("ready")), "; ".join(page.get("reasons") or []), frag, state,
                    str(man.get("built") or "")[:16].replace("T", " ")))
    return out


def _section_rows(board: Path, versions, root: Path) -> str:
    """The Sections of each version's build as one table: Section (its part of the Delivery), ready, in the build."""
    from live.frame import ROUTE, href
    from urllib.parse import urlencode
    rows = []
    for v in versions:
        for sec, ready, why, frag, state, built in section_states(board, v):
            rows.append((link(href(sec, root, THEME, "Delivery"), f"{v.name.split('_', 1)[0]} › {sec.name}"),
                         esc("✅ ready" if ready else "✗ " + (why or "not ready")),
                         esc(f"{state} · built {built}" if built else state),
                         link(ROUTE + "?" + urlencode({"path": rel(sec, root)}), "folder ↗")))
    return table(("Section", "ready at the build", "in the build", "back to"), rows) if rows else ""


def _version_delivery(d, board, job, root):
    """A version's Delivery as folding item cards, no third row (JL 261007: "item card based", s12): Manuscript
    (the PDF, the Word file), Letters (the cover letter), Checks (submission readiness), Sent (each frozen send)."""
    dv = d["delivery"]
    if dv["dir"] is None:
        return Space(html=_empty("No delivery/ yet: Build writes it."), run_types=_delivery_runs())
    cards = delivery_view(job, root, THEME)         # the manuscript, the letters: one card per result (b10 s32-D18)
    out = []
    for suffix, kind in ((".pdf", "LaTeX"), (".docx", "Word")) if not cards else ():
        main = next((o for o in PD._outputs(d, suffix) if "main" in o["what"]), None) or \
            next(iter(PD._outputs(d, suffix)), None)
        if main is None:
            continue
        meta = " · ".join(x for x in (("built" if main["exists"] else "not built"), "stale" if main["stale"] else "",
                                      main["size"], main["stamp"]) if x)
        body = _preview(d, suffix)
        if suffix == ".pdf" and dv["displays"]:
            body += table(("printed", "label", "from the Section"),
                          [(esc(r[0]), f"<code>{esc(r[2])}</code>", esc(r[4])) for r in dv["displays"]])
        out.append(("Manuscript", _fold(f"{esc(Path(main['rel']).name)} · {kind}", esc(meta), body,
                                        P._file_link(d, main["path"], "↗") if main["exists"] else "")))
    if cards and dv["displays"]:                    # what the PDF prints, kept beside the cards
        out.append(("Manuscript", _fold("displays in the build", esc(f'{len(dv["displays"])} printed'),
                                        table(("printed", "label", "from the Section"),
                                              [(esc(r[0]), f"<code>{esc(r[2])}</code>", esc(r[4])) for r in dv["displays"]]))))
    cover = PD._cover(d)                             # with cards, a built cover letter is one of them
    if not cards and cover is not None:
        pdf = (cover.get("outputs") or {}).get("pdf")
        pdf = (dv["dir"] / pdf) if pdf and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
        body = _frame(d, pdf, "cover letter") if pdf and pdf.is_file() else _empty("Not built yet.")
        out.append(("Letters", _fold("cover letter", esc(("built" if pdf and pdf.is_file() else "not built") + " · "
                                                         + ("ready" if cover.get("ready") else "not ready")), body)))
    elif not cards:
        out.append(("Letters", _fold("cover letter", "not built", _empty(
            "No cover letter built yet: add a [coverletter] block to delivery/paper-build.toml and run the build."))))
    sections = _section_rows(board, [job], root)
    if sections:
        out.append(("Sections", sections))
    man = dv["manifest"] or {}
    rd = man.get("readiness") or {}
    g4 = next((v for g, _, v in d.get("gates") or [] if g == "G4"), "")
    meta = " · ".join(x for x in (str(man.get("status", "no build")), f"G4 {g4.split(' · ')[0]}" if g4 else "") if x)
    out.append(("Checks", _fold("submission readiness", esc(meta), _checks(d))))
    for frozen in sorted(x for b in _version_round_pages(board, job) for kind in ("sent", "released")
                         for x in (b.parent / kind).glob("*/") if x.is_dir()):
        files = sorted(f for f in frozen.rglob("*") if f.is_file() and not f.name.startswith("."))
        body = table(("file", "size"), [(P._file_link(d, f, f.relative_to(frozen).as_posix()), esc(P._size(f)))
                                        for f in files[:40]]) + (f"<p class=mut>and {len(files) - 40} more</p>"
                                                                if len(files) > 40 else "")
        out.append(("Sent", _fold(f"{frozen.parent.name}/{frozen.name}", f"frozen · {frozen.parent.parent.name} · "
                                  f"{len(files)} files", body)))
    html, last = cards, ""
    for group, card in out:
        html += (f"<h3>{esc(group)}</h3>" if group != last else "") + card
        last = group
    return Space(html=html, run_types=_delivery_runs())


def _delivery_runs():
    """Build · Check (Send stays a proposal, s12)."""
    return _run_cards("Job", "Delivery")


def _delivery(d, sub, opts=("delivery/", "LaTeX", "Word", "Cover letter", "Rounds"), board=None, root=None):
    s = _pick(sub, opts)
    if s == "delivery/":                            # every result of the Board, as the base's cards (b10 s32-D18)
        html = (delivery_view(board, root, THEME) if board is not None and root is not None else "") or \
            _empty("No delivery/ yet.")
    elif s in ("LaTeX", "Word"):
        html = (_empty("No delivery/ yet.") if d["delivery"]["dir"] is None else
                _built(d, ".pdf" if s == "LaTeX" else ".docx", checks="Checks" not in opts))
        if board is not None and root is not None:      # each version's Sections, in the build or not
            versions = [v for v in sorted(board.glob("j[0-9][0-9]_*/")) if (delivery_dir(v) / "build-manifest.json").is_file()]
            rows = _section_rows(board, versions, root)
            html += ('<h3 class="space-h">Sections in the build</h3>' + rows) if rows else ""
    elif s == "Cover letter":
        html = _cover(d)
    elif s == "Checks":
        html = _empty("No delivery/ yet.") if d["delivery"]["dir"] is None else _checks(d)
    else:
        html = _rounds(d)
    return Space(html=html, subspaces=opts, open=s, run_types=_delivery_runs())


# ── a Section: the base's Page Task, and the paper's four lines over it (◆, b16 s13, JL 261007) ──
# ── a version (Job), from s12: one send of the paper ────────────────────────────────────────────────
# Today a Job is one group folder (Ba-/Bb-/Bc-<desk>-<part>, level_patterns); on the ladder it is one
# version folder (jNN_v<N>_<desk>/) holding every Section and Round of one send. Either way its Pages are
# the Board's ## Pages entries under it, read through paper.collect() of the Board.
VERSION_AR = ("Questions", "Draft-Main", "Draft-Appendix", "Comments", "Cover letter")
VERSION_WD = ("All", "Main", "Appendix", "Letters")
# the five standing questions of a send (s12, the Job session): the question, what answers it
STANDING = (("J1", "What is the one-minute story?", "the telling's face, sNN-story-… beside the Jobs · this version's Abstract and Introduction"),
            ("J2", "Why this venue?", "venues/<venue>/call.md · the venue's playbook"),
            ("J3", "Which writing principles does it follow?", "the playbook's style · By reader expectations"),
            ("J4", "Is it ready to send?", "every Section's CHECK · Delivery › Checks (G4)"),
            ("J5", "What changed since the last send?", "a revision only: the comments report's Review Items"))


def _mine(board, job, rel_):
    """Whether a Page (its path relative to the Board) sits under this Job's folder."""
    return bool(rel_) and Path(rel_).parts[0] == job.relative_to(board).parts[0]


def _version_rows(d, board, job):
    return [r for r in P.section_rows(d) if r["page"] and _mine(board, job, r["page"]["rel"])]


def _version_round_pages(board, job):
    """The review batches of this send: today the Board's Bc-<desk>-Round/RD<NN>-…/, on the ladder the version's
    own RD<NN>-…/ and CM<NN>-…/ (hai-paper-comments)."""
    found = (list(board.glob("B[a-z]-*-Round/RD*/RD*.md")) + list(job.glob("RD*/RD*.md"))
             + [q for q in job.glob("reports/q[0-9][0-9]_*/q[0-9][0-9]_*.md")      # a comments report (JL 261007)
                if re.search(r"(?m)^page-type:\s*(comments|round)\b", q.read_text(encoding="utf-8", errors="replace"))]
             + list(job.glob("CM*/CM*.md")))                     # t3N_ is Letters (a cover letter), never comments
    return sorted({q.resolve() for q in found if q.stem == q.parent.name})


def _letter_pages(job):
    """The send's letters, its t3N_ Page Tasks (t31 cover letter, t32 response), in number order (s12)."""
    return sorted(q for q in job.glob("t3[0-9]_*/t3[0-9]_*.md") if q.stem == q.parent.name)


def _md_table(text, heading):
    """The first table under the first heading that names `heading`: (head, rows), lowercase head."""
    m = re.search(rf"(?ms)^#+[^\n]*{re.escape(heading)}[^\n]*\n(.*?)(?=^#+ |\Z)", text)
    lines = [l for l in (m.group(1).splitlines() if m else []) if l.startswith("|")]
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    return ([h.lower() for h in rows[0]], rows[1:]) if rows else ([], [])


def _comments(board, job, root):
    """Comments (s12) as the old page's item cards (JL 261007: "All the things to be the card"): one card per
    Review Item (cites · lands on · its state; opened, its work and reply), or, until a batch lists them, one per
    concern of its Feedback Concern Table."""
    cards = []
    for page in _version_round_pages(board, job):
        text = page.read_text(encoding="utf-8", errors="replace")
        opener = pop(reader(page, root), page.stem, page.stem + " ↗")
        head, body = _md_table(text, "Review Items")
        if body:
            for r in body:
                x = dict(zip(head, r))
                state = x.get("state", "") or "open"
                cards.append(P._card("item-" + x.get("item", ""), "Review", x.get("item", ""),
                                     esc("cites " + x.get("cites", "")), esc(x.get("lands on", "")), state,
                                     P._status_cls("✅" if state in ("answered", "applied") else state),
                                     [("work", esc(x.get("work", "") or "—")), ("reply", esc(x.get("reply", "") or "no reply yet")),
                                      ("comments", opener)], key=x.get("item", "")))
            continue
        head, body = _md_table(text, "Concern Table")
        for r in body:
            x = dict(zip(head, r))
            # one line on top (JL 261008: "this is the disaster"): the concern in full, its source under it, its
            # state; the route and the rest go inside, links rendered, so nothing squeezes the concern
            src = next((x[k] for k in ("source", "from", "raised by") if x.get(k)), "")
            cards.append(P._card("concern-" + x.get("item", ""), x.get("item", "") or "point",
                                 x.get("concern", ""), esc(src), "",
                                 x.get("state", "") or "open", P._status_cls(x.get("state", "")),
                                 [(k, P.inline(v)) for k, v in x.items() if v and k not in ("item", "concern")]
                                 + [("comments", opener)]))
    return pv(P._cards(cards, "No Review Items yet: a comments report's points land here, each with where it goes "
                              "and its reply."))


def _version_description(d, board, job, root, sub):
    opts = ("Version", "Venue rules")
    s = _pick(sub, opts)
    rows = _version_rows(d, board, job)
    if s == "Version":
        face = job / f"{job.name}.md"
        head = _header(face) if face.is_file() else {}       # the version's face (g03 D6): send · desk · venue …
        states = {}
        for r in rows:
            states[P._state_word(r["state"])] = states.get(P._state_word(r["state"]), 0) + 1
        html = _kv([("send", esc(head.get("send") or job.name)), ("desk", esc(head.get("desk") or P.paper_desk(d) or "—")),
                    ("venue", esc(head.get("venue") or P.venue_name(d) or "—"))]
                   + [(k, esc(head[k])) for k in ("state", "tells", "from", "responds-to", "answers") if head.get(k)] + [
                    ("Sections", esc(f"{len(rows)}: " + " · ".join(f"{n} {w}" for w, n in states.items()) if rows else "none")),
                    ("review batches", esc(str(len(_version_round_pages(board, job))))),
                    ("face", link(reader(face, root), face.name) if face.is_file()
                     else '<span class=mut>none yet: a version gets its own face on the ladder (jNN_v&lt;N&gt;_&lt;desk&gt;.md)</span>')])
    else:
        calls = sorted((board / "venues").glob("*/call.md"))
        html = (table(("venue", "call"), [(link(reader(c, root), c.parent.name), esc(rel(c, root))) for c in calls])
                if calls else f'<p>Venue: <b>{esc(P.venue_name(d) or "—")}</b> (from the Story).</p>'
                              + _empty("No venues/<venue>/call.md yet: its rules are read from there (b16 Q02)."))
    return Space(html=html, subspaces=opts, open=s, run_types=_run_cards("Job", "Description", s))


def _standing(d, job, root):
    """The send's questions as b03's own question row (JL 261007: the base frame's question_rows, "Q03 … │ no work
    yet │ report title ↗, answer, drawing thumbnail, report q03 · open"): the version's register (its ## Questions,
    a comments report among them), then the standing J1-J5 not asked there yet (J5 only for a revision), drawn in
    the same markup."""
    face = job / f"{job.name}.md"
    text = face.read_text(encoding="utf-8", errors="replace") if face.is_file() else ""
    rows = [_brow(qid, t, "not asked yet", "", f'<p class=mut>{esc(w)}</p>',
                  '<p class=mut>no report yet · Ask a Question writes it into ## Questions with its report</p>')
            for qid, t, w in STANDING
            if not re.search(rf"\b{qid}\b", text) and (qid != "J5" or re.search(r"(?m)^from:\s*j\d", text))]
    base = _base_rows(job, root)                    # the standing rows continue under the base's own head
    html = base + (("" if "q-head-row" in base else _HEAD) + "".join(rows) if rows else "")
    return html or _empty("No question yet: Ask a Question.")


# ── Draft-Main · Draft-Appendix (s12, JL 261007): one Question │ Work │ Report row per Section, in reading
# order; opened, the rendered draft and the Section's logic + narrative drawing side by side, both view only


PARA = re.compile(r"(?m)^#{3,4} +((?:C\d+\.)?P\d+)\b.*$")      # ### C1.P1 · … (a draft) · #### P1. … (a face)


def _paragraphs(folder, stem):
    """(planned, written) paragraphs: planned from the newest draft's Structure part, written = those with
    prose under its Draft part; a face that keeps its words in ## Content counts there."""
    def version(f):
        m = re.search(r"-draft-v([\d.]+)\.md$", f.name)
        return tuple(int(x) for x in m.group(1).split(".") if x) if m else ()
    drafts = sorted(folder.glob(f"draft/{stem}-draft-v*.md"), key=version)
    text = drafts[-1].read_text(encoding="utf-8", errors="replace") if drafts else ""
    parts = dict((m.group(1).lower(), m.start()) for m in re.finditer(r"(?m)^## +\d+ · (\w+)", text))
    cut = lambda a: text[parts[a]:min([v for v in parts.values() if v > parts[a]] or [len(text)])] if a in parts else ""
    planned = list(dict.fromkeys(PARA.findall(cut("structure") or text)))
    prose = lambda body: [i for i, b in zip(PARA.findall(body), PARA.split(body)[2::2]) if b.strip()]
    written = set(prose(cut("draft")))
    face = folder / f"{stem}.md"
    if not written and face.is_file():
        body = face.read_text(encoding="utf-8", errors="replace").partition("\n## Content")[2].split("\n## ", 1)[0]
        written = set(prose(body))
        planned = planned or list(dict.fromkeys(PARA.findall(body)))
    return len(planned), len(written)


# ── Cover letter (JL 261007, s12): the letter as the editor reads it, one row per paragraph ───────────────
ASSEMBLE = skill_dir("hai-paper-assemble") / "scripts"      # a skill, or a part of hai-paper
LETTER = (("¶1 · what we submit", "the version's face: title · article type · venue", ("submit", "what we", "manuscript")),
          ("¶2 · the one-minute story", "J1 · the one-minute story", ("story", "one-minute", "contribution", "finding")),
          ("¶3 · why this venue", "J2 · why this venue", ("venue", "fit", "journal", "why")),
          ("¶4 · declarations", "venues/<venue>/call.md: originality · conflicts · data · funding",
           ("declar", "conflict", "original", "funding", "data")),
          ("¶5 · suggested reviewers", "only when the venue asks", ("reviewer",)))

def _letter_words(board, job):
    """(paragraphs as [(heading, text)], the page that holds them, content | draft): from the version's cover
    letter Task (t3N_), else its batches, through hai-paper-assemble's own reader (cover_letter.py)."""
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location("cover_letter", ASSEMBLE / "cover_letter.py")
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
    except Exception:
        return [], None, ""
    pages = ([q for q in _letter_pages(job) if "cover" in q.stem] + _version_round_pages(board, job)
             + sorted(job.glob("t*_cover_letter*/t*_cover_letter*.md")))
    for page in pages:                              # the page's Content first, then its drafts, newest first
        drafts = sorted(page.parent.glob("draft/*-draft-v*.md"), key=C._draft_version, reverse=True)
        for src, where in [(page, "content")] + [(x, "draft") for x in drafts]:
            text = src.read_text(encoding="utf-8", errors="replace")
            heads = list(C.HEAD.finditer(text))
            top = next((i for i, h in enumerate(heads) if "cover letter" in h.group(2).lower()), None)
            if top is None:
                continue
            level, end, subs = len(heads[top].group(1)), len(text), []
            for h in heads[top + 1:]:
                if len(h.group(1)) <= level:
                    end = h.start()
                    break
                subs.append(h)
            named = []                              # each paragraph with the sub-heading above it, if any
            for k, cut in enumerate([heads[top]] + subs):
                stop = subs[k].start() if k < len(subs) else end
                body = text[cut.end():stop]
                named += [("" if k == 0 else cut.group(2).strip(), w) for w in (C.division("## x\n" + body, "x") or [])]
            if named:
                return named, src, where
    return [], None, ""


def _cover_letter(d, board, job, root):
    """One card per paragraph (what it says · the question or rule it answers; opened, its text), then the built
    letter embedded (Delivery › Cover letter keeps its files
    and checks)."""
    paras, src, where = _letter_words(board, job)
    cover = PD._cover(d) or {}
    state = ("ready" if cover.get("ready") else "not ready") if cover else "not built"
    headed = any(h for h, _ in paras)
    used, rows = set(), []
    for n, (slot, work, keys) in enumerate(LETTER):
        if headed:                                  # a paragraph answers the row its sub-heading names
            i = next((k for k, (h, _) in enumerate(paras) if k not in used and any(x in h.lower() for x in keys)), None)
            if i is not None:
                used.add(i)
            rows.append((slot, work, paras[i][1] if i is not None else ""))
        else:                                       # no sub-headings: the paragraphs in order, unmapped
            rows.append((slot, "—" if n < len(paras) else work, paras[n][1] if n < len(paras) else ""))
            used.add(n)
    rows += [(f"¶{k + 1} · {h or '—'}", "—", t) for k, (h, t) in enumerate(paras) if k not in used]
    body = pv(P._cards([P._card(f"para-{k}", slot.split(" · ")[0], slot.split(" · ", 1)[-1], esc(work), "",
                                "written" if text else "not written yet", "ok" if text else "mut", [],
                                body=f"<p>{esc(text)}</p>" if text else "") for k, (slot, work, text) in enumerate(rows)],
                       "No paragraph yet."))                # one card per paragraph (JL 261007: cards)
    source = (f'<p class=mut>words from {pop(reader(src, root), src.stem, src.name + " ↗")}'
              f' ({"its Content" if where == "content" else "its latest draft"}) · the letter: {esc(state)}</p>'
              if src else '<p class=mut>No letter yet: its words go in the cover letter Task (t31_cover-letter) '
                          'or the submission batch\'s <b>### Cover letter</b> division. The letter: ' + esc(state) + '</p>')
    pdf = (cover.get("outputs") or {}).get("pdf")
    base = d["delivery"]["dir"]
    pdf = (base / pdf) if pdf and base is not None and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
    built = ("<h3>The letter as built</h3>" + _frame(d, pdf, "cover letter") if pdf and pdf.is_file()
             else "<h3>The letter as built</h3>" + _empty("Not built yet: Delivery › Cover letter builds it."))
    return source + body + built


def _version_report(d, board, job, root, sub):
    s = _pick(sub, VERSION_AR)
    if s == "Questions":
        html = _standing(d, job, root)
    elif s in ("Draft-Main", "Draft-Appendix"):
        part = "main" if s == "Draft-Main" else "appendix"
        rows = [r for r in _version_rows(d, board, job) if r["part"] == part]
        html = pv(P._cards(P._narrative_cards(d, rows), f"No {part} Section in this send."))
    elif s == "Cover letter":
        html = _cover_letter(d, board, job, root)
    else:
        html = _comments(board, job, root)
    return Space(html=html, subspaces=VERSION_AR, open=s, run_types=_run_cards("Job", "Audience Report", s))


def _version_work(d, board, job, root, sub):
    s = _pick(sub, VERSION_WD)
    rows = _version_rows(d, board, job)
    if s == "Letters":                              # the letters are t3N_ Page Tasks; the comments are reports
        from live.frame import ROUTE
        cards = []
        for q in _letter_pages(job):
            h = _header(q)
            tab = ROUTE + "?" + P.urlencode({"path": rel(q.parent, root)})
            cards.append(P._card("letter-" + q.stem, "Letter", q.stem,
                                 "to the editor" if "cover" in q.stem else "to the reviewers" if "respon" in q.stem else "",
                                 "", P._state_word(h.get("state", "")) or h.get("state", "") or "—", "mut",
                                 [("open", link(tab, "the Task tab ↗")), ("face", pop(reader(q, root), q.stem, q.name + " ↗"))]))
        for q in _version_round_pages(board, job):
            h = _header(q)
            cards.append(P._card("comments-" + q.stem, "Comments", q.stem, "the comments a response answers", "",
                                 h.get("state", "") or "open", "mut", [("report", pop(reader(q, root), q.stem, q.name + " ↗"))]))
        html = pv(P._cards(cards, "No letter Task yet: t31_cover-letter (to the editor) and, in a revision, "
                                  "t32_response (to the reviewers), each a Page Task like a Section."))
    elif s == "All":                                # every Section, ✎ Write on each, its Runs and what they found (b10 s32-D19)
        html = work_tree("Job", job, root, THEME) or pv(P._section_table(d, rows))
    else:
        html = pv(P._section_table(d, [r for r in rows if r["part"] == s.lower()]))
    return Space(html=html, subspaces=VERSION_WD, open=s,
                 run_types=_run_cards("Job", "Work Details", None if s == "All" else s))


def version_spaces(job, root, sub):
    """The version tab (s12): a send's Description, Audience Report, Work Details, Runs and Delivery."""
    board = next((q for q in job.parents if (q / "board.md").is_file()), None)
    if board is None:
        return {}
    d = _data(board, root, job)
    # two versions may hold the same Section names (j02 starts as a copy of j01): this tab reads its own
    d = dict(d, sections=[p for p in d["sections"] if p["rel"] and _mine(board, job, p["rel"])])
    if delivery_dir(job).is_dir():                 # on the ladder each version builds its own (g03 D4)
        d = dict(d, delivery=P.delivery_info(d, delivery_dir(job)))
    return _disk_version(d, board, job, {"Description": _version_description(d, board, job, root, sub),
                                         "Audience Report": _version_report(d, board, job, root, sub),
                                         "Work Details": _version_work(d, board, job, root, sub),
                                         "Runs": Space(run_types=_run_cards("Job", "Runs")),
                                         "Delivery": _version_delivery(d, board, job, root)})
