# Session reflection · 260727 → 260728 · MISQ §3 Theory and §4 Measurement

Raw material for a later digest. One topic per section, each with the evidence that produced it,
so a digest can decide what graduates into a skill and what was one-off.

**Count: 20 topics.** 14 are JL preferences or rulings about how the work should be done.
6 are findings about the machinery that only surfaced by running it.

Scope of the session: `S-Main-3-theory.md`, `S-Main-4-measurement.md`, `S-Display-0-design.md`,
`S-Display-1a`, `S-Display-1b`, the `displays/` registry, two probe entries, one bank QA file.

---

# Part 1 · JL preferences and rulings (14)

## P1 · Answer at the size of the question
**Rule.** A closed question gets the answer on line 1. Diagrams and tables are for open questions.
**Evidence.** Opening turn: "you know which markdown you are working with?" The wanted answer was
one path. Reinforces an existing memory rather than adding one.
**Lands in.** General response discipline, not a skill.

## P2 · Convention propagates by copying a NAMED sibling, never by invention
**Rule.** When a page's shape is wrong, JL names the page to copy. Go read that page and match it
structurally; do not design a replacement.
**Evidence.** Twice, and the second time because the first copy was still not right:
"where we are are not good, please check S-Main-2" → later "please follow S-Main-3 S Main 3's
where we are, to update your where we are section."
**Lands in.** `haipipe-paper-stage`, `haipipe-board` — an S-page section should name its exemplar.
**Note for the digest.** S-Main-3's shape had itself evolved past S-Main-2's by the second ask
(it gained a fenced `STATE · measured` block). So "copy the sibling" means copy it *now*, not
copy the memory of it.

