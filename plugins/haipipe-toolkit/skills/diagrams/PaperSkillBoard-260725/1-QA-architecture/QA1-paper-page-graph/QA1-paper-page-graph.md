# QA1 · Follow the paper Page graph from intent to reviewed build

state: ✅ SETTLED · Page-first graph validated
owner: JL
method: compare every live Paper route with the Page that owns its durable decision

## Opening
What is the smallest Page graph that can carry a paper from stable intent to a checked revision?
The graph must preserve identity across venues, give each target its own Narrative, and keep evidence with the Page that uses it.
This Page fixes that graph so the Paper door does not grow another stage runtime.

**Where this page sits**: QA2 assigns ownership at each boundary.

**Why it matters**: if the graph is wrong, Section prose and evidence become competing authorities.

## Writing Style
Use stable Page Type names and show direction of authority.
Keep historical stage names out of the current graph.

## Diagram
**Current Paper Page graph**: the durable artifacts and their feedback path.

```text
🃏 Probe evidence ─┬─ 🔗 PageX
                  └─ 📮 QA Probe

🌱 Seed + 🏛 Venue + evidence
                 │
                 ▼
          🧭 Narrative @ Venue
                 │ one row per reader unit
                 ▼
          📄 Section Pages ──▶ 📦 build ──▶ 🔄 Round
                 ▲                            │
                 └──── checked routed work ──┘

📊 `/haipipe-paper status [family]` = regenerated observation, never authority
   (dropped as a sixth Page Type 260820; see QBt6 archive)
```

## Content
### 1 · Page graph
**Authority flow**: every downstream Page names the upstream version it executes.

```text
identity ─▶ target ─▶ reader order ─▶ prose ─▶ feedback
  Seed      Venue      Narrative      Section    Round
```

Seed is stable and venue-free.
Each selected Venue receives its own Narrative, and each Section executes exactly one current Narrative row.
Round routes accepted feedback to the owning Narrative or Section and records the checked return.
`/haipipe-paper status [family]` is rebuilt from these Pages and cannot close or accept them.

## Aims
### A1 · 🧭 Page graph
- A1.1 · The live graph names one durable owner for every paper decision.
  **Done when:** Seed, Venue, Narrative, Section, and Round have distinct grains and authority.

## States
### A1 · 🧭 Page graph
- ✅ A1.1 · The five current Page Types and their direction of authority are explicit.

## Files
- `../../paper/haipipe-paper/SKILL.md` · public Paper router
- `../../paper/page-types/` · five Page Type contracts

## Log
260820 · Replaced the ten-stage delivery chain with the six-type Page graph.
260820 · Dropped Dash as a sixth Page Type; it survives as `/haipipe-paper status [family]`, a command with no lifecycle or authority (QBt6, archived).
