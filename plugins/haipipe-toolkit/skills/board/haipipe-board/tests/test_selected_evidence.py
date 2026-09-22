"""Reading and delivery select the same current evidence from the Item ledger."""
import pytest
from live.export import ExportMixin, _SCRIPTS
from live.evidence import _result_records
from src.evidence_selection import selected_results, EvidenceSelectionError
from src.evidence_labels import collect_result_labels


def fixture(tmp_path, kind='DISPLAY'):
    page = tmp_path / 'Page.md'
    page.write_text('# Page\n\n## Opening\nQuestion?\n\n## Content\n')
    outline = tmp_path / 'outline'
    outline.mkdir()
    item = f'E01-{kind}-example'
    manifest = tmp_path / 'results' / 're-selected' / 'result.yaml'
    manifest.parent.mkdir(parents=True)
    body = f'item: {item}\ntype: {kind}\npage_run: re-selected\nstatus: complete\n'
    if kind == 'DISPLAY':
        unit = manifest.parent / 'payload' / 'Page-Display1-test'
        (unit / 'assets').mkdir(parents=True)
        (unit / 'float.tex').write_text(r'\begin{table}\caption{Selected}\label{tab:selected}\end{table}')
        (unit / 'assets' / 'table-body.tex').write_text('Current evidence')
        body += 'payload:\n  unit: payload/Page-Display1-test\nlabels:\n  - token: D_selected\n    kind: DISPLAY\n    display: Selected\n    status: resolved\n'
    else:
        (manifest.parent / 'payload').mkdir()
        (manifest.parent / 'payload' / 'sources.bib').write_text('@article{Current, title={Current source}}\n')
        body += 'payload:\n  bibliography: payload/sources.bib\n'
    manifest.write_text(body)
    ledger = outline / 'Page-evidence-items.md'
    ledger.write_text(f'''### {item} · C1.P1.B1 · Example
- **Local Run**: Page · Evidence Item · reuse · re-selected → results/re-selected/result.yaml
- **Verified**: ✅ JL 2026-09-20
- **Decide**: ☑ make
''')
    return page, manifest, ledger


def test_binding_wins_over_history_for_every_reader(tmp_path):
    page, manifest, ledger = fixture(tmp_path)
    history = tmp_path / 'results' / 'zz-historical'
    history.mkdir()
    (history / 'result.yaml').write_text(manifest.read_text().replace('Selected', 'Stale'))
    assert selected_results(page) == [manifest]
    assert _result_records(tmp_path)[0]['fields']['result'] == 'results/re-selected/result.yaml'
    assert collect_result_labels(tmp_path)['D_selected']['display'] == 'Selected'
    units = ExportMixin()._page_units(page)
    assert len(units) == 1 and units[0][1]['caption'] == 'Selected'


def test_missing_binding_never_uses_legacy(tmp_path):
    page, manifest, ledger = fixture(tmp_path)
    legacy = tmp_path / 'outline' / 'evidence' / 'display' / 'old'
    legacy.mkdir(parents=True)
    (legacy / 'float.tex').write_text(r'\begin{table}\label{old}\end{table}')
    ledger.write_text(ledger.read_text().replace('re-selected/result.yaml', 'missing/result.yaml'))
    assert _result_records(tmp_path) == []
    assert collect_result_labels(tmp_path) == {}
    with pytest.raises(EvidenceSelectionError, match='selected Result is missing'):
        ExportMixin()._page_units(page)


def test_selected_bib_requires_verification(tmp_path):
    page, manifest, ledger = fixture(tmp_path, 'CITE')
    old = tmp_path / 'outline' / 'evidence' / 'bibex'
    old.mkdir(parents=True)
    (old / 'Page.bib').write_text('@article{Stale, title={Stale source}}')
    out = tmp_path / 'delivery'
    out.mkdir()
    bib = ExportMixin()._selected_bibliography(page, out)
    assert 'Current' in bib.read_text() and 'Stale' not in bib.read_text()
    ledger.write_text(ledger.read_text().replace('✅ JL 2026-09-20', '⬜'))
    with pytest.raises(EvidenceSelectionError, match='verification'):
        ExportMixin()._selected_bibliography(page, out)


