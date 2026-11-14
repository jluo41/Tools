"""Outline's minimal, Result-first Evidence Space.

The live surface is grouped by Evidence type and reads only
``results/*/result.yaml``. Each item is a collapsed, read-only summary whose
details distinguish the Evidence Label, Evidence Item, Evidence Run, and
Supporting Runs. Retired Outline Evidence files are never an input or
fallback; their presence is reported as a migration blocker. This module
presents only and never executes a Run.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys
from urllib.parse import quote

from src.outline_version import plan_dir
from src.evidence_labels import parse_result_labels
from src.item_table import (readable_global_run, readable_paper_route, short_name,
                            readable_task, wall_label)


# The parts of this module live in their own files; every name still answers here.
from live.evidence_css import (  # noqa: F401
    _CSS,
)
from live.evidence_text import (  # noqa: F401
    _FIELD, _ITEM_HEADING, _inline_lite, _md_lite,
)
from live.evidence_items import (  # noqa: F401
    _evidence_cards, _evidence_snapshot, _item_card, _local_run_chip, _plan_chips, _run_chips,
)
from live.evidence_bindings import (  # noqa: F401
    _MARKDOWN_LINK, _RUN_BINDING_HEADING, _human_run_name, _lineage_chip, _run_binding, _run_binding_card,
    _run_binding_cards, _run_binding_snapshot, _run_detail, _run_popover, _safe_run_href, _survey_sentence,
    _with_evidence_context,
)
from live.evidence_related import (  # noqa: F401
    _authored_support, _record_context, _related_run_card, _related_run_cards, _related_runs, _run_key,
    _support_family,
)
from live.evidence_results import (  # noqa: F401
    _RESULT_ITEM, _detail_row, _document_text, _evidence_blockers, _evidence_inventory, _evidence_run_contract,
    _evidence_type, _result_document, _result_records, _status_parts, _supporting_run_ids, _top_field,
)
from live.evidence_prompt import (  # noqa: F401
    _copy_prompt_button, _evidence_copy_prompt, _label_details, _label_summary,
)
from live.evidence_sections import (  # noqa: F401
    _evidence_sections, _workspace_actions,
)

# evidence_preview reads _evidence_type and _md_lite back from this module, so it loads after them.
from live.evidence_preview import (  # noqa: F401  (moved; names kept importable here)
    _PREVIEW_IMAGE_SUFFIXES, _PREVIEW_PATH_KEYS, _PREVIEW_COPY_KEYS,
    _PREVIEW_SUFFIX_ORDER, _payload, _preview_scalar, _find_preview_scalar,
    _preview_label, _value_preview_label, _value_preview_rows, _value_preview_table,
    _preview_facts, _preview_table, _payload_table, _preview_texts,
    _preview_path_hints, _safe_preview_file, _preview_artifact, _render_delimited,
    _preview_asset_data, _render_preview_artifact, _result_preview)


def _retired_evidence_paths(page_home: pathlib.Path) -> list[str]:
    """Return only the presence of retired Evidence paths, never their content."""
    outline = plan_dir(page_home)
    found = []
    if outline.is_dir():
        found.extend(sorted(
            path.relative_to(page_home).as_posix()
            for path in outline.glob("*-evidence.md")
            if path.is_file() or path.is_symlink()
        ))
        retired_folder = outline / "evidence"
        if retired_folder.exists() or retired_folder.is_symlink():
            found.append(retired_folder.relative_to(page_home).as_posix())
    return found


def _migration_notice(page_home: pathlib.Path) -> str:
    paths = _retired_evidence_paths(page_home)
    if not paths:
        return ""
    listed = ", ".join("<code>%s</code>" % html.escape(path) for path in paths[:3])
    extra = " and %d more" % (len(paths) - 3) if len(paths) > 3 else ""
    return (
        '<div class=evidence-migration-blocker><strong>v4 migration required.</strong> '
        'Retired Evidence paths are ignored: %s%s. Move them to '
        '<code>_archive/legacy-outline-evidence/</code> before accepting this Page as v4.</div>'
        % (listed, extra)
    )


def render(page_src: pathlib.Path, path_q: str, file_q: str,
           root: pathlib.Path | None = None) -> str:
    """Render the v4 Evidence Space as typed, Result-first disclosure cards."""
    from live.outline_prompts import assets_html as prompt_assets_html

    page_home = page_src.parent
    records = _evidence_inventory(page_src, _result_records(page_home))
    body = _evidence_sections(records, page_home=page_home, root=root or page_home,
                               path_q=path_q, file_q=file_q, page_src=page_src)
    migration_notice = _migration_notice(page_home)
    counts = {kind: sum(1 for record in records if _evidence_type(record) == kind)
              for kind in ("DISPLAY", "CITE", "VALUE")}
    overview = (
        '<a class=total href="#evidence-items">%d Evidence Items</a>' % len(records) +
        '<a href="#evidence-DISPLAY">%d Displays</a>' % counts["DISPLAY"] +
        '<a href="#evidence-CITE">%d Citations</a>' % counts["CITE"] +
        '<a href="#evidence-VALUE">%d Values</a>' % counts["VALUE"]
    )
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Evidence Space · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<body class=embedded>{prompt_assets_html()}<header><h1>Evidence Space</h1></header>
<div id=evidence-items class=evidence-list><div class=evidence-overview>{overview}</div>{migration_notice}
<details class=source-details><summary>Sources</summary><div class=source-body>Result <code>results/**/result.yaml</code>.</div></details>
{body}</div>
<script>
(function(){{var links=document.querySelectorAll('.evidence-overview a'),sections=document.querySelectorAll('.evidence-type-section'),source=document.querySelector('.source-details');
function applyFilter(){{var match=location.hash.match(/^#evidence-(DISPLAY|CITE|VALUE)$/),kind=match?match[1]:"";
sections.forEach(function(section){{section.hidden=!!kind && section.dataset.evidenceType!==kind;}});
if(source)source.hidden=!!kind;
links.forEach(function(link){{var active=!!kind && link.getAttribute('href')==="#evidence-"+kind;link.classList.toggle('active',active);}});
}}
window.addEventListener('hashchange',applyFilter);applyFilter();}})();
(function(){{var q=new URLSearchParams(location.search),id=q.get('focus');if(!id)return;
var row=document.getElementById(id);if(row){{row.open=true;row.classList.add('run-focus');row.scrollIntoView({{block:'center'}});}}}})();
</script>
</body>"""


class EvidenceTabMixin:
    """Current read-only Result-first route for Outline's Evidence Space."""

    # ---- GET/HEAD /_board/evidence?path=…&file=… ------------------------
    def evidence_tab_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        _p = {"path": path_q, "file": file_q}
        got = self.target(_p)
        file_q = _p["file"]
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0], path_q, file_q, root=got[1]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/evidence — the shell's write() twin, writes nothing
    def plug_evidence(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/evidence?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
