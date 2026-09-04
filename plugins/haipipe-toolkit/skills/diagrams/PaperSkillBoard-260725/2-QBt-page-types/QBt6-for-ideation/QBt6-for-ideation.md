# QBt6 · Rank a direction's ideas before any Seed exists

state: ✅ SETTLED · 0.5.4 · source reports' own structure · QBt6 id re-minted after Dash
page-type: ideation
owner: JL
method: keep every idea, eliminated or sent, on the one page the repo is minted with

## Opening
Where do a research direction's ideas live before a paper exists to hold them?
Ideation is the story group's page zero (`SD00-ideation`), minted with the repo before any Seed.
It generates and ranks ideas, novelty-checks them, records pilots, then eliminates each one or sends one to a Seed.
Eliminated ideas stay forever; the page is the direction's memory, not a scratchpad.

**Where this page sits**: journey phase P0; gate G0 is the door to the Seed, and the Seed's §5 first row binds back to this page as a birth certificate.

**Why it matters**: without a page zero, the "why this paper" evidence scatters into chat logs and is unrecoverable at review time.

## Writing Style
Mirror the source reports' own field names (IDEA_REPORT / Novelty Check Report headers); coin nothing.
Rank ideas and keep each one's method, hypothesis, minimum experiment, risk, and recommendation as the report wrote them.

## Diagram
**Page zero and its exit**: ideas are cheap and disposable; the send is gated.

```text
💭 SD00-ideation
├── Direction · Ideas (ranked, one source bullet per IDEA_REPORT)
├── Idea 1 · Idea 2 · … (rank order, report fields verbatim)
├── Eliminated Ideas (kept forever) · Suggested Execution Order
│
└── G0: per-claim novelty bound to QA files · pilot or waiver ·
        a person's PROCEED tick
        └─▶ `went to` names 🌱 SD01-seed (or a sibling repo's Seed)
```

## Content
### 1 · Ideation contract
**Fixed grammar**: division 1 is Direction, division 2 is the ranked Ideas index, one division per idea in rank order, Eliminated Ideas and Suggested Execution Order close the page.

```text
direction · ranked ideas · idea divisions (report fields)
eliminated ideas · suggested execution order
```

Each idea division carries the report's own fields: Method, Hypothesis, Minimum experiment, Expected outcome, Core Claims, Pilot result, Risk, Reviewer's likely objection, Recommendation.
Gate G0 is tested on the idea's summary row alone: novelty per claim bound to QA files, a pilot result or explicit waiver, and a person's PROCEED (or PROCEED WITH CAUTION with the risk accepted in the tick).
The receipt is recorded after the act: the Seed exists in `A1-SD-story/`, its §5 first row binds this page back, and the idea's `went to` cell names it.

## Aims
### A1 · 💭 Ideation contract
- ✅ A1.1 · Every idea the direction ever weighed remains readable on one page.
  **Done when:** eliminated ideas keep their divisions and the winning idea's `went to` resolves.
  **Now:** The 0.5.0 shape adopts the source reports' own structure, so nothing is re-summarized.
- ✅ A1.2 · No idea reaches a Seed without its G0 evidence.
  **Done when:** the summary row shows per-claim novelty, pilot or waiver, and a person's tick.
  **Now:** G0 has fired live (2 boards; one CHECK routed HOLD), per the family status of 260828.


## Files
- `../../paper/workflow-phases/haipipe-paper-ideation/SKILL.md` · source contract
- `../../paper/haipipe-paper-workflow/SKILL.md` · gate G0 and the P0 phase

## Log
260828 · Specimen minted during the field repair. The QBt6 id previously named Dash, retired 260820; its archive folder was deleted 260822 under retired-means-deleted, freeing the id. Ideation entered the family with the journey (260824, 0.4.x→0.5.4): page zero, minted with the repo, G0 to the Seed.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0