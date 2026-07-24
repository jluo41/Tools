# Q file template
state: 🟡 PARTIAL
owner: CC
method: ship a blank template that can be copied as-is, with required sections clearly marked

## Question
I open an empty `QA9-xxx.md` — what do I put in it? Which sections are required, and which can be deleted wholesale?

- Why it is hard
  The generator only recognizes a fixed set of section names. Misspell one and that section **silently disappears — no error**. Silent failure is the hardest kind to debug.
- What breaks if we leave it
  Without a clear template, everyone writes a different-shaped Q and the page turns messy; the RA and future agents touch this file every day.
- What it affects downstream
  The template decides what the page can display at all. It is the flip side of `QA4`: when `QA4` changes the on-stage order, this template must follow, or newly written questions drift back to the old shape.

## Boundary
- ✅ Covered here
  **The inside of one Q file**: which sections exist, which are required vs. optional, what goes in each, and what `ref/q-template.md` looks like.
- ↪ Covered elsewhere
  Which files are in the folder and how a Q attaches to the board — that is `QA1`. Nor **how the words inside each section should be written** — that is `QA5` (this one owns structure, that one owns prose).

## Diagram
```
copy ref/q-template.md                    required? → where it shows
┌────────────────────────────────┐
│ # short title    ≤14 chars     │ required → index row + page headline
│ state: 🔴 OPEN                 │ required → status badge (one word only)
│ owner: CC   method: …          │ owner required / method optional → header bar
├────────────────────────────────┤
│ ## Question   1 para + bullets │ required → ❓ the big lead line
│ ## Boundary   owns / not-owns  │ advised  → 🚧 grey border
│ ## Diagram    ascii figure     │ optional → the signature figure
│ ## Items to Finish - [ ] list  │ required → 🎯 green box (auto-counts 2/5)
│ ## Where we are                │ required → 📍 yellow box
│ ## Files      what it touches  │ advised  → 📁 blue border
├────────────────────────────────┤ ↓ all folded, never on stage
│ ## Law    ## Lesson            │ optional → settled rules / lessons learned
│ ## Glossary   ## Discussion    │ optional → new words / free discussion
│ ## Comments   ## Log           │ optional → inline comments / change log
└────────────────────────────────┘
```

## Items to Finish
- [x] A blank template file under `ref/` that can be copied as-is
      `ref/q-template.md` (`board.md`'s `## Links` points it at the skill's ref). Parse-tested against build.py: state/owner/method stay clean, all 11 sections are picked up, and the top `<!-- usage -->` comment is dropped at build time and never reaches the page.
- [x] One guide line at the top of every section: what to write here, and how long
      The first line of each section's body IS the guide sentence (what + how long); you overwrite it as you fill in.
- [x] Mark which sections are required and which optional
      Guide sentences start with `required ·` / `optional ·`; the top four lines (title · state · owner required, method optional) are covered in the usage comment — the markers must NOT go into lines like `state:`, the meta parser would eat them.
- [x] Adding a question = copy the template and rename, without consulting any existing board
      A zero-background agent, given only the template, filled out a valid card (`/tmp/QA9-testfill.md`, parse-verified) without opening any existing board.
- [x] Template caught up with the 260723 redesign
      New order, new section names (`Items to Finish` / `Where we are`), new `## Boundary`, `## Question` turned into "one paragraph + bullets", `## Why here` retired — `ref/q-template.md` rewritten.
- [ ] Re-run the zero-background fill test on the new template
      The last cold-read validated the OLD template. The structure changed, so it must be re-verified: a fresh agent, given only the new template, fills out a card a zero-background reader can understand.

## Where we are
**The template has caught up with the 260723 redesign, but the new version has not been cold-read yet — hence back to 🟡.**

- What the template looks like
  Top block `# title / state / owner / method`, plus 11 `##` sections. The first line of each section is a guide sentence starting with `required ·` or `optional ·`, overwritten as you fill in. A `<!-- usage -->` comment at the top explains how to use it and is dropped at build time.
- Required / optional
  Six required: `# title`, `state`, `owner`, `## Question`, `## Items to Finish`, `## Where we are`. `## Boundary` and `## Files` optional but strongly advised; everything else (`method`, `## Diagram`, all folded sections) optional — if unused, delete the whole section including its heading.
