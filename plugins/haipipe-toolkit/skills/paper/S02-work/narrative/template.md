# Narrative: <Paper Title>

Date: <YYYY-MM-DD>

The design contract for ONE paper: a one-page, evidence-tracked story. It is NOT a draft of the paper. It mirrors the paper's REAL sections, and the section list comes from the VENUE rather than from this file (JL 260802), and every beat carries a readiness tag wired to the probe pipeline plus an interrogation comment.

How to use: copy this file to `<paper>/0-lifecycle/S01-opening/3-narrative.md`, then replace every `<...>` placeholder. Delete beats you do not need; add beats the paper needs. Keep the readiness legend and the comment vocabulary. A filled real-world exemplar (older .tex form, same structure) lives at `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal/0-lifecycle/S01-opening/3-narrative.tex`.

## Readiness Legend

Each beat gets exactly one tag. The tag couples the beat to its evidence status and routes [PENDING]/[GAP] beats to /haipipe-probe.

- **[READY]** evidence in hand: a confirmed probe or a run we trust
- **[PENDING]** data exists but a render/check/probe is still open
- **[INFER]** an inference: grounded in the evidence, one reasoned step beyond, never measured (no probe will confirm it)
- **[LIT]** rests on outside literature; citation audit pending
- **[GAP]** no evidence yet; needs a probe

Comment vocabulary (attached below each beat, visibly subordinate to it):

- Internal interrogation comment: `↪ <verb> · <role>: <one sharp sentence: why this beat is here / what breaks without it>`. Verb in {keep, add, demoted, cut, added by author}; role in {stakes, validity, contribution, guardrail, safety, defense, mechanism, grounded opener, no-blame anchor, so-what, ...}. Authored by the interrogation subagent, not self-authored.
- External reviewer comment: `↪ <Reviewer> [done|part|open] "<their feedback, VERBATIM; do not paraphrase or compress>" => <how we addressed it, in OUR words>`. Multiple reviewers coexist on a beat; each line carries its own name. A comment with no single home beat stays in the footer ledger, not on a beat.
- Order on a beat that has both: beat text, then internal comment, then external comment.
- Comment style (both kinds): SHORT PLAIN sentences, one idea each. No run-on lines chained by semicolons, no stacked parentheticals. Lead with the action, then the open item. (Same readability rule as the pitch.)

## Spine (throughline)

The whole paper in one breath: an arrow chain from the problem to the so-what. Everything below must serve this line.

<the problem / stakes> -> <the move or signal this paper introduces> -> <the core finding> -> <the so-what / what it is and is not>

Format reminder: each section below = a short story PARAGRAPH (the narrative flow, draft-quality, plain language) + "Key points to cover" bullets behind it. Each bullet = readiness tag + bold label + 1-3 sentences + an interrogation comment.

## Sections: where the list comes from

<!-- RULE: DO NOT copy the four sections below as the paper's section list. They are a FALLBACK,
     used only when no venue blueprint exists yet.

     THE LIST COMES FROM THE VENUE (JL 260802, ruling A).
     · Read `S-Venue-0-venue.md`'s `### Structural Blueprint`. It carries one row per section of
       the target journal, transcribed from that venue's playbook, where each section has its own
       measured `<journal>-<section>/style.md`.
     · Write ONE `## ` section here per section THIS paper writes.
     · A paper MAY SPLIT one venue section into two, and MAY ADD one the venue does not list.
       It records which venue section each one obeys, and why it diverged.
     · The style rules always come from the venue section a section points at, so splitting
       changes the CUT and never the NORMS.
     · `section-edit` reads this file as `units_from:`, so one section here becomes one
       `S-Main-<n>` page. Getting this list wrong gets the manuscript's page list wrong.

     EVERY SECTION CARRIES TWO LINES under its heading:
       venue-section: <the blueprint row it obeys, or `—` when the paper added it>
       Adaptation:    <one sentence: why this paper split, merged, or added it. `none` if it maps 1:1>

     Worked example, MISQ: the venue lists seven sections and the paper writes nine.
       ## Abstract        venue-section: abstract      Adaptation: none
       ## Introduction    venue-section: introduction  Adaptation: none
       ## Literature      venue-section: theory        Adaptation: split; the lineage map is its own section
       ## Theory          venue-section: theory        Adaptation: split; hypotheses argued separately
       ## Measurement     venue-section: methods       Adaptation: split; the construct needs its own defence
       ## Empirical       venue-section: methods       Adaptation: split; design and estimator sit apart
       ## Results         venue-section: results       Adaptation: none
       ## Discussion      venue-section: discussion    Adaptation: none
       ## Conclusion      venue-section: —             Adaptation: added; MISQ folds it into Discussion
     The venue's `appendix` section is NOT written here: an appendix is its own Delivery concern. -->

