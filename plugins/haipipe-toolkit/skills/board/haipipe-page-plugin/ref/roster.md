# The plugin roster · one row per name

The single list of page-plugin names (design.excalidraw, JL 260815).
A subfolder of a page's home folder is board material only if its name is here.
`kind`: PRIMARY = originals a person makes, committed; DERIVED = projections of the page's text, regenerable, gitignorable.

| name       | kind    | storage (`<page>/<name>/`)          | surface (right-pane tab)             | writer                                        | status |
|------------|---------|-------------------------------------|--------------------------------------|-----------------------------------------------|--------|
| `draw/`    | PRIMARY | `<stem>.excalidraw` scene           | 🖌 the live Excalidraw editor        | the xcal save path (`live/xcal.py`)           | 🟢 live |
| `chat/`    | PRIMARY | `<YYMMDD-HHMM>/` kept sessions      | 💬 Chat (GUI/TUI segment inside)     | the session's closing keep step (QPf4, open)  | 🟡 live tab; landing unruled |
| `meeting/` | PRIMARY | `<YYMMDD-HHMM>/` digest + transcript| 🗣 digest reader (planned)           | the meeting intake                            | 📋 declared |
| `slide/`   | DERIVED | `<stem>-deck.html`                  | 🎞 the deck, framed `?plain`         | `/_board/deck` (`live/deck.py` + reflow)      | 🟢 live |
| `latex/`   | DERIVED | `<stem>.tex` + compiled `<stem>.pdf`| 📜 the compiled PDF, tex fallback    | `/_board/latex` → `md2tex.py` + xelatex       | 🟢 built this round |
| `word/`    | DERIVED | `<stem>.docx` + preview `<stem>.pdf`| 📝 the PDF twin; ⬇ the .docx        | `/_board/word` → `md2docx.py` + `docx2pdf.py` | 🟢 built this round |
| `bibex/`   | MIXED   | `<stem>.bib` PRIMARY (the page's own bib, JL 260815) + derived `<stem>-bib.html` | 📚 citation workbench: status chip, Scholar/DOI/URL links, ✓ checked tick, ✎ edit, ＋ add | `/_board/bibex` refresh (seed-imports from the paper's `0-*.bib`, never writes it) + `/_board/bibex-verify` (the human ✓ as a `verified` field) + `/_board/bibex-entry` (the pen: person-supplied text verbatim, never composed) | 🟢 built this round |
| `display/` | DERIVED | floats the page's divisions ship    | 🖼 (planned)                         | the display family                            | 📋 declared |
| `skill/`   | MIXED   | `<stem>.md` PRIMARY (the page's skill map: uses/designs rows, aligned ticks) + derived `<stem>-skill.html` | 🛠 skill workbench: one card per skill with version, drift dates, ✓ aligned, ↑ designs, ＋ declare | `/_board/skill` scan-seed (uses at most, never invents) + `/_board/skill-verify` (the human ✓) + `/_board/skill-entry` (the pen, typo-guarded) | 🟢 built 260815 |
| `logging/` | PRIMARY | run/session logs the page owns      | 🧾 (planned)                         | the owning runner                             | 📋 declared |
| `_fixture/`| PRIMARY | specimen inputs/outputs             | none — underscore keeps it off-board | the specimen's builder                        | 📋 declared |

Writers for the DERIVED paper trio live in `skills/paper/haipipe-paper/scripts/to-word/` (`md2tex.py`, `md2docx.py`, `docx2pdf.py`); the board calls them and holds no copy.
`--paper-root` is discovered by walking up from the page for a `0-*.bib`; a page outside any paper exports cite-less rather than refusing.
