"""venue_jama.py: the JAMA Internal Medicine layout: its title page, Key Points, abstract and supplement (build_jama_internal_medicine).
latex_room_to_docx.py runs this file inside its own namespace (_load_part), so the config and the Word helpers come from there."""
from __future__ import annotations

import re
from pathlib import Path


def labelled_blocks(doc: Document, heading: str, block: str) -> None:
    """Render JAMA Key Points or a structured abstract from labelled TeX prose."""
    add_heading(doc, heading, 1)
    labels = list(re.finditer(r"\\noindent\s*\\textbf\s*\{([^{}]+)\}", block))
    if not labels:
        add_text(doc, latex_to_text(block))
        return
    for index, match in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(block)
        paragraph = doc.add_paragraph(style="Normal")
        paragraph.paragraph_format.line_spacing = 2.0
        paragraph.paragraph_format.space_after = Pt(0)
        label_run = paragraph.add_run(latex_to_text(match.group(1)) + " ")
        body_run = paragraph.add_run(latex_to_text(block[match.end():end]))
        set_font(label_run, size=12, bold=True)
        set_font(body_run, size=12)


def extract_jama_title(center_block: str) -> tuple[str, str]:
    """Read the title and blinded-author line from JAMA's source-owned title block."""
    title_part = center_block.split(r"\vspace", 1)[0]
    title_part = re.sub(r"\\(?:begin|end)\{center\}", "", title_part)
    title_part = re.sub(r"\\(?:Large|large|bfseries)\b", "", title_part)
    title = latex_to_text(title_part.replace(r"\\", " "))
    author_match = re.search(r"\vspace\{[^}]+\}\s*(.*?)\s*\vspace", center_block, re.S)
    author = latex_to_text(author_match.group(1).strip()) if author_match else ""
    return title, author


def jama_parts(raw_master: str) -> tuple[str, str, str, str, str, str]:
    """Split a JAMA IM desk room without requiring a generic abstract environment."""
    body = clean_fragment(raw_master, MASTER.parent, remove_abstract=False)
    register_labels(body)
    body = body.split(r"\begin{document}", 1)[-1].split(r"\end{document}", 1)[0]
    center_match = CENTER_PATTERN.search(body)
    if center_match is None:
        raise RuntimeError("JAMA IM source is missing its title-page center block")
    title, author = extract_jama_title(center_match.group(0))

    key_match = re.search(r"\\section\*\{Key Points\}(.*?)\\section\*\{Abstract\}", body, re.S)
    abstract_match = re.search(r"\\section\*\{Abstract\}(.*?)\\section\s*\{Introduction\}", body, re.S)
    bib_match = re.search(r"\\bibliography\s*\{", body)
    appendix_match = re.search(r"\\appendix\b", body)
    # 0.12.3: a Research Letter has no Key Points and no Abstract; the text then starts at its Introduction
    if bib_match is None or appendix_match is None:
        raise RuntimeError("JAMA IM source is missing its bibliography or appendix boundary")
    if abstract_match is None and re.search(r"\\section\*\{Abstract\}", body):
        raise RuntimeError("JAMA IM source has an Abstract heading but no Introduction after it")
    key_points = key_match.group(1) if key_match else ""
    abstract = abstract_match.group(1) if abstract_match else ""
    intro = re.search(r"\\section\s*\{Introduction\}", body)
    if intro is None:
        raise RuntimeError("JAMA IM source is missing Introduction")
    main_text = body[intro.start():bib_match.start()]
    # A desk whose opening is not headed Abstract (Lancet: Summary, then the Research in context panel) keeps every
    # numbered section after its heading: the abstract ends at the first \section, and the main text starts there.
    head = str(PROFILE_CONFIG.get("abstract_heading", "Abstract"))
    head_match = None if abstract_match else re.search(r"\\section\*\{" + re.escape(head) + r"\}", body)
    if head_match:
        nxt = re.search(r"\\section\s*\{", body[head_match.end():])
        if nxt is not None and head_match.end() + nxt.start() <= intro.start():
            start = head_match.end() + nxt.start()
            abstract, main_text = body[head_match.end():start], body[start:bib_match.start()]
    supplement_text = body[appendix_match.end():]
    return title, author, key_points, abstract, main_text, supplement_text


def add_byline(doc: Document, latex: str) -> None:
    """[paper] authors (LaTeX: lines split by \\\\, affiliation marks in \\textsuperscript) as centred lines: the
    names at body size, the affiliations a size smaller, each mark set as a superscript."""
    text = re.sub(r"\\\\(\[[^\]]*\])?", "\n", latex)
    text = re.sub(r"\\(small|footnotesize|normalsize)\b", "", text)
    for i, line in enumerate(l.strip() for l in text.split("\n")):
        if not line.strip("{} "):
            continue
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.line_spacing = 1.15
        paragraph.paragraph_format.space_after = Pt(2 if i else 8)
        for k, part in enumerate(re.split(r"\\textsuperscript\{([^}]*)\}", line)):
            part = part.replace("{", "").replace("}", "")
            if part:
                run = paragraph.add_run(part)
                set_font(run, size=12 if i == 0 else 10)
                run.font.superscript = bool(k % 2)


