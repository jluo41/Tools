# Delivery Claims: the adjudicated ledger and its campaign
state: 🔴 OPEN
owner: JL
method: state the rung's contract from the shipped claims skill, then raise the settlement bar to JL as the one open ruling

## Opening
What does rung 1c-claims deliver, the K of the ladder, and how deep must its claims settle before the tail may consume them?
The ledger it writes is the only home of a claim's status: supported, weak, or GAP, judged by the author from evidence.
The catch: truth is venue-free but the shipping bar is not, so an sms may ship on lighter settlement than a report.
This page states the ledger's contract and puts the settlement bar in front of JL.

**The words in the question**: rung 1c-claims is the third rung of the venue-free evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice), and its one artifact is `0-lifecycle/1c-claims/1c-claims.md`.
Adjudicated means every status in it was judged by the author from evidence, never copied from a raw number.

**The K of the ladder**: read the four rungs as DIKW: 1a describes the data, 1b finds its patterns, 1c states what generalizes, and 1d turns that into counsel.
K is the knowledge rung, and its whole product is the ledger.

**The tail**: everything that consumes the ledger downstream: rung 1d-advice first, whose entries may only cite claims at or above the bar, then the venue-aligned stages that adopt or decline those entries.

**Settling**: a claim settles when its status traces to a judged artifact, such as a probe answer; how much of the campaign must settle before shipping is the bar part 2 states.

**Covered elsewhere**: how the theme space is mined and which hooks it raises belongs to rung 1b; what advice does with settled claims belongs to rung 1d; pinning the venue that sets the bar belongs to the venue stage, outside the ladder entirely.
This page owns only the ledger between them and the bar the tail reads.

**The precedent**: QB4@paper, the paper board's Value concern, is the closest analog: what must be true, with evidence.
There a stated number binds to the run that produced it; here a stated status binds to the artifact that was judged.

**Why it matters**: an advice entry that cites a GAP claim ships counsel nothing supports, and the settlement bar is the only thing standing between an unsettled ledger and a deployed artifact.

## Writing Style
How this page must be written, so the next editor edits to the same rules.

**Inherited**: the page grammar, section order, and sentence rules come from the board's page contract and `ref/writing-rules.md`, and are not restated here.

**Status words are the skill's own**: write supported, weak, and GAP exactly, plus Rival, Refutes-if, theme hook, and Declined; a synonym here coins a second vocabulary for the one the gate greps.

**Say "judged artifact", never "the data shows"**: the status monopoly is a trace to something reviewed, so any wording that lets a raw number confer `supported` has already broken the rule it describes.

**This page DESIGNS; an intervention's 1c-claims.md SHOWS**: Content states what the rung must deliver for every intervention, not what one intervention holds today.
Where a live ledger differs, that is a finding on that intervention, never a new definition here.

**Language and sentences**: English only, one sentence per source line, no em-dashes.

## Diagram

**The K rung and its bar**: where the ledger sits, and who reads it before shipping.

```text
  🪜 1a ─▶ 1b themes ─▶ 📒 1c CLAIMS ─▶ 1d advice ─▶ 🎪 venue tail
             (hooks)      (the ledger)    (cites ≥ bar)

  📒 sections   Claims · Q-consumer · Evidence Campaign
  🏷 status     supported | weak | GAP · written HERE only
  🚪 bar        light (sms) · medium (email) · full (report)
  🔁 refuted    drop or reword · back to 1b
```

## Content

### 1 · The ledger: three sections, one status monopoly
**The three sections of 1c-claims.md**: what each holds, and the reservoir under Claims.

```text
  📒 1c-claims.md
  ├─ 🏷 Claims              C<n> · theme tag T<n> · role · status · -> PP
  │   └─ 🗂 Declined hooks  hooks passed over · one line + why
  ├─ ❓ Q-consumer           one ## Q-Claim-<n> block per evidence question
  └─ 🗺 Evidence Campaign    dispatch order · dependencies · summary table
```
📌 This part states what the rung's one artifact holds and who may write a claim's status.

