---
name: haipipe-novelty-check
description: >-
  Verify an admitted research Idea claim by claim against current literature,
  identify the closest work, steelman rejection and defense, and state the
  remaining delta with honest evidence-depth limits. Use for novelty checks,
  prior-art questions, "has this been done", scoop risk, or contribution
  verification; it does not judge identification credibility or journal fit.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.5"
  last_updated: "2026-09-22"
  capability_family: "2_test"
---

# /haipipe-novelty-check · claim × closest-work verification

Load `haipipe-ideation` and the target Idea Card. For durable work, load
`haipipe-discovery`, Search, Review, and Synthesize; every load-bearing paper
must resolve to a completed Discovery Result, its one-entry Bib, and its
runtime verification receipt. This skill owns the novelty question and
adversarial comparison. Discovery owns finding and reading sources.

For a durable commission, use the owner-bound Run Specs in
`../haipipe-ideation/references/workflow-runs.md`. This capability's checks
are internal Steps unless separately commissioned under that contract.

## 1. Extract the claims

Split the Idea into 1–5 independently testable Core Claims. For each, freeze:

```text
claim                 the proposition whose newness matters
research question     what is being asked
mechanism             why the effect or behavior should occur
identification/setting where and how it is tested
outcome               what is observed or changed
time boundary         searched through which date
```

A project title, fashionable topic, dataset, or model name is not a Core
Claim. Do not let a broad claim hide one preempted subclaim.

## 2. Build the query ladder

For each claim, prepare multiple formulations across these families:

1. exact proposition and distinctive phrases;
2. mechanism synonyms and neighboring theory terms;
3. outcome synonyms plus population/setting;
4. method, identification strategy, dataset, intervention, or shock;
5. backward and forward citation chains from plausible antecedents;
6. recent working papers, preprints, and the field's current top-venue pass.

Durable search obeys Discovery's channel law: preprint plus journal index,
with biomedical, economics, management, or technical channels added as the
field requires. Record every channel as searched, unavailable, or omitted
with reason. Search snippets and model memory are leads, not findings.

## 3. Admit and read the closest work

Resolve plausible overlaps to canonical Subjects and admit them through
Discovery. Review the actual methods, mechanism, setting, and outcomes. The
closest one or two works should be read at full-text depth before a strong
`novel` or `preempted` verdict. When lawful full text is unavailable, keep the
claim `inconclusive` or qualify it `partial`; never infer overlap from a title
or abstract alone.

## 4. Adversarial comparison

For each Core Claim:

1. steelman the strongest evidence-bound rejection that the claim is already
   done or only incremental;
2. steelman the strongest honest defense of a material remaining delta;
3. compare prior work and candidate point by point on the tuple below;
4. reconcile what is new, what is inherited, and what remains unverified.

| Delta component | Closest work | Candidate | Material difference? |
|---|---|---|---|
| research question | | | |
| mechanism | | | |
| identification or setting | | | |
| outcome | | | |

Shared data, topic, or shock does not establish preemption when the mechanism
or outcome differs materially. Conversely, changing only terminology or
applying X to Y does not establish novelty. State scoop risk separately from
verified overlap.

## 5. Verdict and stopping rule

Use the shared statuses:

- `novel`: the material claim survives the closest-work rejection;
- `partial`: a defensible delta remains, but important components overlap;
- `preempted`: verified prior work establishes the material claim;
- `inconclusive`: adequate sources exist but access, conflict, or depth blocks
  reconciliation;
- `unverified`: the required search/review has not been completed.

Stop only when the planned query families and required channels are recorded,
all plausible closest works that could change the verdict are admitted and
reviewed to the available depth, and a final additional query/citation pass
finds no new candidate that changes the comparison. A user-set resource limit
may stop earlier, but the status remains `inconclusive` or `unverified`.

### Confidence anchors and abstention

`confidence` is a claim-level judgment about how well the cited, admitted
literature evidence supports that row's `verdict` within its recorded search
boundary. Its evidence object is the claim's query/channel coverage, closest
Discovery Subjects/Results and actual reading depth, plus the four-part delta
comparison. It does not measure the probability that a claim is novel, the
quality or credibility of its research design, or its eventual impact. Search
volume, model certainty, memory, snippets, and citation counts alone do not
raise confidence. These are qualitative rubric anchors, not probability
estimates; this revision does not claim empirical calibration against
independent reviewer labels or later novelty outcomes.

| Label | Evidence anchor and example |
|---|---|
| `high` | Required search families/channels and final citation pass are complete; every plausible closest work that could change the reading is understood at full-text depth, or the complete search produced no plausible antecedent; each material delta is resolved without conflict. Example: the closest full-text study shares the topic but establishes a different mechanism and outcome, while the candidate's claim-level delta is explicit. Compared with `medium`, no bounded evidence gap remains that could qualify the reading. |
| `medium` | Direct, claim-relevant evidence supports the reading and the closest work is understood, with a named bounded limitation that does not leave a material alternative unresolved. Example: a secondary adjacent work is available only as an abstract, but the full-text closest work resolves the central claim. Compared with `high`, a non-decisive coverage/depth limitation remains. |
| `low` | Some admitted, claim-relevant evidence exists, but incomplete coverage, a plausible unresolved closest work, or a material conflict prevents a stable reading. Example: only abstracts were accessible for a work that may establish the mechanism. Compared with `medium`, the gap could change the claim-level verdict; keep the status `inconclusive` or `unverified` and route the missing evidence. |
| `none` | Neither claim-relevant admitted sources nor completed search-coverage evidence supports a directional reading. Example: the only leads are model memory, snippets, or unadmitted titles. Compared with `low`, there is no usable direct basis even for a tentative reading; this is abstention, not a low-strength verdict. |

