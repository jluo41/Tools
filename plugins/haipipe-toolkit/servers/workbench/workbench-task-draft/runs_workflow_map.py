"""The Workflow map in the Run Space: which Page Run Spec reads and writes
which Space (moved verbatim from runs.py).
"""
from __future__ import annotations

import html
from pathlib import Path

from src.outline_version import plan_dir


def _workflow_map_rows(page_src: Path) -> list[tuple[str, str, list[tuple[str, str, str]]]]:
    """Return the small Page Run Spec × Space definition map.

    This is deliberately a definition projection, not a second Run inventory.
    Run Spec rows are stable; the paths are parameterized by the current Page
    stem so the same view works for every file-backed Page.
    """
    stem = page_src.stem
    folder = plan_dir(page_src.parent).name
    outline = f"{folder}/{stem}-{'draft' if folder == 'draft' else 'outline'}-v*.md"
    evidence_items = f"{folder}/{stem}-evidence-items.md"
    product = f"{stem}.md"
    return [
        (
            "structure",
            "Page.interactive-writing.structure",
            [
                ("action", "OutlinePlan", outline),
                ("review", "EvidenceItemPlan", evidence_items),
                ("run", "StructureRun", "runs/rp-struct-*.md + results/rp-struct-*/"),
                ("—", "—", "—"),
            ],
        ),
        (
            "scratch",
            "Page.interactive-writing.scratch",
            [
                ("input", "ScratchNote", f"{outline}#Scratch"),
                ("—", "—", "—"),
                ("run", "ScratchResult", "runs/rp-scratch-* + results/rp-scratch-*/"),
                ("—", "—", "—"),
            ],
        ),
        (
            "revise",
            "Page.interactive-writing.revise",
            [
                ("input", "TwoTexts", "results/rp-*/vNNN.md ×2 · or delivery/web/<page>.md ×2"),
                ("—", "—", "—"),
                ("run", "ChangeLedger", "runs/rp-revise-* + results/rp-revise-*/"),
                ("—", "—", "—"),
            ],
        ),
        (
            "section-writing",
            "Page.interactive-writing.section",
            [
                ("review", "WritingResult", outline),
                ("review", "EvidenceBinding", "results/re-*/result.yaml"),
                ("run", "SectionWritingRun", "runs/rp-sec-*.md + results/rp-sec-*/"),
                ("read", "PageDraft", product),
            ],
        ),
        (
            "paragraph-writing",
            "Page.interactive-writing.paragraph",
            [
                ("review", "WritingResult", outline),
                ("review", "EvidenceBinding", "results/re-*/result.yaml"),
                ("run", "ParagraphWritingRun", "runs/rp-para-*.md + results/rp-para-*/"),
                ("read", "PageDraft", product),
            ],
        ),
        (
            "evidence-item",
            "Page.evidence-item",
            [
                ("review", "EvidenceBinding", evidence_items),
                ("action", "EvidenceResult", "results/re-{value,display,cite}-*/result.yaml"),
                ("run", "EvidenceRun", "runs/re-*.md + results/re-*/"),
                ("review", "ArtifactDependency", "delivery/<lane>/ built files"),
            ],
        ),
        (
            "delivery",
            "Page.delivery",
            [
                ("read", "PageSource", product),
                ("read", "EvidenceResult", "results/re-*/result.yaml"),
                ("run", "DeliveryRun", "runs/rd*.md + results/rd*/"),
                ("write", "DeliveryArtifact", "delivery/{web,latex,word,render}/"),
            ],
        ),
    ]


def _workflow_map_cell(mode: str, schema: str, path: str) -> str:
    """Render one compact, copy-friendly cell in the map grid."""
    if mode == "—":
        return '<div class="workflow-map-cell workflow-map-empty" role=cell>—</div>'
    return (
        '<div class=workflow-map-cell role=cell>'
        '<span class=workflow-map-mode>%s</span>'
        '<span class=workflow-map-schema>%s</span>'
        '<code class=workflow-map-path>%s</code></div>' % (
            html.escape(mode), html.escape(schema), html.escape(path)
        )
    )


def _workflow_map_html(page_src: Path) -> str:
    """Render the reader-facing Workflow × Space specification."""
    headers = (
        ("Run Spec", ""),
        ("Draft", "draft"),
        ("Evidence", "evidence"),
        ("Run", "runtime"),
        ("Delivery", "delivery"),
    )
    header_html = []
    for label, internal in headers:
        suffix = f" <code>{internal}</code>" if internal and internal != label.lower() else ""
        header_html.append(
            '<div class="workflow-map-cell workflow-map-head" role=columnheader>%s%s</div>' %
            (html.escape(label), suffix)
        )
    rows_html = []
    for spec_id, run_type, cells in _workflow_map_rows(page_src):
        cells_html = [
            '<div class="workflow-map-cell workflow-map-spec" role=rowheader>%s<code>%s</code></div>' %
            (html.escape(spec_id), html.escape(run_type))
        ]
        cells_html.extend(_workflow_map_cell(*cell) for cell in cells)
        rows_html.append('<div class=workflow-map-row role=row>%s</div>' % "".join(cells_html))
    return (
        '<p class=workflow-map-note>Rows are planned Run Specs; columns are Spaces. '
        'Each cell shows <code>mode · schema · path</code>. This map is read-only; '
        'the concrete Runs remain in the other Run Space tabs. Context collection, '
        'Content adoption, and whole-Page Check are controller operations. '
        'Check reviews Draft, Evidence, Run records, and Delivery together.</p>'
        '<div class=workflow-map-viewport><div class=workflow-map-grid role=table '
        'aria-label="Workflow by Space specification">%s%s</div></div>' %
        ("".join(header_html), "".join(rows_html))
    )