Rung 1c writes one artifact, `0-lifecycle/1c-claims/1c-claims.md`, and its Claims section is the ledger.
Each claim is one `C<n>` entry: a short statement, a theme tag naming the 1b theme it came from, a role of primary, enabling, or assumption, a status, and a `-> PP` reference into the probe pool.
Below the entries, Declined hooks records the theme hooks considered and not committed, one line with a why each, and that section is the reservoir the next round re-mines.
The Q-consumer section holds the evidence questions the draft cannot answer itself, one `## Q-Claim-<n>` block each; the probe phase organizes them into `1-probes/` entries, and this stage never runs bank work inline.
The Evidence Campaign section is the dispatch order with dependencies plus the compact summary table, and that table is what the CHECK gate reads.

#### 1.1 · The status monopoly
(supported | weak | GAP is written in this ledger, by the author, and nowhere else)
A claim's status lives only here, per claim and private to the intervention, never in a probe file.
A probe entry carries evidence, the copy of the answering QA file's answer; the judgment stays the author's to write.
A claim is `supported` only when its status traces to a judged artifact, such as a probe answer or an equivalently reviewed result, never to intuition and never to a raw unjudged number.

#### 1.2 · Numbers ride the claim
(verified values land inline with a resolving pointer; there is no sidecar)
A verified number stays inline on its claim with a resolving pointer to the task or discovery result, which remains the source of truth, and there is no `_VALUES_` or `_CITATION_` sidecar.
QB4@paper reaches the same shape for the paper family: there a stated number binds to the run that produced it, and here a stated status binds to the artifact that was judged.

### 2 · Settlement depth: the venue scales the bar, never the truth
**The settlement gate**: the three bars the CHECK gate can hold the campaign against.

```text
  🚪 light    sms · push · reminder   anchors named · stray GAPs allowed
  🚪 medium   checklist · email       primaries supported or weak-with-caveat
  🚪 full     dashboard · report      primaries judged · load-bearing GAPs settled
  🤷 no venue pinned                  light · provisionally
```
📌 This part states who sets the bar, what the gate holds against it, and the one default JL has not ruled.

The ledger is venue-free: retargeting the intervention changes the required settlement and never the ledger's truth.
The CHECK gate reads `claims_settlement` from `STATUS.md` and holds the Evidence Campaign table against that bar.
Under `light`, every claim the artifact leans on is at least tied to a named anchor or common knowledge, and a GAP is allowed when it is not load-bearing; under `full`, every primary is supported from a judged artifact and every load-bearing GAP is settled.
The same bar reaches rung 1d: an advice entry may only cite claims at or above it, which is exactly how an sms ships on lighter settlement than a report.
When no venue is pinned the skill applies `light` provisionally, and whether that default stands is the row waiting for JL in States.

### 3 · Promotion and the sweep: primaries tested to destruction
**The promotion apparatus**: what a 1b hook must gain before it may lead the ledger.

```text
  🪝 1b hook ─▶ 🏷 C<n> entry     or 🗂 Declined line + why
  every primary carries
     🔀 Rival:       the strongest alternative explanation
     💥 Refutes-if:  the result that would FLIP it
  🔍 the sweep       confirm · refute-capable probe · rival explanation
  🔁 refuted         drop or reword · [ROUTE -> themes]
```
📌 This part states the promotion test from 1b and why a refuted claim is a discovery rather than a failure.

Every 1b theme hook is consumed: it becomes a `C<n>` entry or a Declined line with a why, so nothing 1b raised can silently vanish.
The promotion test is refute-capability: a hook may lead the ledger as a primary only when the page can say what would flip it, so every primary carries a `Rival:` line and a refute-capable probe stated as `Refutes-if:`.
The sweep walks each primary through three lenses: does the evidence confirm the claim or merely fail to contradict it, does a probe exist whose result could refute it, and what rival explanation would produce the same pattern.
A claim that survives all three earns its campaign row; a claim that cannot name its rival is untested, whatever its evidence says.

#### 3.1 · A refutation is a discovery event
(the route back to 1b converts a wrong generalization into a new pattern question)
When a landed answer refutes a claim, `--backfill` flips it: refuted means drop or reword, and inconclusive keeps the claim weak or GAP with the caveat recorded.
A claim left with no plausible theme parent signals a 1b gap, so the route is back to re-theme, logged as `[ROUTE -> themes]`, rather than orphan-tagging the claim.
That loopback is the ladder working: the refutation is caught for the cost of a probe, not after the tail has shipped counsel built on it.

