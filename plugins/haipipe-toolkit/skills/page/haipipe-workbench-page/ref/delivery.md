# Delivery Space · what the Page ships, and the one Run per lane that builds it

**LOAD `../SKILL.md` (`haipipe-workbench-page`) FIRST.** This reference owns the
Delivery Space of the Page workbench: the built files under `<page>/delivery/`,
the check that says whether each lane is current, and the fixed Delivery Runs
listed in its Runs panel. Rebuilding itself is `haipipe-page-delivery`.

```text
the Space     Delivery · tabs Web · LaTeX · Word · Slides, each with its state
              (pass · stale · not built) · views Preview · Artifacts · Checks
the Runs      one fixed Run per lane in the Runs panel on the right:
              run-delivery-webpage · run-delivery-latex · run-delivery-word
              (Done while the lane is current, Ready when the Page changed)
the command   page.py export <page> [--lane web|latex|word|all] [--author "<name>"]
              writes runs/run-delivery-<lane>.sh and the lane's files
the writers   web    → haipipe-page/src/page_workspace.py (build_page)
              latex  → exporters/md2tex.py + LuaLaTeX      (ExportMixin.export_latex)
              word   → exporters/md2docx.py + docx2pdf.py  (ExportMixin.export_word)
              slides → servers/workbench-shared/autodeck.py, only on the ✨ press
```

## 🗂 Storage · derived, never hand-edited

```text
delivery/web/     index.html · <page>.md (a copy that must read the same as the Page)
delivery/latex/   <page>.tex · <page>.pdf · <page>-view.html · evidence-selection.json
delivery/word/    <page>.docx · <page>.pdf (its twin) · <page>-view.html · evidence-selection.json
delivery/slide/   <page>-deck.html
```

Every file is written by code from the Page (AGENTS.md rule 6). A wrong word is
a Page or Draft edit, a wrong layout is an exporter fix; either way the lane's
Run is rerun. No lane manifest, receipt or hash is written (rules 6 and 9), and
a Delivery Run keeps no `results/` folder. Older `rdNN_<lane>` Runs and any
leftover `build-manifest.json` are history that nothing reads.

Word and LaTeX use only the ledger-selected Results and record
`evidence-selection.json`. A Page without a ledger uses the labelled legacy
migration profile; missing current bindings never fall back to a legacy Bib or
display. The shared Markdown reader strips HTML comments so Board notes never
become manuscript prose. The deck is authored by a model (`claude -p`, minutes,
money), so it builds only on the explicit ✨ press.

## 🔍 Checks · current or stale, by file time

The Checks view frames `/_board/delivery?path=…&file=…&workspace=1`
(`delivery.py::check_delivery`, GET only, never builds or edits). A lane is
`pass` when its built files are at least as new as the Page, `stale` when one is
older, and `not built` when it has none; the web copy must also read the same as
the Page. Each row names the file and its build time. A current lane is
delivery evidence, not a whole-Page acceptance: `haipipe-page-check` remains
the only whole-Page close gate. `/_board/delivery` without `workspace=1` is the
older 📤 tab, kept for old links.

## 📂 Files

- `../../workflow-runs/haipipe-page-delivery/SKILL.md` · the fixed Runs and how to rerun them
- `../../haipipe-page/src/page_export.py` · `cli/page.py export` · the command and the ticket writer
- `../../../../servers/workbench-page/space_views.py` · `delivery_space_html`, the Space
- `../../../../servers/workbench-page/delivery.py` · `check_delivery`, `FIXED_RUNS`, the Checks view
- `../../../../servers/workbench-page/runs.py` · `_fixed_delivery_run`, the Runs panel rows
- `../../../../servers/workbench-page/export.py` · `exporters/` · the LaTeX and Word writers
- `../../../../servers/workbench-shared/autodeck.py` · the deck's ✨ pen