Use `confidence: none` only with `inconclusive` or `unverified`; never attach
`none` to `novel`, `partial`, or `preempted`. If a missing source, required
search pass, inaccessible full text, or reviewer conflict could change the
verdict, abstain: use `inconclusive` when the required search found relevant
material but access/depth/conflict prevents reconciliation, and `unverified`
when required search or review remains incomplete. Keep confidence `low` when
some direct evidence exists, or `none` when it does not. Do not convert lack of
prior-art findings into high confidence when the search boundary is incomplete.
Pair `low` only with `inconclusive` or `unverified`; a settled directional
verdict needs the `medium` or `high` evidence anchor.
If reviewers remain divided after review, preserve each raw assessment and
follow the shared resolution protocol; an `undetermined` resolution maps to
`inconclusive` with `confidence: none`. Never convert novelty confidence to
identification credibility or another field's label.

## Output receipt

Update `core_claims[].novelty_check` and write
`workflow/novelty/<idea>_<timestamp>.yaml` using this canonical shape:

```yaml
version: 1
kind: idea-novelty-check
idea_id: i01
assessment_binding:
  mode: owning_run | direct
  assessment_id: "unique id in the owning Task Result or direct call"
  owning_run: "bNN.jNN.tNN/rNN | null"
  evaluator: null  # direct mode: {actor: person/ID or agent/ID, model_or_build: ...}
  criterion: null  # direct mode: {id: haipipe-novelty-check, version: "0.1.4", owner: haipipe-novelty-check}
  input: null      # direct mode: {subject_hash: "sha256:...", manifest_sha256: "sha256:..."}
scope:
  searched_through: "YYYY-MM-DD"
  evidence_boundary: "local-only, full Discovery, or another explicit limit"
  status: complete | bounded | blocked
query_families:
  - family: exact-proposition | mechanism | outcome-setting | method-data | citation-chain | recent-top-venue
    formulations: ["exact query or planned formulation"]
    status: searched | planned-not-run | unavailable | omitted
    reason: "required when status is not searched"
channels:
  - channel: preprint | journal-index | pubmed | medrxiv | field-index | citation-chain | other
    status: searched | planned-not-run | unavailable | omitted
    reason: "required when status is not searched"
candidates:
  - subject: "canonical Subject id/path or lead description"
    result_path: "Discovery Result path or null"
    disposition: closest | related | excluded | unresolved
    reading_depth: none | metadata | abstract | full-text
    reason: "why it received this disposition"
claims:
  - claim_id: c01
    contribution_role: central | supporting
    search_question: "has this exact claim been established?"
    closest_results: ["Discovery Result paths; may be empty"]
    closest_work: "bounded comparison or explicit none verified"
    evidence_depth: none | metadata | abstract | full-text
    rejection_case: "strongest evidence-bound preemption case"
    defense_case: "strongest honest remaining-delta case"
    delta_tuple:
      research_question: "shared/different/unknown plus explanation"
      mechanism: "shared/different/unknown plus explanation"
      identification_or_setting: "shared/different/unknown plus explanation"
      outcome: "shared/different/unknown plus explanation"
    remaining_delta: "material residual or unresolved"
    verdict: novel | partial | preempted | inconclusive | unverified
    confidence: high | medium | low | none
    limitation: "what coverage/depth prevents a stronger reading"
limits: ["assessment-wide limit"]
created_at: "ISO-8601"
```

Each evaluator writes a new immutable raw receipt with its own
`assessment_binding`. For `owning_run`, the evaluator, rubric and input hashes
are inherited through `owning_run` + `assessment_id` from the Task Result. For
`direct`, fill the three direct-mode fields from the shared contract in
`references/receipts.md`. If multiple reviewers assess the same frozen inputs,
retain every raw file and write a same-shape resolution receipt with
`review_resolution`, including when they agree; never edit a
reviewer's original or replace a conflicting claim with a vote. An unresolved
claim stays `inconclusive`, confidence `none`, and HOLD. The Idea Card's
`receipt` points to the current resolution receipt when one exists.

Use `planned-not-run` when a query/channel was required and formulated but the
commission explicitly prohibited execution; use `omitted` only when the
frozen scope did not require it. `bounded` means some required coverage was not
executed or not available, while `blocked` means no meaningful comparison
could be performed. An all-context/no-search assessment therefore remains
`unverified`; it may still preserve planned queries and adversarial reasoning.

Every claim row projects into the matching Idea Card novelty block, including
the receipt path and unchanged evidence_depth. New cards use
none/metadata/abstract/full-text; legacy metadata-only reads as metadata.
No source read means none. The Idea Card stores the conclusion, not copied paper notes.

Novelty is not identification credibility. Report a scientifically new but
poorly identified Idea as novel with a separate pressure-test risk; never
quietly reduce novelty to express design doubt.

## One-off mode

Follow the umbrella skill's one-off source route: reuse verified inputs,
otherwise use Discovery one-off search/read within the request; return links,
access dates and reading depth inline. Keep no-search/read-only restrictions.
Unavailable evidence means provisional/HOLD. Inline work creates no durable
portfolio or source bank unless the user asks to retain it.
Include a complete direct-mode `assessment_binding` in the inline result. If
more than one reviewer is used, retain each raw judgment inline and return the
shared `review_resolution` block; unresolved conflict remains HOLD.

Return the same claim table, search coverage, closest-work comparison,
rejection/defense, verdict, and limitations inline. Cite direct sources. If
full text or a required channel was unavailable, make the confidence limit
prominent.