def add_jama_title_page(doc: Document, title: str, author: str, main_words: int,
                        table_count: int, figure_count: int, evidence: dict[str, object]) -> None:
    """Venue-only title packaging; all study-specific text remains in the room source."""
    add_text(doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    if (str(evidence.get("mode", "draft")) not in {"final", "submission", "submission-ready"}
            and PROFILE_CONFIG.get("status_header", True)):
        add_text(doc, str(PROFILE_CONFIG.get("draft_label", "DRAFT — NOT SUBMISSION READY")),
                 align=WD_ALIGN_PARAGRAPH.CENTER)
    if author:
        add_text(doc, author, align=WD_ALIGN_PARAGRAPH.CENTER)
    elif str(PAPER_CONFIG.get("authors", "")).strip():
        add_byline(doc, str(PAPER_CONFIG["authors"]))   # JL 261023: the Word title page printed no authors
    add_text(doc, str(PROFILE_CONFIG.get("venue_label", "JAMA Internal Medicine")),
             align=WD_ALIGN_PARAGRAPH.CENTER)
    date = str(PROFILE_CONFIG.get("document_date", "")).strip()
    if date:
        add_text(doc, date, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(doc, f"Word count: {main_words}", align=WD_ALIGN_PARAGRAPH.CENTER)
    plural = lambda n, word: f"{n} {word}" + ("" if n == 1 else "s")   # "1 table", never "1 tables" (JL 261028)
    add_text(doc, f"Main displays: {plural(table_count, 'table')}; {plural(figure_count, 'figure')}",
             align=WD_ALIGN_PARAGRAPH.CENTER)
    if evidence.get("pending_markers"):
        add_text(doc, "Evidence placeholders remain; this build is not submission-ready.",
                 align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()


def build_jama_internal_medicine(raw_master: str, evidence: dict[str, object]) -> tuple[Path, Path]:
    """JAMA IM is a venue profile, not a paper-specific renderer."""
    title, author, key_points, abstract, main_text, supplement_text = jama_parts(raw_master)
    main_events, main_displays = parse_events(main_text)
    supplement_events, _ = parse_events(supplement_text)
    missing = [key for key in CITATION_NUMBERS if key not in BIB]
    if missing:
        raise RuntimeError(f"Citations missing from reference.bib: {missing}")
    main_tables = [display for display in main_displays if display.kind == "table"]
    main_figures = [display for display in main_displays if display.kind == "figure"]
    MAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUPP_PATH.parent.mkdir(parents=True, exist_ok=True)

    main_doc = Document()
    configure_document(main_doc)
    add_jama_title_page(main_doc, title, author, word_count(main_events), len(main_tables), len(main_figures), evidence)
    if key_points:
        labelled_blocks(main_doc, str(PROFILE_CONFIG.get("key_points_heading", "KEY POINTS")), key_points)
    if key_points and bool(PROFILE_CONFIG.get("abstract_new_page", False)):   # the Abstract starts a page (JL 261023)
        main_doc.add_page_break()
    if abstract:
        labelled_blocks(main_doc, str(PROFILE_CONFIG.get("abstract_heading", "ABSTRACT")), abstract)
    if abstract and bool(PROFILE_CONFIG.get("abstract_own_page", False)):   # the text starts on a new page after the keywords (JL 261023)
        main_doc.add_page_break()
    include = bool(PROFILE_CONFIG.get("include_main_displays", False))
    at_end = bool(PROFILE_CONFIG.get("main_displays_at_end", False))   # JAMA: tables, then figures, after the references
    add_events(main_doc, main_events, include_displays=include and not at_end, number_displays=True, main_numbering=True)
    add_references(main_doc)
    if include and at_end:
        for kind, adder, prefix in (("table", add_table, PROFILE_CONFIG.get("main_table_prefix", "Table ")),
                                    ("figure", add_figure, PROFILE_CONFIG.get("main_figure_prefix", "Figure "))):
            for number, display in enumerate([d for d in main_displays if d.kind == kind], start=1):
                main_doc.add_page_break()
                adder(main_doc, display, f"{prefix}{number}")
    save_docx(main_doc, MAIN_PATH)

    if not supplement_events:   # 0.12.3: no supplement (a Research Letter): none written, a stale one removed
        for stale in (SUPP_PATH, SUPP_PDF_PATH):
            if stale.exists():
                stale.unlink()
        pdf_report = render_submission_pdfs()
        write_common_receipts(main_events, main_displays, supplement_events, title, evidence, pdf_report)
        return MAIN_PATH, SUPP_PATH

    supp_doc = Document()
    configure_document(supp_doc, body_size=11, line_spacing=1.5)
    add_text(supp_doc, title, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(supp_doc, str(PROFILE_CONFIG.get("supplement_title", "ONLINE-ONLY SUPPLEMENTAL MATERIAL")),
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    if PROFILE_CONFIG.get("supplement_contents", False):   # JAMA: every element and its title on the first page
        add_supplement_contents(supp_doc, supplement_events)
    supp_doc.add_page_break()
    # numbered as the LaTeX lane numbers them, in source order: eTable 1, eFigure 1 (the profile's prefixes). Without
    # number_displays a caption printed with no label (pp-LBP-JAMA 261103)
    add_events(supp_doc, supplement_events, include_displays=True, compact=True, number_displays=True,
               heading_upper=bool(PROFILE_CONFIG.get("supplement_heading_upper", True)))
    if PROFILE_CONFIG.get("supplement_font"):
        restyle_runs(supp_doc, str(PROFILE_CONFIG["supplement_font"]), float(PROFILE_CONFIG.get("supplement_body_size", 10)))
    save_docx(supp_doc, SUPP_PATH)

    pdf_report = render_submission_pdfs()
    write_common_receipts(main_events, main_displays, supplement_events, title, evidence, pdf_report)
    return MAIN_PATH, SUPP_PATH
