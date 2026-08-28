# QBt3 · Turn Seed and Venue into a detailed Narrative map

state: ✅ SETTLED · 0.5.2 current 260828 · claims carry E-parents · one NA page per desk in its own group
page-type: narrative
owner: JL
method: require exact claims with licensed parents and one executable row per reader-ordered Section

## Opening
How should this paper make its claims in reader order for one selected venue?
Narrative owns the paper's venue decision, claim system, argument arc, reader journey, evidence allocation, and detailed Section map.
Every claim is a selection from the Seed's Establishment Board, never new merchandise.
It does not write final Section prose.

**Where this page sits**: it lives in `A2-NA-narrative/` as `NA<NN>-narrative-<desk>`, one page per desk numbered in arrival order; it reads the Seed's §8 handoff (never the Roadmap directly) and one QBv bank page, then hands one row to each Section.

## Writing Style
Write exact propositions rather than themes.
Name each claim's E-row parent; a role never exceeds what the parent's status licenses.
Make each Section row detailed enough that a fresh writer does not invent the logic.

## Diagram
**The story head and the tellings**: the venue-free head is one group, every telling is its own NA page.

```text
A1-SD-story/                       the venue-free head, one each
├── 💭 SD00-ideation · 🌱 SD01-seed · 🗺 SD02-roadmap
A2-NA-narrative/                   one page per desk, arrival order
├── 🧭 NA01-narrative-misq   claims cite E-rows · binds 🏛 QBv1 via pagex/
└── 🧭 NA02-narrative-jama   a retarget is a NEW NA page, never a rewrite
                 ├─ row 1 ─▶ Section 1     (in that desk's B group)
                 ├─ row 2 ─▶ Section 2
                 └─ row n ─▶ Appendix n
```

Boards laid out under the pre-0.5.0 grammar (narratives inside the SD story group) are grandfathered and migrate only on explicit request.

## Content
### 1 · Narrative contract
**Governing artifact**: one row per Section carries claims, reader state, evidence, displays, moves, transitions, constraints, and risks.

```text
venue decision · claim system · argument arc · reader journey
per-section outline · evidence/display allocation · handoffs
```

The claim law joins the two 0.3.0 neighbors: an ✅ E-parent licenses any role, a 🔨 parent caps the role at provisional, and a claim with no parent is a defect with two exits, add the E-row to the Seed or drop the claim.
Division 1 is the paper's venue decision and binds the shared QBv page through `pagex/`, quoting no desk rule without the binding.
A material row change reopens its Section because current prose never outranks the Narrative map.

## Aims
### A1 · 🧭 Narrative contract
- A1.1 · Narrative provides one complete and versioned execution row per Section.
  **Done when:** every claim and reader transition has a visible landing place and evidence state.
- A1.2 · No claim outruns its license.
  **Done when:** every claim names an E-parent and no peak role rests on 🔨 or ⬜.

## States
### A1 · 🧭 Narrative contract
- ✅ A1.1 · The current contract requires claims and a detailed per-section outline.
- ✅ A1.2 · The 0.4.0 claim law makes the license check mechanical.

## Files
- `../../paper/page-types/haipipe-page-for-narrative/SKILL.md` · source contract

## Log
260820 · Made Narrative the governing venue-aligned paper outline.
260821 · 0.4.0 ruled by JL: Narratives move into `0-SD-seed/` beside the Seed as SD<NN> pages; every claim cites its Seed E-row parent with role capped by parent status; division 1 owns the venue decision and binds the QBv bank page.
260828 · Refreshed to 0.5.2: journey 0.5.0 moved Narratives into their own `A2-NA-narrative/` group as `NA<NN>-narrative-<desk>` pages (SD ids now belong to the story head: ideation, seed, roadmap); a Narrative enters through gate G4 and reads the Seed's §8 handoff, never the Roadmap. The claim law and division-1 venue binding are unchanged.