## FALLBACK sections (use only when no venue blueprint exists)

<!-- RULE: the four below are a generic skeleton, kept so a paper drafted before its venue is
     pinned still has something to fill. Replace them with the venue's list as soon as
     `S-Venue-0-venue.md` carries a Structural Blueprint. Their Flow lines and beat roles stay
     useful whatever the venue: reuse them on whichever section they fit. -->

## Introduction: <what is known, the gap, and the bet>

venue-section: introduction
Adaptation: <none, or why this paper split, merged, or added it>

**Flow:** <known fact> -> <what exists at scale> -> <the precise unmet gap> -> <so we test X>

<One grounded sentence: the broad fact that gives the paper stakes.> <One sentence: the data or signal that makes the question answerable.> <One sentence: the precise gap, then the question we ask.>

Key points to cover:

1. [LIT] **<Stakes>:** <the external fact that makes this matter, with a citation>.
   - ↪ keep · stakes: <why this beat earns its place; the exact link to cite so the stakes do not read as borrowed>.
   - ↪ <Reviewer> [part] "<their comment, verbatim>" => <how we addressed it, in short plain sentences. One idea each.> (example of an external comment threaded onto a beat; delete if unused)
2. [READY] **<The gap>:** <draw the white space precisely: what prior work did and did not do>.
   - ↪ keep · contribution setup: <why this is the strongest Intro beat; what to scope so the contribution is not overclaimed>.
3. [READY] **<Our contribution>:** <the one-sentence reason this paper exists; name any enabling method as enabler, not contribution>.
   - ↪ keep · contribution: <keep the scope tight; keep enabler-vs-contribution clear here, not floated to Methods>.

## Methods: <how we test it>

venue-section: methods
Adaptation: <none, or why this paper split, merged, or added it>

**Flow:** <the cohort/setting> -> <the build> -> <the exposure/measure> -> <the outcomes> -> <the estimator and its honesty>

<One sentence: setting + the measure, flagged as enabler if it is one.> <One sentence: how the analytic sample is built, so it is reproducible.> <One sentence: what we relate to what, and the honesty guardrail (e.g. associational).>

Key points to cover:

1. [READY] **<Setting>:** <population and N; define the unit of analysis in one clause>.
   - ↪ keep · validity: <frames the denominator before any estimate; define the unit or the population is ambiguous>.
2. [PENDING] **<Cohort construction>:** <the build rules, pinned to code; note any number still server-only or unbuilt>.
   - ↪ keep · validity: <the reproducibility spine; until the pending number lands it is a liability, not a strength>.
3. [READY] **<Exposure / measure>:** <the key variable; inoculate against the obvious construct-validity attack>.
   - ↪ keep · validity: <where the construct-validity attack is met; carry the enabler flag explicitly if it applies>.
4. [READY] **<Outcomes>:** <the dependent measures; define thresholds here>.
   - ↪ keep · validity: <ties the test to what makes the result matter; define thresholds where they are first used>.
5. [READY] **<Design>:** <the estimator + key controls + the honesty guardrail>.
   - ↪ keep · guardrail: <carries the honesty (e.g. associational); pre-specify primary contrasts or they read as cherry-picked>.

## Results: <what the data reveal>

venue-section: results
Adaptation: <none, or why this paper split, merged, or added it>

**Flow:** <who is in the sample> -> <the main result> -> <where it concentrates> -> <the high-risk tail> -> <it survives the obvious confound> -> <it holds under the robustness check>

<One sentence: describe the cohort / Table 1.> <One sentence: the headline finding, surprise kept sharp.> <One sentence: where it amplifies and what shape it takes.>

Key points to cover:

1. [PENDING] **<Cohort (Table 1)>:** <who is in the sample and how key variables distribute>.
   - ↪ keep · stakes: <the section cannot open without it; mark PENDING until the table is built>.
2. [READY] **<C1, main>:** <the headline result in one line>.
   - ↪ keep · contribution: <the headline; keep any surprise sharp>.
3. [READY] **<C2, where it concentrates (safety/impact)>:** <the result that carries the venue fit>.
   - ↪ keep · contribution: <present with the pre-specified anchor and one reconciled number set, or it dies on multiplicity>.
4. [READY] **<C3, the tail>:** <the result that converts an average into a consequential claim>.
   - ↪ keep · safety: <this is the beat the venue rewards; lead it over shape detail>.
