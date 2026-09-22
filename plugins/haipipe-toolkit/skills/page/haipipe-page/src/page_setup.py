"""Semantic Markdown setup for a newly imported standalone Page.

This module deliberately stops short of claiming editorial acceptance.  It
turns the supplied document into reviewable Page records: a specific Opening,
an unapproved Shape, reader-move Bullets, matching candidate prose, backstage
Context records, and one completed delegated setup Run.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import tomllib

from live.outline_preview import bullet_token, read_drafts
from src.plan_shape import iter_plan_bullets


SETUP_MARKER = "setup: semantic-markdown-v1"


@dataclass(frozen=True)
class DraftBullet:
    role: str
    point: str
    draft: str
    source_sentences: int


@dataclass(frozen=True)
class DraftParagraph:
    label: str
    bullets: tuple[DraftBullet, ...]


@dataclass(frozen=True)
class DraftDivision:
    title: str
    paragraphs: tuple[DraftParagraph, ...]


def _split_sections(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    """Read H1/H2 structure without treating headings in fences as structure."""
    title = ""
    sections: list[tuple[str, list[str]]] = []
    current: tuple[str, list[str]] | None = None
    prelude: list[str] = []
    fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if not fence and line.startswith("## "):
            current = (line[3:].strip(), [])
            sections.append(current)
            continue
        (current[1] if current else prelude).append(line)
    if not sections:
        sections = [(title or "Source", prelude)]
    return title, [(heading, "\n".join(lines).strip()) for heading, lines in sections]


def _blocks(markdown: str) -> list[str]:
    """Return prose/list/quote blocks and ignore executable/display fences."""
    blocks: list[str] = []
    buffer: list[str] = []
    fence = False

    def flush():
        if buffer:
            text = "\n".join(buffer).strip()
            if text and text != "---":
                blocks.append(text)
            buffer.clear()

    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            flush()
            fence = not fence
            continue
        if fence:
            continue
        if not line.strip():
            flush()
        else:
            buffer.append(line)
    flush()
    return blocks


def _plain(markdown: str) -> str:
    text = re.sub(r"(?m)^\s*>+\s?", "", markdown)
    text = re.sub(r"(?m)^\s*(?:[-*+] |\d+[.)]\s+)", "", text)
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_~`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _sentences(text: str) -> list[str]:
    """Conservative sentence split suitable for authored English Markdown."""
    protected = text
    substitutions = {
        "e.g.": "e·g·", "i.e.": "i·e·", "et al.": "et al·",
        "Dr.": "Dr·", "Mr.": "Mr·", "Ms.": "Ms·", "Prof.": "Prof·",
    }
    for source, replacement in substitutions.items():
        protected = protected.replace(source, replacement)
    protected = re.sub(r"(?<=\d)\.(?=\d)", "·", protected)
    protected = re.sub(r"(?<=\b[A-Z])\.(?=\s+[A-Z][a-z])", "·", protected)
    boundary = re.compile(r"[.!?。！？](?:[\"”’])?(\s+)(?=[A-Z0-9“‘\"(])")
    pieces, start = [], 0
    for match in boundary.finditer(protected):
        pieces.append(protected[start:match.start(1)])
        start = match.end(1)
    pieces.append(protected[start:])
    restored = [piece.replace("·", ".").strip() for piece in pieces if piece.strip()]
    return restored or ([text] if text else [])


def _role(text: str, heading: str, index: int, count: int, *, quoted: bool = False) -> str:
    lower = text.lower()
    start = lower.lstrip('“\"‘')
    if start.startswith(("for example", "consider ", "an example")):
        return "Example"
    if quoted or text.startswith(("“", '"')) or heading.lower().startswith("voice"):
        return "Voice"
    if any(word in lower for word in ("citation", "evidence", "numerical result", "regression")):
        return "Evidence"
    if start.startswith(("this is why", "this is what")) or "i distinguish" in lower:
        return "Definition"
    if any(phrase in lower for phrase in ("i want", "we want", "should ", "must ", "need to", "has to")):
        return "Requirement"
    if start.startswith(("if ", "when ", "once ", "unless ")):
        return "Condition"
    if any(phrase in lower for phrase in (
        "because ", "therefore", "so that", "this makes", "allows ",
        " prevent ", " prevents ", " causes ", " leads to ",
    )):
        return "Mechanism"
    if any(phrase in lower for phrase in ("problem", "loses", "lost", "wrong", "undo", "repeat")):
        return "Problem"
    if any(phrase in lower for phrase in ("over time", "teach us", "learn", "preference")):
        return "Learning"
    if any(phrase in lower for phrase in ("then ", "next ", "begin ", "return ", "step ", "process")):
        return "Process"
    if "?" in text:
        return "Question"
    # A modal buried in a complement ("how quickly a clinic can offer" or
    # "does not guarantee that a patient can use") does not make the whole
    # reader move a Possibility.  Inspect only the leading/main-clause span.
    modal_span = re.split(r"\b(?:that|how|which|when|because)\b", start, maxsplit=1)[0]
    if re.search(r"\b(?:can|could|may|might)\b", modal_span):
        return "Possibility"
    if index == 0:
        return "Phenomenon"
    if index == count - 1:
        return "Implication"
    return "Principle"


def _point(text: str) -> str:
    """Produce a complete provisional reader move; the full prose stays at right.

    Setup must never manufacture apparent concision by cutting a source clause
    after an arbitrary word count.  The later structure Run may rewrite a long
    provisional head into the stricter 4–11-word house style with semantic
    judgment; deterministic setup preserves the complete clause for that review.
    """
    cleaned = text.strip().strip('“”\"‘’')
    cleaned = re.sub(
        r"^(?:But|And|Then|Now|So|For example|In other words|This is why)\s*[,;:]?\s+",
        "", cleaned, flags=re.I,
    )
    labelled = re.match(r"^([^:]{1,32}):\s+(.+)$", cleaned)
    if labelled and len(labelled.group(1).split()) <= 3:
        cleaned = labelled.group(2)
    # A comma is not a safe deterministic Point boundary: it may join an
    # Oxford-comma list whose final item completes the claim.  Preserve such
    # clauses for semantic OUTLINE review instead of silently clipping them.
    clause = re.split(r"[;:]", cleaned, maxsplit=1)[0].strip()
    return clause.rstrip(".,;:") or "The source paragraph needs a clear reader move"


def _head_sentence(sentences: list[str]) -> str:
    """Choose the sentence that best exposes the paragraph's reader move."""
    def score(item: tuple[int, str]) -> tuple[int, int]:
        index, sentence = item
        lower = sentence.lower().lstrip('“\"\'‘')
        words = sentence.split()
        value = index  # conclusions commonly come late in authored paragraphs
        if any(term in lower for term in (
            " should ", " must ", " need ", " want ", "this is why",
            "therefore", "so that", "means that", "allows ", "cannot ",
        )):
            value += 8
        if any(term in lower for term in ("problem", "otherwise", "instead", "rather than")):
            value += 4
        if lower.startswith(("this ", "that ", "it ", "these ", "those ", "there ")):
            value -= 4
        if lower.startswith(("for example", "consider ", "an example")):
            value -= 6
        if sentence.endswith("?"):
            value -= 3
        if len(words) < 5:
            value -= 5
        return value, -index

    return max(enumerate(sentences), key=score)[1]