def test_wrong_run_and_escaped_bib_are_rejected(tmp_path):
    page, manifest, ledger = fixture(tmp_path, 'CITE')
    original = manifest.read_text()
    manifest.write_text(original.replace('re-selected', 're-wrong'))
    with pytest.raises(EvidenceSelectionError, match='Local Run'):
        selected_results(page)
    manifest.write_text(original.replace('payload/sources.bib', '../../../external.bib'))
    with pytest.raises(EvidenceSelectionError, match='leaves its selected Result'):
        ExportMixin()._selected_bibliography(page, tmp_path)


def test_deferred_result_is_not_exported(tmp_path):
    page, manifest, ledger = fixture(tmp_path)
    ledger.write_text(ledger.read_text().replace('☑ make', '☑ defer'))
    assert selected_results(page) == []
    assert ExportMixin()._page_units(page) == []


def test_history_ambiguity_is_not_resolved_by_filename(tmp_path):
    page, manifest, ledger = fixture(tmp_path)
    ledger.unlink()
    duplicate = tmp_path / 'results' / 'zz-historical'
    duplicate.mkdir()
    (duplicate / 'result.yaml').write_text(manifest.read_text())
    with pytest.raises(EvidenceSelectionError, match='Ambiguous historical Results'):
        ExportMixin()._page_units(page)
    assert _result_records(tmp_path) == []


def test_export_scripts_resolve_to_canonical_writers():
    assert (_SCRIPTS / 'md2tex.py').is_file()
    assert (_SCRIPTS / 'md2docx.py').is_file()


@pytest.mark.parametrize('method', ['export_word', 'export_latex'])
def test_both_writers_reject_invalid_selection_before_conversion(tmp_path, method):
    page, manifest, ledger = fixture(tmp_path)
    manifest.write_text(manifest.read_text().replace('status: complete', 'status: blocked'))
    out = tmp_path / 'out'
    out.mkdir()
    class Fake(ExportMixin):
        root = tmp_path
        def _export_target(self, payload, workbench): return page, out, tmp_path, None
        def _canon_ctx(self, board, payload): return {}
        def _run(self, *args, **kwargs): raise AssertionError('Converter must not run')
    result, error = getattr(Fake(), method)({})
    assert result is None and 'not ready' in error


def test_word_stages_only_selected_display(tmp_path):
    import json
    page, manifest, ledger = fixture(tmp_path)
    historical = tmp_path / 'results' / 'zz-history' / 'payload' / 'old'
    historical.mkdir(parents=True)
    (historical / 'float.tex').write_text(r'\begin{table}\caption{Stale}\label{tab:selected}\end{table}')
    out = tmp_path / 'out'
    out.mkdir()
    class Fake(ExportMixin):
        root = tmp_path
        def _export_target(self, payload, workbench): return page, out, tmp_path, None
        def _canon_ctx(self, board, payload): return {}
        def _rebuild_ui(self, route, payload): return '', ''
        def _run(self, cmd, **kwargs):
            from pathlib import Path
            if '--display-root' in cmd:
                files = list(Path(cmd[cmd.index('--display-root')+1]).rglob('float.tex'))
                assert len(files)==1 and 'Selected' in files[0].read_text()
            Path(cmd[cmd.index('-o')+1]).write_bytes(b'fixture artifact')
            return 0, 'ok'
    result, error = Fake().export_word({})
    assert error is None and result['ok']
    assert json.loads((out/'evidence-selection.json').read_text())['profile']=='current-ledger'


def test_duplicate_keys_within_one_selected_bib_are_rejected(tmp_path):
    page, manifest, ledger = fixture(tmp_path, 'CITE')
    bib = manifest.parent/'payload'/'sources.bib'
    bib.write_text(bib.read_text()+'@article{Current, title={Conflicting source}}\n')
    with pytest.raises(EvidenceSelectionError, match='duplicate keys within'):
        ExportMixin()._selected_bibliography(page, tmp_path)
