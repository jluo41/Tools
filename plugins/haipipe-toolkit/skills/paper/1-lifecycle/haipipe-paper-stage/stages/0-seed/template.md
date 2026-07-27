<!-- TEMPLATE (follow, don't ship). Fill 0-lifecycle/0-seed/0-seed.md from this skeleton: replace every <…>, and each `<!-- RULE: … -->` comment is guidance to FOLLOW then DELETE — a RULE comment must never appear in the finished seed. Delete this top line too. -->
0-seed: <working title>
========================

Date: YYYY-MM-DD
Status: DRAFT


Seed Question
-------------
<!-- RULE: ONE paper-shaped question, venue-free. Split a run-on into a primary sentence + a secondary boundary-condition sentence. -->

<The single paper-shaped question this seed exists to answer.>


Motivations
-----------
<!-- RULE: puzzle / gap / surprise, then why-now, then name each audience and why it cares. One sentence per line. A sentence a question hangs on carries that question's id in a trailing bracket, e.g. [Q-Seed-1]. -->

<Why is this interesting: the puzzle, the gap, or the surprise.>
<One sentence per line.>

<What makes the angle novel or feasible now.>

<To whom is it interesting: name the audiences and why each cares.>


Landscape
---------
<!-- RULE: what others are already doing on this topic — the field map that frames the questions, a few lines (not a full related-work). Where it stakes a novelty/gap claim, cite the question that tests it, e.g. [Q-Seed-1]/[Q-Seed-2]. Sourced from the seed's novelty/landscape feasibility probe; oriented intuition in DRAFT, confirmed and woven at REVISE. -->

<Closest prior work on this topic, and where the gap this paper occupies is. One sentence per line.>


Tentative Claim Shape
---------------------
<!-- RULE: H1 (core) + H2/H3 (secondary), every hypothesis HEDGED (a hypothesis, not a finding). Associational language; name the cited enabler and disclaim blame. An H-line a question hangs on carries its [Q-Seed-<n>] bracket too. -->

**H1 (core, hedged).**
<The core hypothesis, phrased as a hypothesis, not a finding.>

**H2 (<role>, hedged).**
<Any secondary shapes the paper may take, still hedged.>


Q-consumer
----------
<!-- RULE: logical source for Board `## Items to Finish`: every question the draft raises becomes
     one `- [ ] 🔎 Q-Seed-<n>` checklist record there, never a Content heading.
     · RAISE FREELY — as many questions as the draft needs; asking is cheap. When a sentence rests on something no existing question tests, PROPOSE A NEW ONE rather than leave it unanchored. No question shape is disqualified from being asked here.
     · DISPATCH NARROWLY — PROBE handles feasibility-shaped questions (novelty, external-data-obtainability) within the invocation's depth ceiling. Anything else stays here with `Answer: deferred -> RESOURCE` and a `[FORWARD -> RESOURCE]` pointer in this S page's `## Log`.
     · STAGE-PREFIXED ID — `Q-Seed-<n>`. Each stage owns its own index (Q-Claim-<n>, Q-Pitch-<n>, …) so a cited id is never ambiguous across stages.
     · ANCHORED, not detached — every question spot-checks a SPECIFIC assertion above (Seed Question / Motivations / Landscape / H-line); cite its id inline in the sentence(s) it hangs on, e.g. [Q-Seed-1]. One question may be cited from several sentences/sections — that is how it links to more than one place.
     · Description = what the question wants. Reason = every anchor it is cited from + why each matters if that assertion is wrong (the back-link). Probe = the pointer to the ENTRY that carries this question, `→ 1-probes/PP<nn> · QX<n>` (DISPATCHED questions only; a DEFERRED one has no entry, so it writes `--`). Answer = empty in DRAFT; PROBE fills it from the answering QA file.
     · The loop closes at REVISE (not PROBE): the answer is woven back into every sentence that cites [Q-Seed-<n>] (Landscape included), and the bracket is discharged. Born from content (DRAFT drops the bracket in), dies into content (REVISE discharges it). -->

- [ ] 🔎 Q-Seed-<n> · <question title>
      **Description:** <what the question wants to know — one sentence per line>
      **Reason:** <which Motivations / Landscape / H-line(s) above cite this id, and why each matters if that assertion is wrong>
      **Probe:** not opened yet
      **Answer:** <empty in DRAFT — PROBE fills it from the answering QA file, anchored [source: PPnn]; a question the gate DEFERRED reads `deferred -> RESOURCE`; on a loopback redo, prior-cycle resolution + source>
