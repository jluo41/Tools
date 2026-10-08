Release: one version of the Prototype, from proposals to a signature
=====================================================================

(b11 s00 · s21 phase 3, 261008.) A release is one Job of the Prototype, `tasks/Prototype-bNN-<Topic>/jNN_pN_<slug>/`:
the questions asked in it, their scripts, the cuts and the thresholds, frozen once a person signs it. Every Board Job
runs exactly one signed release (insight-ladder.md rule 1). This file is the release's contract; the ladder is
[insight-ladder.md](insight-ladder.md), the question file and the script are
[block-contract.md](block-contract.md) § The question file and § The script.


The life of a release
---------------------

```text
proposals/<slug>.md  ── run-triage-proposals-pN ──▶  a batch: each taken (taken-in: pN), declined (why), or left open
        │
        ▼
jNN_pN_<slug>/       ── run-open-version-pN ──▶  every question of the newest release kept and pointed back;
                                                 partitions.md, thresholds.yaml, src/ copied
        │  apply the batch:  new question → run-ask-<l><nn>  ·  fix → change  ·  retire → retire  ·  cut → run-set-cuts
        ▼
each new or changed question:  run-plan-evidence → run-review-plan (another agent agrees)
                               → run-write-script → run-review-script (another agent)
        │
        ▼
run-review-questions-pN (Q1–Q7, another agent; a person signs a change)  ·  run-set-cuts-pN (a person signs the cuts)
        │
        ▼
run-sign-release-pN  (a person signs: signed: ✅ <YYMMDD>, state: closed)  ──▶  frozen; a Board may now run it
```

`insight_ladder.py` makes each step's folders and refuses to skip a gate; `haipipe-insight-question`
`scripts/proposals.py` records the triage.


release.yaml
------------

```yaml
release: p2                       # the id; it stays pN in faces, Run names and every Board Job that pins it
questions:                        # every question asked in this release, in tNN order
  D01: {task: ../j01_p1_<slug>/t01_D01_<slug>, change: kept}          # kept: its Task lives in an earlier release
  I01: {task: t02_I01_<slug>, change: "changed: <what, one line>"}     # changed: carried here under the same tNN
  I04: {task: t06_I04_<slug>, change: new}                             # new: asked first here
retired:                          # left out of this release, never asked again under the same id
  K02: <why, one line>
```

A kept question's Task is never copied: the Board Job reads it where it lives. A changed question is carried forward
(`insight_ladder.py change`), keeps its `tNN`, and its `agreed:` resets until another agent agrees it again; its
`changes:` list in question.md says what changed in which release. A question id is never reused, a retired one
included. The release's face (`jNN_pN_<slug>.md`) carries `release · state · signed · from` (the release it opened
from) and, for a carried Block, `carried-from`.


The cuts
--------

The cuts are part of the plan, set in the release before any outcome is seen (`run-set-cuts-pN`, a person signs them),
and never on a Board: a Board proposes a cut (`run-propose-cut-<slug>`), and the next release takes it or not.

```yaml
---
partitions:
- {name: full, where: [], why: every row}                 # required, unfiltered, the template
- name: <name>                                            # one lower-case word, unique, never meta
  where: [{column: <col>, lte: <value>}, …]               # eq · ne · lt · lte · gt · gte · isin · notin · notna
  why: <why this subgroup is asked about>
- {name: cross, of: [<name>, <name>], why: one test of the difference}
---
```

1. **A cut's place is its Run's number.** A Board Job's hard Run `rNN_<partition>` takes NN from the cut's place
   in `partitions.md`; adding a cut at the end renumbers nothing.
2. **`cross` holds no rows of its own.** A cross Run receives the listed cuts and tests their difference once. A
   per-cut page never carries a cross-cut sentence; that is a cross question's.
3. **Power before any contrast.** `thresholds.yaml` holds `power.smallest_effect_pp` (and alphas, floors, seeds); a
   cut whose rows cannot detect it is refused with its minimum detectable effect, and a refusal is an answer.
   Never judge a cut by whether its result is still significant.
4. **A changed cut is a new release.** Changing a filter, adding or retiring a cut, or changing a threshold changes
   the release's hash, so every Board Job after it moves the code clock.

**The pooling verdict.** Whether the cuts support one counsel or need separate ones is a Knowledge question on Cross
(`run-pool-tNN`): `POOL` (every cut's Wisdom defers to the full counsel), `SPLIT` (each cut may counsel within its
own evidenced boundary), or `UNDETERMINED` (no cut's Wisdom may act as though either were proved; only the full
counsel stands, and it says subgroup applicability is open). A non-significant difference alone never establishes
POOL. Every Wisdom page of a Board Job is conditioned on its Job's current verdict.


Signing
-------

`run-sign-release-pN` asks a person to sign once every new or changed question is agreed by another agent, every
new or changed script is reviewed by another agent, the question review has a verdict, and the cuts are signed. The
signature is `signed: ✅ <YYMMDD>` (never a name), recorded when the person states it
(`insight_ladder.py sign --date YYMMDD`), and it sets `state: closed`. After it the release never changes: a fix is
a proposal, and a proposal is the next release.

Cadence (decided 261008): one release per triaged batch of proposals, never one per proposal, so a Board does not
gain a Job for every new question.
