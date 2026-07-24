# Migrate the two old boards
state: ✅ SETTLED
owner: CC
method: rewrite into the new format + regenerate the html + delete the old intermediates

## Question
Two old-format boards already sit under `subjective-label/diagram/`. Should they migrate to the new format, and how far does the migration need to go?

- Why it is hard
  Migrate too much and it is wasted work (those boards' topics have passed); migrate too little and they will not open — useless as examples.
- What breaks if we leave it
  Those two boards are this skill's only **physical evidence**. If they stay stuck in an unopenable old version, nothing SKILL.md says has a single example to point at.
- What it affects downstream
  It also tests one thing directly: whether the generator is truly backward-compatible with old boards (whether the `ALIAS` multi-name mechanism holds).

## Boundary
- ✅ Covered here
  **What happens to the legacy boards**: which ones migrate, how far, or regenerate in place.
- ↪ Covered elsewhere
  The new format itself — that is `QA1`/`QA2`/`QA4`. This question owns only the existing stock.

## Diagram
```
01-sublabel-license-260722/  ──folded──►  02-method-260722/ (new format, 13 questions)
  validation core ①②⑤        ─►  QB3 take a score that is not self-assigned
  ③ auto-lexicon             ─►  QD4 do not hard-code the lexicon
  ④ objective                ─►  QC3 which criterion picks the construct
  ⑥ b02-naming               ─►  a ZD comment on QC2
  Di's note-update/audit      ─►  02/_source/ (archived, not destroyed)
  board.md/html/bak · deck.html · render.py  ─►  deleted
```

## Items to Finish
- [x] `02-method-260722/` converted to the QA1 format: split into one file per question (13 `QX-slug.md`), Chinese section names → English, `[Q1]` → `QA1`, Diagram/Log added
- [x] `02-method`'s `board.html` regenerated and opens fine (13 questions, 20,450 chars of body with zero scripts)
- [x] `01-sublabel-license-260722/` fully absorbed: validation core → QB3, ③ → QD4, ④ → QC3, ⑥ → a QC2 comment; Di's F1–F8 dispatched as 12 anchored comments; Di's design originals moved to `02/_source/`
- [x] Old intermediates removed: the whole `01-sublabel-license-260722/` (incl. `render.py`/`deck.html`/`board.html.bak`) deleted

## Where we are
**Both legacy boards are migrated; `02-method-260722/` is now the single subjective-label board** (13 questions, four groups QA/QB/QC/QD, colored index ordered by the Roster, script-free static page).
- `02-method` content: 7 method Qs (QA1–QA3 / QB1–QB2 / QC1–QC2) + QB3 absorbing 01-license's validation core + the QD engine group JL raised on the spot (QD1 embedding · QD2 cascade · QD3 train a classifier · QD4 auto-lexicon) + QC3 objective, folded out of 01-license's ④.
- `01-license` disposition: all 6 items rehomed (①②⑤ → QB3 · ③ → QD4 · ④ → QC3 · ⑥ → QC2 comment); Di's F1–F8 methodology flaws dispatched as 12 anchored `## Comments` (signed ZD, 12/12 highlight hits); Di's `note-update-v3` + `workflow-audit` archived into `02/_source/`; the old folder deleted.

## Files
- `build.py`
  `ALIAS` decides whether old section names are still recognized — whether an old board regenerates untouched depends entirely on it.
- `Tools/plugins/subjective-label/diagram/`
  Where the two legacy boards lived.

## Glossary
blank page: the old page built its entire body with an in-page JS pass, and VS Code's preview pane does not run that JS — so it opened pure white. The new version bakes the body into the HTML with zero scripts, so a blank page is impossible.

## Discussion

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1620 · Closed 🟡→✅: 01-license all six rehomed (③→QD4 ④→QC3 ⑥→QC2 comment), Di F1–F8 dispatched as 12 anchored comments, Di originals archived into `02/_source/`, old folder deleted; 02 now 13 questions
260723 1605 · `02-method` migrated: one file per question (11 then) + 01-license validation core absorbed (QB3) + the new QD engine group; state 🔴→🟡 (01-license's ③④⑥ and cleanup left, pending JL)
260723 0919 · Renumbered Q6 → QB3
260722 2340 · Finish line gains "delete the old deck.html / render.py"
260722 2255 · Opened
260722 2129 · 02-method switched to the static build (7 questions, zero scripts), not yet one-file-per-question
