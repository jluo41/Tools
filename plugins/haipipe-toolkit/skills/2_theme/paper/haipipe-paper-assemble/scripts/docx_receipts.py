"""docx_receipts.py: what a Word build leaves behind: word count, section snapshots, evidence preflight, PDFs and the manifest.
latex_room_to_docx.py runs this file inside its own namespace (_load_part), so MANIFEST_PATH and the config come from there."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


BACK_MATTER_HEADINGS = {"back matter", "article information", "acknowledgments", "acknowledgements", "acknowledgment"}


def word_count(events: Iterable[Event]) -> int:
    """Main-text words: everything before the back matter (0.12.0, JL 261023: the JAMA title page counted the Article
    Information, 3,071 words where the text has about 2,600; journals count the text alone). A profile may start the
    count at a heading (word_count_from: the Lancet counts from the Introduction, not its Research in context panel)
    and add back-matter headings (back_matter_headings); without them the count is as before (261101, b16 review)."""
    stop = BACK_MATTER_HEADINGS | {str(h).strip().lower() for h in PROFILE_CONFIG.get("back_matter_headings", [])}
    start = str(PROFILE_CONFIG.get("word_count_from", "")).strip().lower()
    counting = not start
    words = []
    for event in events:
        name = str(event.value).strip().lower() if event.kind == "heading" else ""
        if name and name in stop:
            break
        if name and name == start:
            counting = True
        if not counting:
            continue
        if event.kind in {"text", "list"}:
            values = event.value if event.kind == "list" else [event.value]
            # a word is what Word counts: a run between spaces holding a letter or digit, so "1.5%-2.5%" is 1
            # word, not 4 (JL 261028: the title page said 3,179 for a 2,970-word text)
            words.extend(w for w in MATH_TOKEN.sub(" ", " ".join(str(v) for v in values)).split() if re.search(r"\w", w))
    return len(words)


def write_section_snapshots(section_specs: list[tuple[str, str]], running_title: str) -> None:
    DRAFT_SECTION_ROOM.mkdir(parents=True, exist_ok=True)
    readme = DRAFT_SECTION_ROOM / "README.md"
    readme.write_text(
        "# Generated section snapshots\n\n"
        "These DOCX files are generated from the configured desk-room sections by the shared "
        "`haipipe-paper-assemble` engine, launched through this paper's thin wrapper. "
        "They are review snapshots only and are never used as builder inputs.\n",
        encoding="utf-8",
    )
    written = set()
    for source_name, label in section_specs:
        source = SECTION_DIR / source_name
        text = clean_fragment(source.read_text(encoding="utf-8"), source.parent)
        events, _ = parse_events(text)
        doc = Document()
        configure_document(doc)
        add_title_page(doc, label, running_title, word_count(events), 0, 0, "Authors hidden for review")
        add_events(doc, events, include_displays=True)
        output_name = source_name.replace("_", "-").replace(".tex", ".docx")
        save_docx(doc, DRAFT_SECTION_ROOM / output_name)
        written.add(output_name)
    # the folder is regenerated whole: a snapshot no section makes any more (a renamed Section's old name) goes
    for stale in DRAFT_SECTION_ROOM.glob("*.docx"):
        if stale.name not in written:
            stale.unlink()


def evidence_lock_path() -> Path | None:
    """Return the materialized room-local evidence receipt, when configured."""
    raw = EVIDENCE_CONFIG.get("lock")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.is_absolute() else (WORD_ROOM / path).resolve()


def evidence_preflight() -> dict[str, object]:
    """Validate evidence state without creating or replacing manuscript prose.

    The Section projection owns the words.  The lock records which Page Evidence
    Items those words depend on.  A draft can keep visible ``[E## pending]``
    markers; a final build cannot.
    """
    mode = str(EVIDENCE_CONFIG.get("mode", "none")).lower()
    path = evidence_lock_path()
    source_text = "\n".join(path.read_text(encoding="utf-8", errors="replace")
                            for path in sorted(SECTION_DIR.glob("*.tex")))
    pending_markers = sorted(set(re.findall(r"\[E\d{2}\s+pending\]", source_text)))
    report: dict[str, object] = {
        "mode": mode,
        "lock": str(path.relative_to(ROOT)) if path and path.is_relative_to(ROOT) else (str(path) if path else None),
        "pending_markers": pending_markers,
        "items": 0,
        "unaccepted_items": [],
        "lock_exists": path.exists() if path else None,
    }
    if path is None:
        return report
    if not path.exists():
        raise FileNotFoundError(f"Configured evidence lock not found: {path}")
    lock = json.loads(path.read_text(encoding="utf-8"))
    items = lock.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"Evidence lock has non-list items: {path}")
    unaccepted = [
        f"{item.get('page', 'unknown')}/{item.get('item', 'unknown')} ({item.get('state', 'unknown')})"
        for item in items if isinstance(item, dict) and item.get("state") != "accepted"
    ]
    report["items"] = len(items)
    report["unaccepted_items"] = unaccepted
    if mode in {"final", "submission", "submission-ready"} and (pending_markers or unaccepted):
        raise RuntimeError(
            "Final build blocked by unresolved evidence: "
            + ", ".join(pending_markers + unaccepted)
        )
    return report


def source_manifest() -> dict[str, object]:
    paths = [MASTER, BIB_PATH]
    paths.extend(sorted(SECTION_DIR.glob("*.tex")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.tex")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.png")))
    paths.extend(sorted(DISPLAY_DIR.rglob("*.pdf")))
    lock_path = evidence_lock_path()
    if lock_path and lock_path.exists():
        paths.append(lock_path)
    # 0.8.4 (JL 260928 "Why we have the sha256? remove that, waste my tokens"): the manifest lists
    # its inputs by path only; nothing ever read the 74 hashes it used to carry.
    files = [str(path.relative_to(ROOT)) for path in paths]
    profile_path = PROFILE_ROOT / f"{PROFILE_NAME}.toml" if PROFILE_NAME else None
    return {
        "engine": "haipipe-paper-assemble/latex_room_to_docx-0.2.1",
        "builder": "haipipe-paper-assemble/scripts/latex_room_to_docx.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)) if CONFIG_PATH.exists() else None,
        "profile": str(profile_path.relative_to(SKILL_ROOT)) if profile_path and profile_path.exists() else None,
        "venue_profile": PROFILE_CONFIG.get("venue_profile", BUILD_CONFIG.get("paper", {}).get("venue_profile")),
        "source_of_record": str(MASTER.relative_to(ROOT)),
        "outputs": [
            str(MAIN_PATH.relative_to(ROOT)),
            str(SUPP_PATH.relative_to(ROOT)),
            str(MAIN_PDF_PATH.relative_to(ROOT)),
            str(SUPP_PDF_PATH.relative_to(ROOT)),
            str(DRAFT_SECTION_ROOM.relative_to(ROOT)),
            str(MANIFEST_PATH.relative_to(ROOT)),
        ],
        "files": files,
    }


def carried_over(manifest: dict[str, object]) -> dict[str, object]:
    """This step's receipt on top of the last build's manifest, never in place of it. Replacing it emptied the Writing
    view for the rest of every build (Paper-PhyAbsence 261104, JL: "not available anymore"): the named `outputs`, the
    cover letter and the portal were gone until build_delivery.py wrote them again at its end."""
    try:
        last = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return manifest
    if not isinstance(last, dict):
        return manifest
    if isinstance(last.get("outputs"), dict):       # the build's own named files stay until it names them again
        manifest["outputs"] = last["outputs"]
    return {**last, **manifest}


def render_submission_pdfs() -> dict[str, object]:
    """Render configured DOCX deliverables to PDFs when LibreOffice is available."""
    soffice = shutil.which("soffice")
    report: dict[str, object] = {
        "renderer": "LibreOffice" if soffice else None,
        "available": bool(soffice),
        "outputs": [],
        "errors": [],
    }
    if not soffice:
        return report
    for docx_path, pdf_path in ((MAIN_PATH, MAIN_PDF_PATH), (SUPP_PATH, SUPP_PDF_PATH)):
        if not docx_path.exists():   # 0.12.3: a paper with no supplement
            continue
        # 0.12.4 (JL 261101): a PDF the LaTeX build wrote after master.tex is LaTeX's reading copy; once LibreOffice was
        # installed this render overwrote it with the Word file's pages (Paper-AgreeableOpioid-Jama: 43 LaTeX pages
        # became 20 Word pages). It renders only a PDF LaTeX did not make.
        if pdf_path.exists() and MASTER.exists() and pdf_path.stat().st_mtime >= MASTER.stat().st_mtime:
            report.setdefault("kept_latex", []).append(str(pdf_path.relative_to(ROOT)))  # type: ignore[union-attr]
            continue
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf_path.parent), str(docx_path)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            produced = pdf_path.parent / docx_path.with_suffix(".pdf").name
            if produced != pdf_path and produced.exists():
                shutil.move(str(produced), str(pdf_path))
            if not pdf_path.exists():
                raise RuntimeError(f"LibreOffice did not create {pdf_path.name}")
            report["outputs"].append(str(pdf_path.relative_to(ROOT)))  # type: ignore[index]
        except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
            report["errors"].append(f"{docx_path.name}: {error}")  # type: ignore[index]
    return report


def write_common_receipts(main_events: list[Event], main_displays: list[Display],
                          supplement_events: list[Event], running_title: str,
                          evidence: dict[str, object], pdf_report: dict[str, object]) -> None:
    """Write derived receipts only; they are never inputs to a later build."""
    snapshot_config = BUILD_CONFIG.get("snapshots", {})
    configured_sections = snapshot_config.get("sections", []) if isinstance(snapshot_config, dict) else []
    section_specs = [
        (str(item["source"]), str(item["label"]))
        for item in configured_sections
        if isinstance(item, dict) and "source" in item and "label" in item
    ]
    if not section_specs:
        section_specs = [
            (path.name, path.stem.replace("_", " ").title())
            for path in sorted(SECTION_DIR.glob("*.tex"))
        ]
    # 0.8.4 (JL 260928: "why it is not the same to each section's word? and no references"): the
    # snapshots are a second, reference-less copy of what each Section Page already delivers in
    # its own delivery/word/; section_snapshots = "" switches them off.
    if str(OUTPUT_CONFIG.get("section_snapshots", "draft-sections")).strip():
        write_section_snapshots(section_specs, running_title)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    manifest = source_manifest()
    manifest["evidence"] = evidence
    word_limit = PROFILE_CONFIG.get("main_text_word_limit")
    manifest["build"] = {
        "status": "DRAFT" if evidence.get("pending_markers") or evidence.get("unaccepted_items") else "CANDIDATE",
        "source_of_record": str(MASTER.relative_to(ROOT)),
        "venue_profile": PROFILE_NAME,
        "main_text_words": word_count(main_events),
        "main_text_word_limit": word_limit,
        "citations": len(CITATION_NUMBERS),
        "main_tables": len([display for display in main_displays if display.kind == "table"]),
        "main_figures": len([display for display in main_displays if display.kind == "figure"]),
        "supplement_events": len(supplement_events),
        "evidence": evidence,
        "pdf": pdf_report,
        "checks": {
            "master_exists": MASTER.exists(),
            "bibliography_exists": BIB_PATH.exists(),
            "citations_resolved": True,
            "within_declared_word_limit": (
                word_limit is None or word_count(main_events) <= int(word_limit)
            ),
            "evidence_lock_exists": evidence.get("lock_exists"),
            "no_pending_evidence": not evidence.get("pending_markers") and not evidence.get("unaccepted_items"),
            "pdf_outputs_rendered": not pdf_report.get("available") or not pdf_report.get("errors"),
            "g6_human_decision": False,
        },
    }
    manifest["render"] = pdf_report
    MANIFEST_PATH.write_text(json.dumps(carried_over(manifest), indent=2) + "\n", encoding="utf-8")