## P3 · A decision row carries real metadata inline; pointers-only is not usable
**Rule.** A row JL is meant to tick must contain the coefficient, the DOI, the file path, the
exact figure. Pointing at where the argument lives is not enough.
**Evidence.** My first `Where we are` was deliberately pointer-shaped ("these are POINTERS; the
argument stays in its owning item") and was rejected. S-Main-2's rows carry full citations with
DOIs and Scholar links; S-Main-3's carry `coef 3.567201, exact p 0.293, N 200,517`.
**Lands in.** `haipipe-paper-stage` Where-we-are contract.
**Tension worth digesting.** This pulls against "do not duplicate content across pages", which is
the rule that motivated the pointer version. The resolution used here: the row carries the
DECISION plus the facts needed to make it; the ARGUMENT stays in Items to Finish.

## P4 · One short sentence per line inside indented blocks
**Rule.** Indented multi-clause lines render as prose walls in the board.
**Evidence.** Captured mid-session in memory as "indented record blocks flow into prose walls".
S-Main-2's item bodies are one short sentence per line.
**Lands in.** `haipipe-board` page-authoring guidance.

## P5 · `assets/` holds the SELECTED artifact; `versions/` holds the lineage
**Rule.** `float.tex` points at a stable `assets/` path forever. Promoting a new winner means
copying it over that path, never repointing the float.
**Evidence.** "I think the final selected one will go to .../assets, so .../versions/research-model-v2.pdf
could this one got the the assets?"
**Finding that strengthened it.** Not a new convention: 7 of the 9 units already did this, and
`display01a` and `display01b` were the only two reaching into `versions/`. Both are now converted.
**Lands in.** `haipipe-display-*` unit layout.

## P6 · Provenance must be answerable from the folder itself
**Rule.** A reader standing in a unit folder must be able to tell where the shipped byte came from.
**Evidence.** "how do we know where is this figure comes from? maybe have a readme in
examples/.../assets?"
**What was built.** `displays/asset-manifest.py`, writing a generated `assets/README.md` per unit.
Two design choices worth keeping: the block is GENERATED with begin/end markers (the hand-written
unit README had drifted in four separate ways), and provenance is recorded by **hash**, so it is
provable rather than asserted.
**What the audit found on first run.** Only 2 of 12 assets across all units were traceable to any
file on disk; 5 were stale against their own `source/`.
**Lands in.** `haipipe-display-*`, plus a candidate pre-submit check (`--check` exits non-zero).

## P7 · Prefer the published source over recomputation
**Rule.** If a number is a published result of a companion paper, read it there. Do not open the
data to re-derive it.
**Evidence.** I had started inspecting `doctors_df_profile.dta` to recover two counts; JL stopped
it: "don't need to do so, just use the report from the npj DM paper."
**Why JL was right, not just faster.** The two counts were never task outputs, which is why a grep
across the whole `tasks/` tree came up empty. They are results of the companion, stated in one
sentence that also carries the same `wang2022recency` citation the manuscript already had. The
provenance and the citation turned out to be the same source.
**Lands in.** `haipipe-probe` — the T1 whitelist should arguably include the companion paper.

## P8 · Call the skill; do not hand-roll its work
**Rule.** When JL says "call the probe", invoke `/haipipe-paper-probe`. Doing equivalent work by
hand is not the same act.
**Evidence.** The sharpest correction of the session: "I asked you to call the probe to fix this
/haipipe-paper-probe and then revise it, why you didn't do it?" Earlier JL had said "Please try to
do as much as probes you can" and I did the work manually.
**What the skill supplied that hand-rolling did not.** A depth ceiling read from the stage contract
(`probe_depth: 0`); the T1 LOCAL whitelist, which is what actually closed both questions; the
fabrication guard (`grep -F` every value against its named source); required PROOF steps; a
checker; and the boundary that PROBE may not edit prose, which forces a separate REVISE pass.
**Lands in.** The strongest single item for the digest. Worth a memory.

## P9 · Retire settled apparatus to the Log; keep Content lean
**Rule.** Apparatus that narrates a past state belongs in the Log. Only apparatus that BINDS a
marker to its source stays attached to a sentence.
**Evidence.** "could you remove the apparatus which we have fixed? and put the concise version in
the log?" Also the standing memory "keep control-center docs lean".
**The rule as applied.** A lane BINDS · the Log NARRATES · Items to Finish OWNS.
**Measured effect.** Content apparatus went 34 lanes / ~2,095 words → 12 lanes, under ~1,250 words
of manuscript.
**The one push-back.** Verified `> Value:` lanes were KEPT, because the revise-place contract is
explicit that a lane on a verified number is the finished form of a sentence: a number is just
digits, and the lane is the only thing tying it to the run. Stripping it makes a verified number
unverifiable.
**Lands in.** `haipipe-paper-stage`, `haipipe-probe`.

## P10 · Delete what is superseded, rather than keeping it for reference
**Rule.** When a placeholder's real artifact has landed, the placeholder goes.
**Evidence.** "delete this, we don't need this" — the ASCII Table 1 sketch under P5.
**How it was done without loss.** The sketch had been a spec for DR01; DR01 was done and the real
unit shipped the same figures. Three `> JL:` threads inside the deleted block were moved verbatim
to the Log (the page's own precedent), and the one fact the block held alone, that the companion
publishes the mean only and no level shares, moved onto the differentiation ruling it is evidence
for.
**Side effect worth noting.** The block had been inflating P5's measured length: 17 sentences /
~167 words → 6 / ~81 after deletion, finally matching the plan block.

## P11 · The section title belongs inside Content, not only as the page title
**Evidence.** "§4 Measuring Patient-Perceived Physician Traits I want you to add this to the
Content as well, not only the content title."
**Constraint discovered.** It sits at `###`, level with its own subsections, because
`section-stats.py` keys paragraphs on `#### P<n>` and demoting them stops the form block measuring
anything. No sibling S-Main page does this, so §4 is currently the only one.
**Lands in.** `haipipe-paper-stage`; needs a family-wide decision, not a one-page exception.

## P12 · A methods section opens with the study design, then the method
**Evidence.** "I want the first part to describe the whole Study design. and then explain how do we
do the LLM annotation."
**Corroboration found afterwards.** The MISQ methods blueprint already asks for it: "healthcare
papers add a standalone research-context subsection first."
**Two implementation rules that came out of it.** The new paragraph is numbered `P0`, not `P1`,
because nine evidence records cited twelve `Pn.Sn` addresses that a renumber would silently break.
And it states no N, no ICD code, no equation, which both keeps it out of §5's territory and lets
it be written while six value questions are still deferred.
**Lands in.** `haipipe-paper-stage` section-kinds.

## P13 · The Log belongs on the Section Page, in order
**Evidence.** "please update the logs to this Section Page."
**What was wrong.** Six new entries newest-first at the top, then a pre-existing block running
260727 → 260725 → 260727. Reordered to oldest-first with the day's entries in event order.
**Lands in.** `haipipe-board` / `haipipe-paper-stage`.

## P14 · Ask for the explicit finish-list
**Evidence.** "please list the items to do to finish this section."
**What made the answer useful.** Grouping by WHO can act (JL-only rulings · human-only bibtex ·
blocked on deferred probes · owned by another page · mine once unblocked) and drawing the critical
path, rather than listing 21 items flat.
**Lands in.** `haipipe-paper-stage` — a `finish-list` verb would be a real affordance.

---

# Part 2 · Findings about the machinery (6)

## M1 · Depth-0 closes far more than the records assume
**Twice in one session**, both on questions recorded as needing an expensive dispatch:
- The review-corpus funnel: recorded as needing a new task-folder. The counts already sat in
  `A01_build_physician`'s audited run outputs, which nobody had opened. Closed at depth 0.
- What 0.095 measures: recorded as `deferred` at depth-3 on `PP05/QX1`. Answered by a landed
  `displays/` unit, which is on the probe's own T1 LOCAL whitelist. Closed with nothing dispatched.
**Implication.** Before deferring, walk the T1 whitelist and the task tree. A "deferred" state is
frequently a statement that nobody looked, not that the answer is expensive.

## M2 · Two numbers that looked verified were wrong, in two different ways
- **1,114,176** was a digit transposition of **1,141,176**. Caught against an audited log, a
  sha256'd artifact, and a published table. It survived because the only cross-check in the
  paragraph, "about 20%", rounds the same either way (19.89% vs 20.37%).
- **0.095** was the RIGHT number attached to the WRONG quantity. The column is headed
  `Cross-Model MAE`; the sentence called it accuracy and built a deployment decision on it. Six
  models can agree closely and be jointly wrong.
**Implication.** The second class is more dangerous and no checker catches it: correct digits,
correct source, wrong meaning. Only reading the source's own column head caught it. A value lane
should record the REGIME, not just the number and the path.

## M3 · State mirrors rot, and they rot fast
Lanes that copied an S-Display page's state line into a Main page were stale within hours, twice,
and the staleness was only caught by opening the actual render. A parallel session's lanes claimed
a "Model reliabiliity" typo and a panel reading "clinical decision latitude"; the current vector
render has neither.
**Implication.** This is the mechanical argument behind P9. A lane may name a unit and a label; it
should not restate that unit's state.

## M4 · Renumbering a registry silently breaks every consumer
The display registry regrouped to `display<block><letter>` mid-session. Every unit id in
S-Main-4's lanes became a dead path, and `S-Display-3-llm-measurement.md` became `S-Display-2c`.
Nothing failed loudly; the lanes just pointed at folders that no longer existed.
**Implication.** A registry rename needs a consumer sweep, or ids need to be indirected.

## M5 · `section-stats.py` counts `%%` comments as manuscript prose
Its skip list is `(">", "```", "- ", "* ", "#", "|", "$")` and omits `%%`, so the `%% {CC-*}:`
why-comments that REVISE *mandates* inflate the measured word count.
**Measured.** One comment moved P3 from 5 sentences / ~126 words to 6 / ~254, and the section total
from ~1,250 to ~1,378. That is exactly the number the MISQ word-floor rulings turn on, on every
section that goes through REVISE.
**Fix.** One entry in that tuple. Not applied: the file is shared across all papers, so it is JL's
call. **This is the highest-value item in Part 2.**

## M6 · Parallel sessions write the same files
Files changed under me repeatedly: `float.tex` was rewritten between my read and my write;
`assets/figure.png` disappeared between two commands; a second set of display lanes appeared beside
mine; a Log entry about the registry appeared while I was drafting one.
**What worked.** Re-measuring before every write rather than trusting an earlier measurement;
verifying another session's claims against disk rather than adopting them (two were stale);
appending corrections beside their entry rather than overwriting it.
**Implication.** Guidance for multi-session work belongs somewhere explicit.

---

# For the digest to decide

Strongest candidates to graduate into a rule or a memory:
1. **P8** call the skill, do not hand-roll it — the correction JL actually pushed back on.
2. **M5** the `%% ` counting defect — a one-line fix that corrupts a ruling input paper-wide.
3. **P2 + P3** copy the named sibling, and a row carries real metadata — these two travel together.
4. **P9** a lane BINDS · the Log NARRATES · Items to Finish OWNS.
5. **M1** check the T1 whitelist and the task tree before deferring.

Probably one-off, not rules: P1, P11, P13, P14.
