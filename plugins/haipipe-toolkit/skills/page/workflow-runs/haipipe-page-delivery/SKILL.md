---
name: haipipe-page-delivery
description: >-
  The Delivery Runs of a Page: one fixed Run per lane (run-delivery-webpage,
  run-delivery-latex, run-delivery-word), rerun in place for every rebuild by
  `page.py export`. The built files are the result: no new Run id, no receipt,
  no manifest, no hash. It never rewrites prose or evidence and never closes the
  Page. Trigger: delivery run, build the pdf, build the docx, build the web
  page, rebuild delivery, stale delivery, /haipipe-page-delivery.
metadata:
  version: "0.2.1"
  last_updated: "2026-09-30"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-delivery · one fixed Run per lane, rerun in place

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means every file under `delivery/<lane>/`: fix the Page or the exporter, then rerun the lane's Run.

**Load nothing else to rebuild.** A rebuild is one command; this file is all of it.

```text
lane    Run (fixed name)        ticket                          result
web     run-delivery-webpage    runs/run-delivery-webpage.sh    delivery/web/     index.html · <page>.md copy
latex   run-delivery-latex      runs/run-delivery-latex.sh      delivery/latex/   <page>.tex · <page>.pdf
word    run-delivery-word       runs/run-delivery-word.sh       delivery/word/    <page>.docx · its PDF twin
```

## 🔁 Rebuild = rerun the same Run

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/page.py export <page-folder> [--lane web|latex|word|all] [--author "Junjie Luo"]
# or, after the first export has written it:  bash <page-folder>/runs/run-delivery-<lane>.sh
```

1. **Same Run every time.** Never allocate `rd01_web`, `rd02_web`, or an attempt
   number (JL 260928: "we just need one run ... no need for rd01_web, rd02_web").
2. **Code writes the ticket.** `page.py export` writes `runs/run-delivery-<lane>.sh`
   with the exact command it ran; nobody types it.
3. **No record to write.** No `runtime.yaml`, no receipt, no
   `build-manifest.json`, no hash (AGENTS.md rules 6 and 9). The files in
   `delivery/<lane>/` and their file time are the whole record.
4. **The state shows itself.** The Delivery Space and the Runs panel call a lane
   current (`Done`) when its files are at least as new as the Page, and stale
   (`Ready`, rerun it) when the Page changed after the build.
5. **Any time.** A build never changes the Page, so it may run whenever the
   person wants to read or send the file. A current lane is not a whole-Page
   acceptance; `haipipe-page-check` is the only whole-Page close gate.

The author of Word comments is the person annotating; for JL's papers it is
"Junjie Luo" (AGENTS.md, Papers). Slides keep the same one-Run rule
(`run-delivery-slides`), but only the explicit ✨ press in the Delivery Space
starts it, because a model writes the deck (minutes, money). A render (Design
screens) belongs to the Design contract (`run-delivery-render`).

## 🔒 Boundaries

- Never edits `<page>.md`, the Draft, an Evidence Result, or an accepted Version.
- A wrong word in a built file is a Page or Draft edit, then a rerun
  (`haipipe-page`, fast path). A wrong layout is an exporter fix, then a rerun.
- Never assembles a paper: paper-level assembly is `haipipe-paper-assemble`.
- Older numbered Runs (`rdNN_<lane>`) are history: read them, never add to them.
- Missing current evidence bindings never fall back to a legacy Bib or display.
- The LaTeX lane never replaces a `<page>.tex` it did not write. A fragment without the
  `% GENERATED from` first line holds words that may exist only there (a hand-owned or
  migrated Section), so md2tex refuses; move the words into the Page and adopt, then
  delete the fragment and rerun.

## 📂 Files

- `../../haipipe-page/cli/page.py` (`export`) · `../../haipipe-page/src/page_export.py` · the command and the ticket writer
- `../../../../servers/workbench-page/export.py` · `exporters/` · the LaTeX and Word writers
- `../../../../servers/workbench-page/delivery.py` · the Delivery Space checks and `FIXED_RUNS`
- `../../haipipe-workbench-page/ref/delivery.md` · the Delivery Space
- `../../../paper/haipipe-paper-assemble/SKILL.md` · paper-level assembly, a different Run