5. [PENDING] **<Robustness>:** <the check that defends the main result against the obvious "is it just outliers" reflex>.
   - ↪ add · defense: <describe the check, not its outcome; once run it flips to READY>.
6. [GAP] **<Mechanism split>** (parked, not in Results): <the decomposition that needs a probe before it can be claimed>.
   - ↪ cut from Results · mechanism: <why it is invalid to assert now; it returns as a Discussion mechanism beat after the probe>.

## Discussion: <what it means>

venue-section: discussion
Adaptation: <none, or why this paper split, merged, or added it>

**Flow:** <finding restated> -> <most plausible explanation, no blame> -> <what it means in practice> -> <what the result is good for> -> <what it cannot claim>

<One sentence: restate the principal finding, no new numbers.> <One sentence: the most plausible reading, framed as plausible not proven.> <One sentence: the practical / bedside / field implication.> <One sentence: the so-what plus the honest scope of the evidence.>

Key points to cover:

1. [READY] **<Principal finding>:** <the restated headline a Discussion opens on; pure summary, no new numbers>.
   - ↪ add · grounded opener: <the grounded anchor before any interpretation>.
2. [INFER] **<Mechanism>:** <the most plausible explanation; cite the supporting literature here only>.
   - ↪ keep · guardrail: <phrase as "most plausible reading," never as established; this beat owns the relocated mechanism literature>.
3. [INFER] **<Implication / so-what>:** <what a reader should take away>.
   - ↪ keep · so-what: <the so-what must be in the sentence itself, not implied>.
4. [READY] **<Limitations>:** <the honest list: design limits, construct limits, confounds the main claim must pre-empt>.
   - ↪ keep · guardrail: <mandatory; the limitation that pre-empts the strongest confounding attack goes here>.
5. [PENDING] **<Multiple comparisons / other reviewer rejection vector>:** <the honest accounting of the most predictable rejection vector at this venue>.
   - ↪ add · guardrail: <pairing the honest burden with the pre-specified anchor is what lets the peak claim survive it>.

## Footer Ledger

The cross-cutting ledger. Reviewer-flagged gaps thread back into the beats above; the Arc states how the spine's peak claim is defended; Awaiting review names beats that still need an independent interrogation pass. External reviewer comments live ON their beats above; the footer only carries comments with no single home beat (e.g. "see comments in Overleaf").

- **Reviewer-flagged gaps:** <list each known reviewer concern and where it is now threaded (which section beat), or mark it Remaining and route it to a probe/computation>.
- **Arc:** <one line: after the demotions/parks/folds above, what does each section land on, and how is the spine's peak claim defended>.
- **Awaiting review:** <any beat authored since the last interrogation pass that still needs an independent keep/move/demote/cut verdict>.
- **External review (<name>, <date>):** <one line pointing to the threaded reviewer comments above + any comment that has no home beat (e.g. "see Overleaf"); source file path>. One line per reviewer.


Q-consumer
----------
<!-- RULE: logical source for Board `## Aims`: every question the arc raises becomes
     one `- P<n> · Q-Narrative-<n>` Aim record there.
     · STAGE-PREFIXED ID — `Q-Narrative-<n>`. Each stage owns its own index (Q-Seed-<n>, Q-Claim-<n>, …) so a cited id is never ambiguous across stages. The id in the heading and the id in the inline anchor are THE SAME TOKEN.
     · ANCHORED, not detached — every question spot-checks a SPECIFIC beat above; cite its id inline in the beat(s) it hangs on, e.g. [Q-Narrative-1]. One question may be cited from several beats.
     · A BEAT THAT EXPOSES AN EVIDENCE GAP RAISES A QUESTION HERE — it never gathers the evidence inline. The arc COMPOSES; it does not collect.
     · A beat tagged [PENDING] or [INFER] whose readiness depends on an unlanded fact must carry a question; that is what makes the tag auditable.
     · Description = what the question wants to know. Reason = every beat it is cited from + what happens to the arc if that beat's assumption is wrong. Answer = empty in DRAFT; PROBE fills it from the answering QA file.
     · The loop closes at REVISE: the answer is woven back into every beat citing [Q-Narrative-<n>], the readiness tag is re-evaluated, and the bracket is discharged. -->

- P<n> · Q-Narrative-<n> · <question title>
  **Done when:** The answer has landed, been interpreted, and been woven into Content.
  **Description:** <what the question wants to know — one sentence per line>
  **Reason:** <which beat(s) above cite this id, and what happens to the arc if that beat's assumption is wrong>
  **Probe:** not opened yet
  **Answer:** <empty in DRAFT — PROBE fills it from the answering QA file, anchored [source: PPnn]>
