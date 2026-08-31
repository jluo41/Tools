# QBt1 · Establish a venue-free Seed that survives retargeting

state: ✅ SETTLED · 0.5.3 · eight divisions hold · novelty column + ideation birth certificate
page-type: seed
owner: JL
method: test whether the Page remains valid after replacing the selected venue

## Opening
What must stay true about a paper even when its target venue changes?
Seed holds the paper's identity and its BLUF pitch up front.
Behind them sit the research question, stakes, read scope, the Establishment Board, boundaries, and a bounded Narrative handoff.
It contains no selected desk, venue promise, or manuscript order.

**Where this page sits**: Venue and Narrative add target-specific constraints downstream.

## Writing Style
State the stable research identity in venue-free language.
Mark every factual establishment with evidence or an open obligation.
A pitch sentence selling a finding cites an ✅ E-row or wears its placeholder openly.

## Diagram
**Seed boundary**: stable paper identity feeds several target Narratives.

```text
🌱 Seed ─┬─▶ 🏛 Venue A + 🧭 Narrative A
         └─▶ 🏛 Venue B + 🧭 Narrative B
```

**Lifetimes**: the eight divisions, and which ones are allowed to move.

```text
1 Identity 🔒 · 2 Pitch 🎤 · 3 RQ 🔒 · 4 Stakes 🔒
5 Source Pages 🐢 · 6 Establishment Board 🔥 · 7 Boundaries 🔒 · 8 Handoff ♻️
                         ▲ the only frequently-moving division
a diff outside 🐢/🔥/♻️ = identity drift, visible by construction
```

## Content
### 1 · Seed contract
**Fixed roles**: the eight required divisions of one Seed, in order.

```text
identity · pitch · research question · stakes · source pages
establishment board · boundaries · Narrative handoff
```

The pitch is BLUF, the one-minute story at division 2: hook, the study in a clause, the headline finding, who should care. Placeholders `⟦pending E<n>⟧` are legal until the cited row flips ✅, so the pitch doubles as the paper's progress bar.
The Establishment Board is flat and unranked; each Narrative crowns its own headline, and the pitch's lead is the general listener's, not a desk's.
Since 0.4.0 every ✅/🔨 E-row also carries its novelty reading, so "is this idea any good?" stays a readable column, not a memory.
Since the journey landed, §5's first row binds the paper's `SD00-ideation` page through `pagex/` as a birth certificate, and only the Seed's pen flips E-rows; the Roadmap proposes settles and never writes them.
The handoff carries ids, status, interpretation, and limits rather than copied raw evidence; a Narrative reads §8 and never the Roadmap directly.

## Aims
### A1 · 🌱 Seed contract
- ✅ A1.1 · Seed remains valid across venue retargeting.
  **Done when:** no venue-specific promise or paper order appears in the Page.
  **Now:** The current type contract is venue-free and evidence-bearing.
- ✅ A1.2 · The pitch cannot over-claim silently.
  **Done when:** every selling sentence cites an ✅ E-row or a named placeholder.
  **Now:** The 0.3.0 placeholder discipline makes the check mechanical.


## Files
- `../../paper/workflow-phases/haipipe-paper-seed/SKILL.md` · source contract

## Log
260820 · Replaced the combined Opening type with a stable Seed type.
260821 · 0.3.0 shape ruled by JL: pitch returns venue-free at division 2 as BLUF with placeholders; Establishment splits from Boundaries on the lifetime seam; Source Pages named the PageX seedbed; eight divisions.
260828 · Refreshed to 0.5.3: the eight divisions hold; E-rows gained the novelty column (0.4.0), §5's first row binds SD00-ideation as the birth certificate, and the establish loop fixed the two-pens rule (Roadmap proposes settles, Seed alone flips).

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0