def _reader_move(sentences: list[str], heading: str, *, quoted: bool) -> DraftBullet:
    """Map one authored paragraph to its primary logical move.

    Setup deliberately does not mistake sentence boundaries for outline
    boundaries. A non-Section Page Bullet may realize as several sentences;
    an agent later splits only genuinely independent reader moves.
    """
    representative = _head_sentence(sentences)
    draft = " ".join(sentence.strip() for sentence in sentences)
    return DraftBullet(
        _role(draft, heading, 0, 1, quoted=quoted),
        _point(representative),
        draft,
        len(sentences),
    )


def _recorded_source_sentence_count(plan_text: str, previews: dict[str, dict[str, str]]) -> int:
    """Prefer setup provenance over re-tokenizing rendered candidate prose.

    Preview rendering can normalize author separators such as middle dots into
    periods.  Those display changes must not rewrite the source-sentence count
    recorded when the editable Markdown was first analyzed.
    """
    blocks = list(iter_plan_bullets(plan_text)) if plan_text else []
    recorded = [
        int(value)
        for value in re.findall(
            r"(?m)^\s+Note:\s+Maps\s+(\d+)\s+source sentences?\b",
            plan_text,
        )
    ]
    if blocks and len(recorded) == len(blocks):
        return sum(recorded)
    return sum(len(_sentences(item.get("text", ""))) for item in previews.values())


