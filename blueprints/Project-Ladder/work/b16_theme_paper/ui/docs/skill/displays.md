# Displays

How a paper's displays show on the Board's Displays list and in their preview PDFs (workbench-paper
`board_displays.py`, haipipe-display `scripts/build_preview.py`). Each topic below is one rule, with its requests.

## 📊 Topic: Displays ▸ the list names each display as the paper prints it

A tab's second line is the face's `name:`, else the s06 display plan's `name` column, else the face title; never the
folder's old number. A display the paper no longer prints (`number: not printed`) leaves the list; its folder stays.

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-21 | after a renumber the tab read "Table C4 · Table · C3 icd codes" | Pp-AgreeableRx-Discrention | `_display_line` takes the plan's name, drops a folder's leading number; test `test_display_list_names.py` |
| 11-21 | "what is this??? is this the new one?? I am confused." (old Table D4 under Others) | JL via Pp-AgreeableRx-Discrention | `retired()` hides `number: not printed` Tasks from every Displays list |

## 🔖 Topic: Displays ▸ a preview prints its citations

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-21 | the preview printed "(?)" for each `\citep` (Table C1) | Pp-AgreeableRx-Discrention | `build_preview.py` adds the paper's bib as a hidden bibliography and runs bibtex; test `test_preview_citations.py` |
