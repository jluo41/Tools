# QA1 · Follow the paper Page graph from intent to reviewed build

state: ✅ SETTLED · Page-first graph validated · journey 0.6.0 registered 260828
owner: JL
method: compare every live Paper route with the Page that owns its durable decision

## Opening
What is the smallest Page graph that can carry a paper from a ranked idea to a checked revision?
The graph must preserve identity across venues, give each target its own Narrative, and keep evidence with the Page that uses it.
Since 260824 the graph also has a journey: six phases named after their authority pages, gated by `haipipe-paper-workflow`, with the venue bank as a library outside the journey.
This Page fixes that graph so the Paper door does not grow another stage runtime.

**Where this page sits**: QA2 assigns ownership at each boundary.

**Why it matters**: if the graph is wrong, Section prose and evidence become competing authorities.

## Writing Style
Use stable Page Type names and show direction of authority.
Keep historical stage names out of the current graph.

## Diagram
**Current Paper Page graph**: the durable artifacts, the journey that orders them, and the feedback path.

```text
🃏 Probe evidence ─┬─ 🔗 PageX
                  └─ 📮 QA Probe

💭 Ideation ──▶ 🌱 Seed ⇄ 🗺 Roadmap        ↺ the establish loop ·
      G0            │   exits only at G4      E-rows flip on the Seed,
                    ▼                         receipts land on the Roadmap
   🏛 Venue ──▶ 🧭 Narrative @ desk
   (library)        │ one row per reader unit
                    ▼
             📄 Section Pages ──▶ 📦 assemble (a verb, G6) ──▶ 🔄 Round
                    ▲                                            │ G7
                    └──────── checked routed work ◀── Seed/Narrative/Section

📊 `/haipipe-paper status [family]` = regenerated observation, never authority
   (dropped as a sixth Page Type 260820)
```

## Content
### 1 · Page graph
**Authority flow**: every downstream Page names the upstream version it executes.

```text
idea ─▶ identity ⇄ campaign ─▶ reader order ─▶ prose ─▶ feedback
Ideation  Seed      Roadmap      Narrative      Section   Round
                              (Venue = the library Narrative §1 binds)
```

Ideation is the story group's page zero; the repo is minted with it, and the winning idea's `went to` names the Seed.
Seed is stable and venue-free; the Roadmap plans its campaign and registers receipts, and only the Seed writes E-row flips.
Each selected desk receives its own Narrative, and each Section executes exactly one current Narrative row.
Round routes each accepted concern exactly once, to the Seed, the Narrative, or a Section, and records the checked return.
`haipipe-paper-workflow` owns the gates G0–G7 between these authorities and never their content.
`/haipipe-paper status [family]` is rebuilt from these Pages and cannot close or accept them.

## Aims
### Decision Now
- [ ] 🗣 Does a paper board keep one desk group (`B<x>-<desk>` with sections, appendices and rounds together), or split it?
      📍 `Part` the page graph (§1)
      🔔 `Why now` JL 260831, reading the MISQ index: 16 pages sit in `Ba-misq` (SM00-SM08, SA01-SA06, RD01) and the paper's shape does not show; the names `A1-SD-story` / `A2-NA-narrative` / `B<x>-<desk>` are the layout law in haipipe-paper-workflow §layout and in the five page-type skills, and MedJournal uses `Ba-jama-im`, so this is a family ruling, not a MISQ edit.
      ⭐ `A ·` keep the folders and the law; the INDEX and the Pages sidebar render three sub-blocks inside a desk group from the page-id token (S = main, A = appendix, RD = rounds), so the shape shows without a rename. Cost: one renderer change in `src/page_board.py index_rows`, no path moves, no skill text.
      `B ·` rename to `1-SD-story` / `2-NA-narrative` / `3-SM-main` / `4-AM-appendix` / `5-RD-rounds` (one desk = three groups). Cost: eight skills' text (haipipe-paper, -workflow, -assemble, page-for-section/-roadmap/-ideation/-seed/-narrative), PaperSkillBoard QBt3/QBt4/QBt6, both paper boards' folders and `board.md`, 23 live files with the old paths, 3 `pagex/` symlinks, then `feedback.py collect --all`, `requirement.py --all`, `evidence-status.py`, rebuilds and server restarts; every future desk needs three groups.
      `C ·` leave the index as it is.
      🛑 `Blocks` nothing; the index is readable, only flat
      🤖 `If nobody answers` A
      ✅ `Done 260831 1053` A executed under this default clause (JL: "focus on the MISQ Board Design"): haipipe-board 0.150.0 `src/page_board.py index_rows` + `sidebar_rows` cut a paper desk group by page-id token (`SM · main sections` · `AM · appendix` · `RD · rounds`); MISQ and MedJournal rebuilt. Tick B only if the folder rename is still wanted on top; C is now moot.
### A1 · 🧭 Page graph
- ✅ A1.1 · The live graph names one durable owner for every paper decision.
  **Done when:** Ideation, Seed, Roadmap, Venue, Narrative, Section, and Round have distinct grains and authority.
  **Now:** The seven current Page Types and their direction of authority are explicit.
- ✅ A1.2 · The journey orders the graph without owning any content.
  **Done when:** every gate G0–G7 is an assertion over pages that already exist, declared only by a person or CHECK.
  **Now:** Journey 0.6.0 names six phases after authority pages; Venue stays a library, never a phase.


## Files
- `../../paper/haipipe-paper/SKILL.md` · public Paper router
- `../../paper/haipipe-paper-workflow/SKILL.md` · the six-phase gate machine
- `../../paper/workflow-phases/` · six journey-phase skills (haipipe-paper-<phase>), each owning its page-type key
- `../../paper/haipipe-paper-venue/` · the one non-phase Page Type (QBv bank record)

## Log
- 260831 1047 · Decision Now: keep one desk group or split it (JL 260831, MISQ index); CC recommends A, sub-blocks in the index by page-id token.
- 260831 1053 · Ruling A executed by its default clause: haipipe-board 0.150.0 renders SM / AM / RD sub-blocks inside a paper desk group in the index and the Pages sidebar; no folder moved, no skill text changed.
260820 · Replaced the ten-stage delivery chain with the six-type Page graph.
260820 · Dropped Dash as a sixth Page Type; it survives as `/haipipe-paper status [family]`, a command with no lifecycle or authority (QBt6, archived).
260828 · Registered the journey: Ideation and Roadmap join the graph (seven types), P1↔P2 form the establish loop exiting at G4, Venue is a library consulted at P3 §1, and `haipipe-paper-workflow` 0.6.0 owns gates G0–G7. The Collection page of journey 0.5.0 folded into the Roadmap this morning.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0