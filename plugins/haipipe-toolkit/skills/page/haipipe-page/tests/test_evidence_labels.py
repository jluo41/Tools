from pathlib import Path
import sys


PAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAGE_ROOT))

from src.evidence_labels import (classify_token, collect_result_labels,
                                 parse_result_labels, resolve_inline_labels)
from live.evidence import _evidence_sections, _result_records
from live.outline import _preview_reader_html


def _result_text():
    return r'''item: E01-VALUE-effect
type: VALUE
page_run: re-value-01_effect
run: re-execution-01
status: ready
provenance: results/re-value-01_effect/payload.json#sha256
labels:
  - token: "$V_effect$"
    kind: VALUE
    target: payload.effect
    status: resolved
    display: "100"
  - token: "\cite{C_source}"
    kind: CITE
    status: unresolved
    target: sources.primary
'''


def test_result_label_manifest_is_shared_by_value_and_citation_tokens():
    labels = parse_result_labels(_result_text())
    assert [(label["token"], label["kind"], label["display"])
            for label in labels] == [
                ("$V_effect$", "VALUE", "100"),
                (r"\cite{C_source}", "CITE", ""),
            ]

    spans = resolve_inline_labels("Effect: $V_effect$.", {
        "$V_effect$": labels[0],
    })
    assert spans[1]["binding"]["display"] == "100"


def test_page_token_grammar_covers_display_subtypes():
    assert classify_token(r"$V_effect$") == ("VALUE", "V_effect")
    for command in ("table", "figure", "algorithm"):
        assert classify_token(rf"\{command}{{D_unit}}") == ("DISPLAY", "D_unit")
    assert classify_token(r"\cite{C_source}") == ("CITE", "C_source")
    assert classify_token(r"\illustration{D_unit}") == ("", "")
    assert classify_token(r"\diagram{D_unit}") == ("", "")


def test_result_records_expose_labels_and_evidence_card_disclosure(tmp_path):
    page = tmp_path / "page"
    result = page / "results" / "re-value-01_effect"
    result.mkdir(parents=True)
    (result / "result.yaml").write_text(_result_text(), encoding="utf-8")

    records = _result_records(page)
    assert len(records) == 1
    fields = records[0]["fields"]
    assert fields["page_run"] == "re-value-01_effect"
    assert fields["owner run"] == "re-execution-01"
    assert fields["labels"][0]["item"] == "E01-VALUE-effect"
    assert fields["labels"][0]["provenance"] == "results/re-value-01_effect/payload.json"

    card = _evidence_sections(records)
    assert ">100</span>" in card
    assert "$V_effect$" in card
    assert "re-value-01_effect" in card
    assert "results/re-value-01_effect/payload.json" in card
    assert r"\cite{C_source}" in card


def test_evidence_cards_render_type_specific_result_previews(tmp_path):
    page = tmp_path / "page"
    display = page / "results" / "re-display-01_design"
    display.mkdir(parents=True)
    (display / "preview.png").write_bytes(b"not-a-real-image-for-render-test")
    (display / "result.yaml").write_text(
        "item: E01-DISPLAY-design\n"
        "type: DISPLAY\n"
        "run: re-display-01_design\n"
        "status: complete\n"
        "bullet: C1.P1.B1\n"
        "payload:\n"
        "  artifact: results/re-display-01_design/preview.png\n"
        "  reader_takeaway: Four panels connect the design inputs.\n",
        encoding="utf-8",
    )

    value = page / "results" / "re-value-01_effect"
    value.mkdir(parents=True)
    (value / "result.yaml").write_text(
        "item: E02-VALUE-effect\n"
        "type: VALUE\n"
        "run: re-value-01_effect\n"
        "status: complete\n"
        "payload:\n"
        "  estimate: 1.25\n"
        "  unit: MME\n"
        "  n: 148\n"
        "  interval_95: [-0.4, 2.9]\n",
        encoding="utf-8",
    )

    citation = page / "results" / "re-cite-01_source"
    citation.mkdir(parents=True)
    (citation / "result.yaml").write_text(
        "{\"item\": \"E03-CITE-source\", \"type\": \"CITE\", "
        "\"run\": \"re-cite-01_source\", \"status\": \"complete\", "
        "\"payload\": {\"sources\": [{\"cite\": \"@Smith_2024\", "
        "\"identity\": \"doi:10.1000/example\", "
        "\"claim\": \"The source supports the stated mechanism.\"}]}}",
        encoding="utf-8",
    )

    records = _result_records(page)
    card = _evidence_sections(records)
    assert 'class=evidence-preview-image' in card
    assert 'src="data:image/png;base64,' in card
    assert "Four panels connect the design inputs." in card
    assert 'class="evidence-preview-table evidence-preview-value-table"' in card
    assert "<th>Field</th><th>Value</th>" in card
    assert "<th>Estimate</th><td>1.25</td>" in card
    assert "MME" in card and "148" in card
    assert "class=evidence-preview-hero" not in card
    assert "class=evidence-preview-facts" not in card
    assert "@Smith_2024" in card
    assert "The source supports the stated mechanism." in card


def test_result_label_collection_is_deterministic(tmp_path):
    page = tmp_path / "page"
    result = page / "results" / "re-value-01_effect"
    result.mkdir(parents=True)
    (result / "result.yaml").write_text(_result_text(), encoding="utf-8")

    bindings = collect_result_labels(page)
    assert bindings["$V_effect$"]["display"] == "100"
    assert bindings["$V_effect$"]["result"] == "results/re-value-01_effect/result.yaml"


def test_outline_preview_embeds_visible_value_and_hidden_authored_token():
    html = _preview_reader_html(
        "The adjusted effect was $V_effect$.", {}, {
            "$V_effect$": {
                "kind": "VALUE",
                "display": "100",
                "status": "resolved",
                "item": "E01-VALUE-effect",
                "page_run": "re-value-01_effect",
                "result": "results/re-value-01_effect/result.yaml",
                "target": "payload.effect",
                "provenance": "results/re-value-01_effect/payload.json#sha256",
            }
        }
    )
    assert "100" in html
    assert "$V_effect$" in html
    assert "re-value-01_effect" in html
    assert "payload.effect" in html
    assert "payload.json#sha256" in html
    assert "missing-evidence-token" not in html


def test_outline_preview_keeps_unresolved_token_visible_and_escaped():
    html = _preview_reader_html(
        r"No result yet: $V_missing$ and <unsafe>.", {}, {}
    )
    assert "$V_missing$" in html
    assert "missing-evidence-token" in html
    assert "&lt;unsafe&gt;" in html
    assert "<unsafe>" not in html
