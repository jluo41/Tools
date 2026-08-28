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
### A1 · 🧭 Page graph
- A1.1 · The live graph names one durable owner for every paper decision.
  **Done when:** Ideation, Seed, Roadmap, Venue, Narrative, Section, and Round have distinct grains and authority.
- A1.2 · The journey orders the graph without owning any content.
  **Done when:** every gate G0–G7 is an assertion over pages that already exist, declared only by a person or CHECK.

## States
### A1 · 🧭 Page graph
- ✅ A1.1 · The seven current Page Types and their direction of authority are explicit.
- ✅ A1.2 · Journey 0.6.0 names six phases after authority pages; Venue stays a library, never a phase.

## Files
- `../../paper/haipipe-paper/SKILL.md` · public Paper router
- `../../paper/haipipe-paper-workflow/SKILL.md` · the six-phase gate machine
- `../../paper/page-types/` · seven Page Type contracts

## Log
260820 · Replaced the ten-stage delivery chain with the six-type Page graph.
260820 · Dropped Dash as a sixth Page Type; it survives as `/haipipe-paper status [family]`, a command with no lifecycle or authority (QBt6, archived).
260828 · Registered the journey: Ideation and Roadmap join the graph (seven types), P1↔P2 form the establish loop exiting at G4, Venue is a library consulted at P3 §1, and `haipipe-paper-workflow` 0.6.0 owns gates G0–G7. The Collection page of journey 0.5.0 folded into the Roadmap this morning.
