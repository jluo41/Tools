# Delivery tab · one tab owns what four lanes ship

**LOAD `haipipe-workbench` and `../SKILL.md` (`haipipe-workbench-page`) FIRST.** This
reference is one lane contract of `haipipe-workbench-page`: the 📤 Delivery tab
over `<page>/delivery/` and the four internal lanes beneath it (latex · word ·
slide · render). Each lane keeps its own storage, writer, and gate here; none
is a second callable Workbench skill, and the tab never auto-calls a model.

```text
the tab       📤 Delivery: a 🏠 stat of what is built, one segment per lane
the lanes     delivery/latex/ · delivery/word/ · delivery/slide/ · delivery/render/
              (flat <page>/latex/ etc. are compatibility reads only)
the writers   /_board/latex → exporters/md2tex.py + LuaLaTeX
              /_board/word  → exporters/md2docx.py + exporters/docx2pdf.py
              /_board/autodeck → servers/workbench-studio/autodeck.py (claude -p)
              render → the Folder-native writer of the owning Design contract;
                       POST /_board/render is only an optional served adapter
the server    servers/workbench-page/delivery.py (surface) · export.py (doors) ·
              exporters/ (the md2tex, md2docx, docx2pdf scripts, run by path)
```

## 📡 Surface · one tab, five segments

```text
📤 Delivery
├── 🏠 What's built   one row per lane: ✅ built · mtime, or ⬜ with the way to
│                     build it; render/ shows its file count
├── 📜 LaTeX          the saved <stem>-view.html; BUILT ON CLICK via /_board/latex
├── 📝 Word           the PDF twin of <stem>.docx; built on click via /_board/word
├── 🎞 Slides         the saved <stem>-deck.html + the ✨ authoring bar: one
│                     explicit press → /_board/autodeck; a missing deck is a
│                     ghost until a person presses, never a view
└── 📱 Render         saved recipient previews (.txt sms/push/reminder ·
                      .html ui-card/dashboard · .docx report) + manifest.json
```

LaTeX and Word are deterministic pens and may build on click. The deck is an
AUTHORED artifact (`claude -p`, minutes, money) and builds only on the ✨ press.
Render is regenerated, never edited; an unpinned venue refuses.

## 🗂 Storage · derived, regenerable, never hand-edited

Every lane is DERIVED from the Page's Markdown: `delivery/latex/<stem>.tex` +
`<stem>.pdf`, `delivery/word/<stem>.docx` + preview `<stem>.pdf`,
`delivery/slide/<stem>-deck.html`, `delivery/render/<stem>-<unit>-v<N>.<ext>`
+ `manifest.json`. A hand edit is overwritten on the next build and the folder
is safe to gitignore. `delivery/web/` is the Page-owned static export built by
`haipipe-page/cli/page.py build`; it is not a lane of this tab.

Current Word and LaTeX exports use only the ledger-selected Results and record
`evidence-selection.json`. Pages without a ledger use the labelled legacy
migration profile; missing current bindings never fall back to a legacy Bib or
display. The shared Markdown reader strips HTML comments (Board receipts) so
they never become manuscript prose.

## 🧾 RD ownership and receipt

Load `../../haipipe-page/ref/page-run-families.md` for the Page Run identity
contract. Each concrete delivery target/version is an `RD` Page Delivery Run
(`rdNN_web`, `rdNN_latex`, `rdNN_word`, `rdNN_slide`, `rdNN_render`). An RD
binds one source Page version to one target lane; the exporter writes the
artifact and the Run's `runtime.yaml` keeps status and warnings. No lane
manifest is written (JL 260928): the built files and their times are the
record. Rebuilding the same target is another attempt in that RD lineage; a
different target or a materially different source version gets a different
RD. A current lane is delivery evidence, not a whole-Page acceptance decision:
`haipipe-page-check` remains the only human whole-Page close gate.

## 🔍 Delivery Workspace · consistency projection

`/_board/delivery?path=…&file=…&workspace=1` (standalone and Board-hosted) is a
GET-only projection Outline embeds. It compares each lane's built files with
the current Page Markdown by file time alone (JL 260928: no content hashes, no
build record needed): a lane is `pass` when its files are at least as new as
the Page, `stale` when one is older, `not-built` when it has none. The web
lane's Markdown copy must also read the same as the Page. Each lane shows the
exact reason, file and build time. It never rebuilds or edits a file. The active lane entries copy a context-bound request to chat;
copying never sends, starts, builds, or writes.

## 📂 Files

- `../../../../servers/workbench-page/delivery.py` · the segmented surface, its
  POST twin, and the Delivery Workspace
- `../../../../servers/workbench-page/export.py` · the `/_board/latex` and
  `/_board/word` doors
- `../../../../servers/workbench-page/exporters/` · `md2tex.py`, `md2docx.py`,
  `docx2pdf.py`, `test_md2docx.py`
- `../../../../servers/workbench-page/assets/js/10-drawer/82-workbench-delivery.js` ·
  the one registry row
- `../../../../servers/workbench-studio/autodeck.py` · the deck's ✨ pen
- `../../haipipe-workbench/ref/roster.md` · the `delivery/`, `latex/`, `word/`,
  `slide/`, `render/`, and `web/` rows