## Aims

### A1 · 📒 The ledger
- A1.1 · The ledger's three sections and the status monopoly are stated so a reader can audit any intervention's 1c-claims.md against this page.
  **Done when:** a reader can name, from part 1 alone, the three sections, who may write a status, and what `supported` must trace to.

### A2 · 🚪 Settlement depth
- A2.1 · The settlement bar the tail reads is ruled by JL, not assumed from the skill.
  **Done when:** the Decision Now row is answered, the ruling lands in `## Law` with the unpinned-venue default named, and this Aim's State flips in the same edit.

### A3 · 🔁 Promotion and the sweep
- A3.1 · The promotion test and the three-lens sweep are stated with the route a refuted claim takes.
  **Done when:** part 3 names Rival, Refutes-if, the three lenses, and the `[ROUTE -> themes]` loopback without contradicting the shipped skill.

### P · 🏁 Page-level
- P1 · This page and the shipped claims skill say the same thing.
  **Done when:** every contract sentence in Content traces to the claims skill at 0.7.6, and a divergence is either fixed here or logged as a proposed skill change.

## States

### Decision Now
- [ ] 🗣 Does the venue-scaled settlement gate, including the provisional `light` bar for an unpinned venue, stand as the tail's consumption contract?
      📍 `Part 2` the bar the CHECK gate holds the Evidence Campaign against
      🔔 `Why now` rung 1d and the venue tail both read this bar, and today an intervention with no pinned venue is gated at `light`, so its advice can cite claims that never settled.
      ⭐ `A ·` ratify the gate as the skill ships it: light for sms, medium for email, full for report, and `light` provisionally when no venue is pinned; recommended because it matches claims skill 0.7.6 and keeps early venue-free rounds unblocked.
      `B ·` tighten the default: an unpinned venue fails the 1c CHECK gate until a venue is pinned, so no advice ever derives from a provisional bar, at the cost of forcing the venue decision earlier in every intervention.
      🛑 `Blocks` nothing; the skill's current behavior runs either way.
      🤖 `If nobody answers` A, the shipped behavior stands.

### A1 · 📒 The ledger
- ✅ A1.1 · Met; part 1 states the three sections, the status monopoly, and the judged-artifact trace, all read from the claims skill at 0.7.6.

### A2 · 🚪 Settlement depth
- 🧠 A2.1 · Waiting on JL; the Decision Now row above carries the two options and the recommendation.

### A3 · 🔁 Promotion and the sweep
- ✅ A3.1 · Met; part 3 states Rival, Refutes-if, the three lenses, and the `[ROUTE -> themes]` loopback as the skill ships them.

### P · 🏁 Page-level
- ✅ P1 · Met at creation; Content was drafted directly from the claims skill 0.7.6 on 260802 and no divergence is known.

## Files

### 📋 Contracts
- `../../../../application/_old/1-lifecycle/1c-claims/haipipe-application-claims/SKILL.md`
  The shipped rung this page mirrors; change the ledger's sections or the settlement gate there first, then update this page in the same round.

### 📥 Input files
- `../../../PaperSkillBoard-260725/board.md`
  QB4@paper, the paper board's Value concern; read it for the precedent this page's status-to-judged-artifact binding follows.

## Glossary

- 🪝 **theme hook**: a pattern rung 1b hands up as a claim candidate; 1c must consume every one, into the ledger or into Declined with a why.
- 📌 **PP reference**: a claim's pointer into the intervention's flat probe pool `1-probes/PPNN_<topic>/`, where its evidence questions are bound and answered.
- 🏋️ **load-bearing**: a claim the shipped artifact's counsel actually leans on; the settlement gate treats its GAPs more strictly than a stray one's.
- 🎪 **the tail**: the ledger's consumers downstream: rung 1d-advice first, then the venue-aligned stages that adopt or decline its entries.
- 📄 **QB4@paper**: this page's plain token for the paper design board's Value page, `../../../PaperSkillBoard-260725/board.md`.

## Log

260802 · Page created from the claims skill 0.7.6 and the QB4@paper precedent; the settlement bar, including the unpinned-venue default, raised to JL as the Decision Now row.
