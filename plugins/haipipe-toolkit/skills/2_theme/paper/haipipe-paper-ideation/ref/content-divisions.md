What each Content division of the Ideation Page holds, from the Discovery Landscape to each Idea's division and its Core Claims; moved from SKILL.md.

## 🔎 Discovery Landscape and Opportunity Map

Division 2 answers what the field currently establishes; division 3 answers
what that evidence leaves worth pursuing. Keep the distinction visible:

```text
Discovery Landscape                         Opportunity Map
accepted evidence and its limits            Ideation's bounded interpretation
direct physician work vs analogues          one durable opportunity id
convergent signals and contradictions       evidence ids + affected Idea ids
unresolved territory and reading depth      open · narrowed · exhausted · contradicted
```

The Landscape projects `discovery_landscape` from the current sync. It may
summarize an accepted Discovery synthesis Page and direct evidence ids, but it
cannot turn an unverified source, search hit, or copied Bib entry into support.
The Opportunity Map projects `opportunity_map` without adding new openings by
Page-author intuition. When new evidence narrows or contradicts an opportunity,
the affected Idea rows and divisions change on the same sync revision.

## 📊 Ideas (ranked) · division 4

The summary table, one row per admitted Idea, every cell a state and never a
blank:

```text
id  idea (the research question)                                     novelty      pilot      venue fit      verdict     target       went to
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
i01 Does a physician's <trait>, read from patient reviews,           partial      ✅ Result   strong · vfit  ✅ PROCEED  JAMA · Art.  StoryA-<desk>-<idea-slug>
    predict <outcome> beyond the star rating?
i02 How many fabricated physician names does an NPI registry check   ⬜ unchecked —          ⬜ pending     ⬜ open     —            —
    remove, and how many real ones does it lose?
i03 ⬜ unframed · card has a title and a claim, no question           ⬜ unchecked —          ⬜ pending     ⬜ open     —            —
```

The `idea` cell is the card's research question, one sentence ending in `?`,
never the handle. An `unframed` row says so in that cell and owes no division.

Verdict vocabulary is projected from the I3 receipt: `⬜ open`, `✅ PROCEED`,
`⚠️ PROCEED WITH CAUTION` with named accepted risk, `❄️ DEFER`, and
`🚫 ABANDON`. Before I3 every row remains open regardless of the machine
recommendation. An abandoned, merged, or deferred Idea is also recorded in the
disposition table with its reason; its summary row and admitted Idea division
stay as history. A `—` cell
is legal only where the authoritative state makes the column moot; on a live
row every cell is a state or a bound path.

For current work, the source block names the exact
`projection/paper-ideation-sync.yaml`, `sync_revision`, Ideation task address,
Direction Card, and evidence bundle. A final selected view also names
`handoff/paper-ideation.yaml` and its `workflow/selection.yaml`. Legacy
IDEA_REPORT or `ideas.md` inputs remain readable, but a new Page does not bypass
the adapter and let ideas appear from nowhere.

The row order supports comparison and attention only. The first row is not
automatically selected, and the page may end with no selected idea, one
selected idea, or several selected ideas. The I3 human receipt and `went to`,
not position, record selection; several selected rows route to distinct Stories.
For every admitted row, `venue fit` is a state backed by its Idea × Venue Fit
Card. A selected row also names the person's target and article/category;
machine recommendations stay inside the idea division.

## 📮 Next Evidence Queue and execution order

Division K+6 groups every unresolved item by its native next owner: Discovery
for external evidence, Task for a pilot or internal fact, Venue for a current
desk contract, or Ideation for Generate/Test/Select work. Each row names the
sync gap or Idea `next_route`, the exact card or opportunity it affects, and
the Result/receipt condition that would close it. It creates no Paper-local
execution Run.

Division K+7 projects `portfolio_recommendation` as the suggested attention
order and labels it machine-authored. Before I3, G0 readiness is only a gate
reading and every verdict/target/Story cell remains open. After I3, the Page
adds only the selected routes found in the final handoff and leaves deferred or
abandoned history visible.

## 🧾 Each Idea's division · one card under evidence

One division per admitted card, headed `Idea <n>: <research question>`, the
question verbatim from the card. It projects the card, Test Matrix, fit card,
and owner receipts without rewriting their conclusions. Every field below is
written relative to the question, so a reader who stops after the first line
still leaves with something to think about:

```text
Research Question             the question this Idea asks, verbatim from the card ·
                              first field, same words as the heading · ends in ?
Origin / Opportunity          which Opportunity Map row raised or changed the question
Hypothesis                    the anticipated answer, one sentence
Method                        how we would answer it, 2-4 concrete steps, plain language
Minimum Experiment            the smallest run that would move the answer
Expected Outcomes             what a yes, a no, a null, and a failed run each mean for the answer
Discovery Basis               direct work, analogues, convergence, contradiction, and open gap
Core Claims / Novelty Check   what an answer would let the paper claim: one line per claim
                              plus its exact search question,
                              closest verified work, remaining delta, limitation,
                              and novel/partial/preempted/inconclusive/unverified status
                              📮 → /haipipe-ideation novelty-check + Discovery Run/Result
Counterevidence               the strongest evidence-bound alternative or rejection
Pilot Result                  POSITIVE/NEGATIVE/WAIVED/PENDING/HOLD + the receipt
                              📮 → task-layer Run/Result, or an explicit waiver
Journal / Venue Fit           broad screen for every admitted idea; deep fit
                              for live finalists; candidate targets, article
                              type, desk risks, missing evidence, reroute,
                              current Venue contract, and machine recommendation
                              📮 → /haipipe-ideation journal-fit
Risk                          what could sink it
Reviewer's Likely Objection   the strongest counterargument
Recommendation               the sync packet's machine-only recommendation
Next Evidence Action         exact Discovery, Task, Venue, select, defer, or abandon route
```

A retrofit page fills only the fields its receipts support and marks the rest
`⬜`; inventing history is worse than a visible blank.

For retrofit novelty, split a flat Core Claims block only where the inherited
text already states distinct claims. Reuse an archived Result only when its exact
question tests the matching claim; otherwise print `unverified` and route a
new Discovery check. Do not convert one old blob-level novelty verdict into
several claim-level passes.

## 🔬 Core Claims, checked one by one

An idea is never novelty-checked as a blob. Its division states 1-5 Core
Claims that would need to be novel; each claim is checked separately and the
table's novelty cell records the Test Matrix reading supported by the worst
claim:

```text
claim → multi-source search (≥3 query shapes · recent-years window)
      → closest prior work + the delta, per claim
      → every cited prior work verified by id/DOI before it enters the page
```

The visible claim table preserves the semantic executor's fields:

```text
claim · search question · closest verified work · remaining delta · limitation · status · Result path
```

"Applying X to Y" is not novel unless the application would reveal a
surprising finding; when the method is not novel but the finding would be, the
division says so explicitly. A prior-work citation that cannot be resolved is
written `[UNVERIFIED]`, never silently trusted. (Discipline adopted from the
ARIS `novelty-check` reference and from this workspace's own
fabricated-citation incidents.)
