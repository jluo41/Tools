# Delivery Space · what the Page ships, and the one Run per lane that builds it

**LOAD `../SKILL.md` (`workbench-task-draft`) FIRST.** This reference owns the
Delivery Space of the Page workbench: the built files under `<Block>/delivery/<source-relative-path>/`,
the check that says whether each lane is current, and the fixed Delivery Runs
listed in its Runs panel. Rebuilding itself is `haipipe-delivery (ref/page-delivery.md)`.

```text
the Space     Delivery · tabs Web · LaTeX · Word · Slides, each with its state
              (pass · stale · not built) · views Preview · Artifacts · Checks
the Runs      one fixed Run per lane in the Runs panel on the right:
              run-delivery-webpage · run-delivery-latex · run-delivery-word
              (Done while the lane is current, Ready when the Page changed)
the command   page.py export <page> [--lane web|latex|word|all] [--author "<name>"]
                [--accept-dropped-keys]
              writes runs/run-delivery-<lane>.sh and the lane's files
the writers   web    → haipipe-draft/src/page_workspace.py (build_page)
              latex  → exporters/md2tex.py + LuaLaTeX      (ExportMixin.export_latex)
              word   → exporters/md2docx.py + docx2pdf.py  (ExportMixin.export_word)
              slides → servers/workbench/autodeck.py, only on the ✨ press
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

## ❌ A refused LaTeX build · the old fragment stays, so it fails loudly

md2tex REFUSES to replace `delivery/latex/<page>.tex` when a citation key would
leave the Section, or when the old fragment has no `% GENERATED from` header.
The refused Section keeps its OLD fragment, and the paper build reads that
fragment, so a refusal is a failure, never a note (261103: three MISQ Sections
printed old words). md2tex prints `❌ REFUSED <page>: ...` with the dropped keys
and the old fragment's date and exits 2; the LaTeX door answers `ok: false`;
`page.py export` prints `❌ latex` and exits 1.

```text
REFUSED t01_introduction: 1 citation key(s) would leave this Section: example2022two.
The old fragment .../latex/t01_introduction.tex (written 2026-11-03 11:28) stays, so a
paper build prints its OLD words. If the drop is intended, rerun with --accept-dropped-keys
```

An intended drop (a rewrite, a paragraph moved to another Section) passes with
`page.py export <page> --lane latex --accept-dropped-keys` (md2tex's flag of the
same name; the door reads `accept_dropped_keys` from the POST body). Each
dropped key passes only when another Section of the paper still cites it (the
Section Pages beside this one, in the same version Job or in the `B?-` groups;
md2tex `--paper-pages` names them explicitly), or a revise card in
`draft/records/<page>-revise.md` removed it (its `Original:` cites the key, its
`Expected:` does not). Any other key stays refused, named. The paper build
(`haipipe-paper-assemble` 0.14.0) stops on a stale fragment and passes the same
flag to each stale Section's lane.

## 🔍 Checks · current or stale, by file time

The Checks view frames `/_board/delivery?path=…&file=…&workspace=1`
(`delivery.py::check_delivery`, GET only, never builds or edits). A lane is
`pass` when its built files are at least as new as the Page, `stale` when one is
older, and `not built` when it has none; the web copy must also read the same as
the Page. Each row names the file and its build time. A current lane is
delivery evidence, not a whole-Page acceptance: `haipipe-draft-review` remains
the only whole-Page close gate. `/_board/delivery` without `workspace=1` is the
older 📤 tab, kept for old links.

## 📂 Files

- `../../../project/haipipe-delivery/ref/page-delivery.md` · the fixed Runs and how to rerun them
- `../../../draft/haipipe-draft/src/page_export.py` · `cli/page.py export` · the command and the ticket writer
- `../../../../../servers/workbench/workbench-task-draft/space_views.py` · `delivery_space_html`, the Space
- `../../../../../servers/workbench/workbench-task-draft/delivery.py` · `check_delivery`, `FIXED_RUNS`, the Checks view
- `../../../../../servers/workbench/workbench-task-draft/runs.py` · `_fixed_delivery_run`, the Runs panel rows
- `../../../../../servers/workbench/workbench-task-draft/export.py` · `exporters/` · the LaTeX and Word writers
- `../../../../../servers/workbench/autodeck.py` · the deck's ✨ pen