def analyze_markdown(markdown: str, fallback_title: str) -> tuple[str, tuple[DraftDivision, ...]]:
    title, raw_sections = _split_sections(markdown)
    divisions: list[DraftDivision] = []
    for heading, body in raw_sections:
        paragraphs: list[DraftParagraph] = []
        for block in _blocks(body):
            plain = _plain(block)
            sentences = _sentences(plain)
            if not sentences:
                continue
            bullet = _reader_move(sentences, heading, quoted=bool(re.match(r"\s*>", block)))
            paragraphs.append(DraftParagraph(_point(sentences[0]), (bullet,)))
        if paragraphs:
            divisions.append(DraftDivision(heading, tuple(paragraphs)))
    if not divisions:
        raise ValueError("Markdown setup found no prose beneath the document headings")
    return title or fallback_title, tuple(divisions)


def _opening(title: str, divisions: tuple[DraftDivision, ...]) -> str:
    first = divisions[0].title
    last = divisions[-1].title
    middle = next((d.title for d in divisions if "evidence" in d.title.lower()),
                  divisions[len(divisions) // 2].title)
    return (
        f'This Page develops “{title}” around “{first},” connects that opening problem to “{middle},” '
        f'and concludes with “{last}.” The imported Markdown remains the editable Content authority, while '
        "the Outline maps each paragraph-level reader move to a Content Draft for review."
    )


def _face(title: str, content: str, divisions: tuple[DraftDivision, ...]) -> str:
    return (
        f"# {title}\nstate: 🟡 Setup complete; Outline review pending\nowner: unassigned\n"
        f"source-content: {content}\n{SETUP_MARKER}\n\n## Opening\n\n{_opening(title, divisions)}\n\n"
        "## Content\n"
    )


def _plan(stem: str, divisions: tuple[DraftDivision, ...], date: str) -> str:
    first, last = divisions[0].title, divisions[-1].title
    out = [
        f"# {stem} · outline v0.1", "outline-version: v0.1", "supersedes: none",
        f"date: {date}", "approved: ⬜",
        f"arc: The document moves from {first} through its working argument to {last}.", "",
    ]
    paragraph_number = 0
    for ci, division in enumerate(divisions, 1):
        out.append(f"## C{ci} · {division.title}")
        for paragraph in division.paragraphs:
            paragraph_number += 1
            out.append(f"### C{ci}.P{paragraph_number} · {paragraph.label}")
            for bi, bullet in enumerate(paragraph.bullets, 1):
                out.extend([
                    f"- B{bi} · [{bullet.role}] {bullet.point}",
                    f"  Note: Maps {bullet.source_sentences} source sentence{'s' if bullet.source_sentences != 1 else ''}; review the reader move before approval. 🎯 A{ci}.1",
                    "  Evidence: none · source-contained expository move; external support was not assessed during setup.",
                    f"  Draft: {bullet.draft}",
                ])
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def _replace_manifest_title(manifest: Path, title: str) -> None:
    text = manifest.read_text(encoding="utf-8")
    replacement = "title = " + json.dumps(title, ensure_ascii=False)
    if re.search(r"(?m)^title\s*=", text):
        text = re.sub(r"(?m)^title\s*=.*$", replacement, text)
    else:
        text += replacement + "\n"
    manifest.write_text(text, encoding="utf-8")


def _context_files(page, title: str, divisions: tuple[DraftDivision, ...], bullets: int,
                   source_sentences: int, date: str) -> None:
    outline = page.folder / "outline"
    stem = page.source.stem
    context = (
        f"# {stem} · Context\npage: {page.source.name}\nkind: generated setup context\n"
        f"written: {date}\nstatus: 🟡 Shape review pending\n\n"
        "### CTX1 · Purpose\n"
        f"- **Question:** How should “{title}” remain readable while its structure and sentence purposes can be reviewed?\n"
        f"- **Scope:** {len(divisions)} imported sections, {bullets} reader-move Bullets, and {source_sentences} source sentences.\n"
        "- **Boundary:** setup maps existing prose; it does not establish truth, editorial acceptance, or Board membership.\n\n"
        "### CTX2 · Current gate\n"
        "- **State:** the generated v0.1 Shape and Content Draft await human review.\n"
        "- **Next:** revise semantic roles or wording, then explicitly approve Shape before promotion.\n"
    )
    files = (
        f"# {stem} · Files\npage: {page.source.name}\nkind: Page file map\nwritten: {date}\n\n"
        "### F1 · Page Face\n"
        f"- **Path:** {page.source.name}\n- **Role:** Opening and the Page Face binding to imported Content.\n\n"
        "### F2 · Editable Content\n"
        f"- **Path:** {page.content.relative_to(page.folder).as_posix()}\n"
        "- **Role:** imported Markdown and the one content authority for the article.\n\n"
        "### F3 · Shape and Content Draft\n"
        f"- **Path:** outline/{stem}-outline-v0.1.md\n"
        "- **Role:** reader moves and matching Draft prose awaiting review.\n"
    )
    (outline / f"{stem}-context.md").write_text(context, encoding="utf-8")
    (outline / f"{stem}-files.md").write_text(files, encoding="utf-8")


def _setup_run(page, title: str, divisions: int, bullets: int, source_sentences: int,
               input_hash: str,
               *, mode: str, delivery: str, audit) -> str:
    runs = page.folder / "runs"
    results = page.folder / "results"
    runs.mkdir(exist_ok=True)
    results.mkdir(exist_ok=True)
    used = {int(m.group(1)) for path in runs.glob("r*_*")
            if (m := re.match(r"r(\d+)_", path.name))}
    number = next(n for n in range(1, 100) if n not in used)
    run = f"r{number:02d}_page-setup"
    result = results / run
    result.mkdir(exist_ok=False)
    ticket = runs / f"{run}.md"
    ticket.write_text(
        "---\nfamily: page\noperation: page-setup\ninteraction: delegated\n"
        f"target: {page.source.name}\nresult: results/{run}\n---\n\n"
        f"- Goal: Turn “{title}” into a substantive standalone Page setup.\n"
        f"- Mode: {mode}.\n"
        "- Scope: Page-owned source, planning records, workbench inputs, and static delivery.\n"
        "- Success: the existing Page state is preserved, built, and reported; a new Markdown Page also receives semantic draft records.\n",
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    content = (page.content or page.source).relative_to(page.folder).as_posix()
    plan = f"outline/{page.source.stem}-outline-v0.1.md"
    outline = f"outline/{page.source.stem}-outline-v0.1.md"
    check = ("every Outline Bullet has embedded Draft prose and an explicit evidence decision"
             if bullets else "Page build completed; no Shape records were claimed")
    status = "complete" if audit.blocking_passed else "failed"
    action = ("Created semantic records" if mode == "create-semantic-records"
              else "Resumed and rebuilt Page")
    outcome = (f"{action}: {divisions} sections and {bullets} reader-move Bullets; "
               f"mechanical gate {'passed' if audit.blocking_passed else 'failed'}")
    content_hash = sha256((page.folder / content).read_bytes()).hexdigest()
    failure = (None if audit.blocking_passed
               else "blocking setup checklist failed; see report.md")
    (result / "runtime.yaml").write_text(
        f"run: {run}\nfamily: page\noperation: page-setup\ninteraction: delegated\n"
        f"mode: {mode}\n"
        f"target: {page.source.name}\nticket: runs/{run}.md\nresult: results/{run}\n"
        f"outcome: {json.dumps(outcome)}\n"
        f"inputs:\n  - path: {json.dumps(content)}\n    sha256: {content_hash}\n"
        f"status: {status}\nstarted_at: {now}\nfinished_at: {now}\n"
        "worker:\n  kind: skill\n  name: haipipe-page\n"
        f"supersedes: null\nfailure: {json.dumps(failure)}\n",
        encoding="utf-8",
    )
    audit.write_json(result / "checks.json")
    (result / "report.md").write_text(
        f"# Page setup Result · {title}\n\n"
        f"- Input SHA-256: `{input_hash}`\n"
        f"- Page Face: `{page.source.name}`\n"
        f"- Content source: `{content}`\n"
        f"- Shape: `{plan}` ({'present' if (page.folder / plan).is_file() else 'not initialized'}).\n"
        f"- Draft authority: `{outline}` ({'present' if (page.folder / outline).is_file() else 'not initialized'}).\n"
        f"- Coverage: {divisions} sections; {bullets} reader-move Bullets; {source_sentences} source sentences.\n"
        f"- Static delivery: `{delivery}`\n"
        f"- Mechanical gate: **{'PASS' if audit.blocking_passed else 'FAIL'}**.\n"
        f"- Coverage check: {check}.\n"
        f"- Mode: {mode}.\n"
        f"- Run status: **{status}**.\n"
        "- Human gate: Shape/content acceptance remains open.\n\n"
        "Audited artifact fingerprints are recorded in `checks.json`; rerun setup after changing a checked artifact.\n\n"
        "## Setup checklist\n\n"
        f"{audit.markdown()}\n",
        encoding="utf-8",
    )
    return run


def setup_markdown_page(page, *, force: bool = False, input_file: Path | None = None):
    """Populate a freshly imported Markdown Page and return a setup summary."""
    if page.content is None or page.content.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Automatic semantic setup currently requires imported Markdown content")
    existing = page.source.read_text(encoding="utf-8")
    plan_glob = list((page.folder / "outline").glob(f"{page.source.stem}-outline-v*.md")) \
        if (page.folder / "outline").is_dir() else []
    is_scaffold = "Working Page for " in existing or SETUP_MARKER in existing
    fresh_intake = "Working Page for " in existing and not plan_glob
    if (not is_scaffold or plan_glob) and not force:
        raise ValueError("Page already has authored/setup records; use --force only after reviewing what will be replaced")

    markdown = page.content.read_text(encoding="utf-8")
    title, divisions = analyze_markdown(markdown, page.title)
    bullet_count = sum(
        len(paragraph.bullets) for division in divisions for paragraph in division.paragraphs
    )
    source_sentence_count = sum(
        bullet.source_sentences
        for division in divisions
        for paragraph in division.paragraphs
        for bullet in paragraph.bullets
    )
    date = datetime.now().strftime("%y%m%d")
    outline = page.folder / "outline"
    outline.mkdir(exist_ok=True)
    plan = outline / f"{page.source.stem}-outline-v0.1.md"
    if force:
        for old in outline.glob(f"{page.source.stem}-outline-v*.md"):
            old.unlink()
    plan.write_text(_plan(page.source.stem, divisions, date), encoding="utf-8")

    blocks = list(iter_plan_bullets(plan.read_text(encoding="utf-8")))
    drafts = [bullet.draft for division in divisions for paragraph in division.paragraphs
              for bullet in paragraph.bullets]
    if len(blocks) != len(drafts):
        raise ValueError("Generated Shape and Content Draft counts diverged")
    page.source.write_text(_face(title, page.content.relative_to(page.folder).as_posix(), divisions),
                           encoding="utf-8")
    _replace_manifest_title(page.folder / "page.toml", title)
    _context_files(page, title, divisions, bullet_count, source_sentence_count, date)
    input_hash = tomllib.loads((page.folder / "page.toml").read_text(encoding="utf-8")).get(
        "input_sha256", sha256(page.content.read_bytes()).hexdigest())
    from src.page_workspace import build_page, load_page
    current = load_page(page.folder)
    delivery_path = build_page(current)
    delivery = delivery_path.relative_to(current.folder).as_posix()
    from src.page_setup_check import validate_setup
    audit = validate_setup(current, plan=plan, delivery=delivery_path,
                           mode="create-semantic-records", input_hash=input_hash,
                           input_file=input_file, strict_input=fresh_intake)
    run = _setup_run(current, title, len(divisions), bullet_count, source_sentence_count,
                     input_hash,
                     mode="create-semantic-records", delivery=delivery, audit=audit)
    if not audit.blocking_passed:
        raise ValueError(f"setup validation failed; inspect results/{run}/report.md")
    return {"title": title, "divisions": len(divisions),
            "paragraphs": sum(len(d.paragraphs) for d in divisions),
            "bullets": bullet_count, "source_sentences": source_sentence_count,
            "plan": plan.relative_to(page.folder).as_posix(),
            "draft": f"outline/{page.source.stem}-outline-v0.1.md", "run": run,
            "delivery": delivery, "mode": "create-semantic-records",
            "checks": audit.as_dict()["summary"], "blocking_gate": "pass"}


def _existing_setup(page, *, input_file: Path | None = None):
    """Build an existing Page without overwriting its human-owned records."""
    from src.outline_version import latest_outline, version_tag
    from src.page_workspace import build_page

    plan = latest_outline(page.folder / "outline", page.source.stem)
    drafts = read_drafts(page.source)
    divisions = paragraphs = bullets = 0
    plan_text = ""
    if plan is not None:
        plan_text = plan.read_text(encoding="utf-8")
        divisions = len(re.findall(r"(?m)^## C\d+\s*·", plan_text))
        paragraphs = len(re.findall(r"(?m)^### C\d+\.P\d+\s*·", plan_text))
        blocks = list(iter_plan_bullets(plan_text))
        bullets = len(blocks)
        # A reviewed head/role correction keeps the same realization and stable
        # address. Setup rebinds that exact map; structural changes still fail
        # coverage and require explicit preview reconciliation.
    source_sentences = _recorded_source_sentence_count(plan_text, drafts)
    manifest = tomllib.loads((page.folder / "page.toml").read_text(encoding="utf-8")) \
        if (page.folder / "page.toml").is_file() else {}
    input_hash = manifest.get(
        "input_sha256", sha256((page.content or page.source).read_bytes()).hexdigest())
    delivery_path = build_page(page)
    delivery = delivery_path.relative_to(page.folder).as_posix()
    from src.page_setup_check import validate_setup
    audit = validate_setup(page, plan=plan, delivery=delivery_path,
                           mode="resume-and-build", input_hash=input_hash,
                           input_file=input_file)
    run = _setup_run(page, page.title, divisions, bullets, source_sentences, input_hash,
                     mode="resume-and-build", delivery=delivery, audit=audit)
    if not audit.blocking_passed:
        raise ValueError(f"setup validation failed; inspect results/{run}/report.md")
    return {"title": page.title, "divisions": divisions, "paragraphs": paragraphs,
            "bullets": bullets, "source_sentences": source_sentences,
            "plan": plan.relative_to(page.folder).as_posix() if plan else None,
            "draft": plan.relative_to(page.folder).as_posix() if drafts else None,
            "run": run, "delivery": delivery, "mode": "resume-and-build",
            "checks": audit.as_dict()["summary"], "blocking_gate": "pass"}


def run_setup(page, *, force: bool = False, input_file: Path | None = None):
    """One setup door: initialize a scaffold, or safely resume an existing Page."""
    face = page.source.read_text(encoding="utf-8")
    outline = page.folder / "outline"
    plans = list(outline.glob(f"{page.source.stem}-outline-v*.md")) if outline.is_dir() else []
    scaffold = "Working Page for " in face
    if force or (scaffold and not plans):
        return setup_markdown_page(page, force=force, input_file=input_file)
    return _existing_setup(page, input_file=input_file)
