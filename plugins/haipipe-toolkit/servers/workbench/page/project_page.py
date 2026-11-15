"""The Project page's parts, under one name for focus_page (`from live import project_page as PP`): the Project's
face in project_face.py, the Findings band in project_findings.py. Each name loads on first use, so importing this
file never pulls focus_page in mid-load."""
from importlib import import_module

FACE = (
    "theme_report",
    "SECTION_ICONS",
    "section_icon",
    "own_face",
    "face_sections",
    "PAGE_TOP",
    "FACE_ICONS",
    "face_yaml",
    "face_lead",
    "_inline",
    "_project_path",
    "_dotted",
    "_load",
    "receipt_source",
    "RUN_SOURCE",
    "block_run_source",
    "run_badge",
    "prediction_card",
    "funnel_view",
    "decisions_list",
    "terms_list",
    "FACE_KINDS",
    "project_top",
    "FIND_CSS_TOP",
    "FACE_CSS",
    "mindmap_view",
)
FINDINGS = (
    "find_part_document",
    "data_stores",
    "store_count",
    "DATA_CSS",
    "data_section",
    "VERSION_DIR",
    "fn_file",
    "FN_CSS",
    "fn_panel",
    "fn_found",
    "fn_sections",
    "work_findings",
    "findings_parts",
    "FIND_ROW_JS",
    "FIND_ROW_CSS",
    "findings_band",
)
__all__ = [*FACE, *FINDINGS]


def __getattr__(name: str):
    if name in FACE or name in FINDINGS:
        return getattr(import_module("live.project_face" if name in FACE else "live.project_findings"), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
