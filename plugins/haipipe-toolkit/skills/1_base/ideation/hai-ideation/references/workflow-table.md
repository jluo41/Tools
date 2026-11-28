# Ideation capability and owner-route table

The executable Workflow Run Spec list is [workflow-runs.md](workflow-runs.md).
This table maps capabilities and gates to those Runs; its I labels are not
Workflow nodes. The numbered stage names are capability vocabulary, like Discovery's
Search/Review/Synthesize; the numbered folders on disk hold vendored originals
only. They do not replace the durable BJTR address
and never allocate a Run by themselves. New Idea Jobs use assessment Tasks
and shared soft Runs; see [idea-block.md](idea-block.md).

References to a P0 working view in this table apply when a Paper is bound or
explicitly requested. A new Idea Job can remain unbound through selection;
its exact I2 semantic revision and scientific/human gates still apply.

| ID | Capability family | Purpose | Canonical writes | Owner execution | Exit | Human gate |
|---|---|---|---|---|---|---|
| `I1` | `1_generate` | Freeze the direction and evidence population; generate, deduplicate, and admit diverse candidates. | `ideation.yaml`, bundle, Direction Card, `iNN` Idea Cards, Paper sync revision | `hai-ideation generate`; missing evidence routes to Task/Discovery; Paper working projection routes to `hai-paper-ideation` | Every admitted card has a falsifiable claim, method, minimum experiment, expected/failure reading, Core Claims, and provenance; novelty remains unverified; the evergreen P0 cockpit can display the current landscape and portfolio while released Content may remain stale until Page release | Resolve a material scope ambiguity when needed |
| `I2a` | `2_test/novelty` | Test every Core Claim against verified closest work. | Idea Card novelty blocks plus a novelty receipt | `hai-ideation novelty-check` → Discovery Search/Review/Synthesize | Each live claim is `novel`, `partial`, or `preempted`; inaccessible or insufficient evidence stays `inconclusive`/`unverified` | None |
| `I2b` | `2_test/pressure` | Test falsifiability, construct/identification risk, data access, ethics, and the minimum experiment. | Pressure receipt plus feasibility block | `hai-ideation pressure-test` → Task/Run when computation is required | Pilot is positive/negative or a reasoned waiver exists; fatal assumptions and repair paths are explicit | Release new computation when required; accept risk only at Select |
| `I2c` | `2_test/journal-fit` | Broad-screen all admitted cards and deep-fit live finalists. | one Venue Fit Card per Idea | `hai-ideation journal-fit` → Discovery + current Venue contracts | Broad screen is complete for all; each live finalist has an evidence-bound deep fit or visible HOLD | None |
| `I2d` | `2_test/nature` | Apply a Nature-family editorial overlay to named Nature candidates. | Nature review receipt linked from the Venue Fit Card | `hai-ideation nature-paper-review`; current rules still come from Venue | Editorial shape, required upgrades, specialist reroutes, and rule gaps are explicit | None |
| `I2` | `2_test` | Reconcile I2a–I2d into one per-Idea test matrix without a composite score. | card/test-matrix updates and refreshed Paper sync revision | `hai-ideation test`; P0 working projection remains `hai-paper-ideation` | Every live Idea has truthful novelty, feasibility, and venue states; missing work has an owner route; the same P0 cockpit shows additions, changes, merges, dispositions, and evidence gaps; released Content/delivery are current only after the Page release barrier | None |
| `I3` | `3_select` | Compare the portfolio, preserve eliminated history, record the sole human decision, and package selected idea-target pairs. | sync `portfolio_recommendation`, selection receipt, card states, `handoff/paper-ideation.yaml` | `hai-ideation select`; Paper only projects the receipt | Every selected Idea has one target/category, current Venue contract, accepted risk, and distinct Story route | Required: select, defer, or abandon |

## Owner routes

```text
external prior work  hai-ideation → hai-discovery-search
                                        → hai-discovery-review
                                        → hai-discovery-synthesize
                                        → verified Result/Card/Bib pointers

internal feasibility hai-ideation → reuse Task Result
                                      or hai-task + hai-run
                                      → Task-owned pilot receipt

venue facts          hai-ideation journal-fit → hai-paper-venue
                                         → current versioned contract
```

Search calls and card/matrix updates are Steps or bookkeeping. New Idea
Jobs organize independently closable assessment questions as Tasks with soft
assessment Runs. Source acquisition and pilots stay in Discovery and Work.
Legacy portfolio commissions retain their original Task-owned Runs.
A specialist invocation or receipt alone never allocates another Run.

## Gate assertions

`I1 → I2` requires:

- a frozen direction and pointer-based evidence bundle;
- one stable `iNN` Card in each new Idea Job (legacy Task portfolios may hold several);
- a falsifiable proposition, method, minimum experiment, expected outcome,
  failure interpretation, and Core Claims on every admitted card; and
- no generated statement presented as an established novelty finding.
- a pointer-only Paper sync packet exposing the Discovery Landscape,
  Opportunity Map, and complete candidate set without selection fields.

`I2 → I3` requires:

- claim-level novelty records with exact search questions and closest-work
  lineage;
- novelty and identification credibility reported as separate axes;
- a Task-owned feasibility receipt or reasoned waiver;
- a retained broad venue screen for every admitted card;
- current Venue contracts for every deep-fit finalist; and
- every HOLD, contradiction, fatal assumption, and reroute preserved.
- the current Test Matrix and machine-only portfolio reading synced to a bound
  Paper P0 working revision when present; a new Idea Job can remain unbound.
  A changed sync revision does not itself publish Page Content or delivery.

`I3 → Paper P0` requires:

- a dated versioned human receipt with one row per reviewed candidate; only
  explicit answers select, defer or abandon; unanswered rows remain open;
- one selected target/category and accepted-risk record per selected card;
- a distinct linked Paper Block and Story route for each selected Idea Job by
  default; legacy Paper portfolios keep their existing Story routes;
- direct paths to cards, owner Results, Venue Fit Cards, and Venue contracts;
  and
- a pointer-only handoff that copies neither evidence nor desk rules.
- one authoritative I3 selection receipt; Paper P0 only projects its verdict,
  target, and `went to` values.