- Three drift spots fixed along the way (template, `board-form.md`, `SKILL.md` disagreed)
  ① Added `## Law` (settled rules) and `## Lesson` (pitfalls) — build.py recognized both all along and other questions were using them; only these three docs missed them. Synced.
  ② The old template said "newest Log lines at the bottom", contradicting the reverse order settled at 1120 (`sort_log` reverse=True, newest on top). Fixed.
  ③ The top four lines used to sit outside the required/optional rules, so a cold-reading agent had to guess; now covered in the usage comment, with a legend for `state`.
- Previously "undecided" items now decided
  Section order in the file is free (build.py fetches by name; the fold order on the page is fixed by build.py); `## Glossary` is optional, not per-question mandatory; `state:` takes exactly one status word — do not copy the legend into it.

## Files
- `ref/q-template.md`
  The deliverable itself — adding a question means copying it.
- `build.py`
  `ALIAS` / `sec()` decide which section names are recognized; a misspelled name silently yields nothing.
- `ref/board-form.md`
  §4 section↔page mapping + required/optional.

## Law
- Section names must be kept verbatim
  build.py takes the whole string after `## ` as the key (`ln[3:].strip()`), so `## Question (required)` is not found. Required/optional markers therefore go into the first body line, never the heading line.
- The six required things (after the 260723 redesign)
  `# title`, `state`, `owner`, `## Question`, `## Items to Finish`, `## Where we are`.
  `## Boundary` optional but strongly advised; everything else optional — delete the whole section if unused.
- On-stage order is fixed
  `Question → Boundary → Diagram → Items to Finish → Where we are` — intent first, status second (settled by `QA4`).
- Fold order is fixed by build.py
  On the page it is always Why here · Discussion · Comments · Law · Lesson · Glossary · Log, regardless of file order.
- Renaming a section must go through ALIAS
  One slot recognizes several names (`Done when` = `Items to Finish`, `Now` = `Where we are`, the old Chinese names still work), so old boards regenerate without touching a single character.
- Log is reverse-chronological
  Newest on top (`sort_log` reverse=True, both in md and on the page).

## Lesson
- In the usage comment, never start a line with `state:` / `owner:` / `method:`
  The meta parser (parse_q) swallows any line whose first word is one of these — the first draft corrupted the status exactly this way; writing `· state …` dodges it.
- The top four lines are outside the `##`-section required/optional rules
  The first template only marked the `##` sections, so a cold-reading agent had to guess whether state/owner were required. Only after adding them to the usage comment was it clear.
- Stale self-contradictions in the template must be purged
  The template still said "newest Log lines at the bottom" long after reverse order was settled at 1120 — exactly the kind of stale sentence a zero-background reader spots first.

## Glossary
required: without it the Q file is invalid. The generator raises no error, but a block is missing on the page.
optional: if unused, delete the whole section including the heading — leave no empty shell.

## Discussion

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 · Synced with the 260723 redesign: template rewritten (new order · `Items to Finish` / `Where we are` · new `## Boundary` · Question as "paragraph + bullets" · `Why here` retired); required count 7 → 6. state ✅ → 🟡 — the structure changed, the old zero-background fill test no longer counts, must re-run
260723 1450 · Cold-read acceptance: a fresh agent produced a valid card from the template alone; top four lines got required/optional + a `state` legend (in the usage comment, dodging the meta parser)
260723 1445 · Landed `ref/q-template.md`: per-section required/optional, added `## Law`/`## Lesson`, Log reversed; `board-form.md` and `SKILL.md` synced → all four finish lines reached, question SETTLED
260723 1130 · Template gains `## Lesson` (folded, for pitfalls)
260723 1120 · Log switched to reverse-chronological, newest on top (md and page)
260723 1105 · Template gains `## Comments` (inline comments with status)
260723 1010 · Template gains the item syntax (`- short heading` + indented explanation)
260723 0950 · Log lines gain time: `YYMMDD HHMM · what changed`, time optional
260723 0919 · All section names switched to English, template examples synced
260723 0910 · Template gains ## Diagram and ## Log
260722 2330 · Status words replaced the home-made ones with OPEN / PARTIAL / SETTLED / ON HOLD
260722 2325 · JL settled two rules on the spot: titles must be short phrases (≤14 chars), finish lines must be checklists
260722 2310 · Renumbered Q2 → QA2
260722 2255 · Split out of QA1 as its own question
