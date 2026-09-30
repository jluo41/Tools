---
name: subjective-label-definition
description: >-
  The Labeling › Definition view skill of the subjective-label family: it
  settles what each label means: outside evidence, the definition discussion with the identified human, and the G0 Confirm meaning gate. Every Run in this view names this skill, and no other view uses it.
  Use for discussing the label meanings, definition-discussion, revising a label's wording, Confirm meaning, G0, meaning receipt, discovery search, or /subjective-label-definition.
metadata:
  version: "0.1.4"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-definition · Labeling Space › Definition

This skill owns the Runs of the labeling workbench's Labeling › Definition
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  Run Type                     state
 4    discovery-search         not built · one bounded outside-evidence query
 5    definition-discussion    built · engine/definition_discussion.py
G0    Confirm meaning              a gate, not a Run · engine/job.py confirm or the button
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

`discovery-search` (not built yet) runs one bounded external-evidence query
per Run and writes `discovery/search_<n>/result.json`. It is provenance for
the discussion, never a gate input.

G0 is the entry predicate for commissioning `round-prepare` in the shared
Workflow graph; it is not a phase-owned gate Run. The five P0 authority files
are `config.yaml`, `corpus/manifest.json`, `test/sealed/status.json`,
`register.md`, and `policy/versions/G_00/manifest.yaml`. A complete,
integrity-valid `corpus-contract` Result with valid human authority but no
meaning receipt is G0-pending, not `HOLD`: the identified human owes the
confirmation. G0 requires nonblank wording for every label. When a Contract
has label names but no meanings, the Definition discussion must settle them
before the UI offers Confirm meaning. Missing or unreadable P0 files, or invalid human
authority requires repair or `HOLD` before any dependent work proceeds.

`definition-discussion` (`engine/definition_discussion.py`) is how the
identified human owns the label wording instead of confirming a draft (JL
260927: S-Label-4's first wording was written by the AI). The chat opens the
Run with `start`, keeps the talk with `say` (author `model` for its questions
and proposals, `human` for the person's words), records only the person's
stated decision per label with `decide` (`--keep`, or `--meaning` plus
`--reason`), and ends with `close`. The model never picks a meaning and never
uses a round item as an example. `close` writes `results/<run>/ledger.yaml`
(each label before, after, and why, plus open questions). When any wording
changed, it calls `job.revise_meanings`, the one sanctioned change to the P0
meanings: it writes `gates/meaning-revisions/<seq>.json` (before, after, the
deciding Run, the retired meaning receipt), archives the G0 receipt to
`gates/g0/history/`, and resets the confirmation, so the person presses
Confirm meaning again. `job.py status` checks the chain: each revision starts where
the last one ended, and `config.yaml` holds the last one's wording, so any
unrecorded edit is caught. Close this Run before releasing a round: the release
writer refuses an open discussion, and the discussion writer refuses any later
turn, decision, or close once a round card exists. After release, a meaning
change is a later guideline patch for `guideline-learn`.

`authority_hold(config)` is true for simulation/proxy authority, imported
source labels without a locally appointed human, a missing human id, or any
mode except `single_human_semantic_authority` with
`creates_human_gold: true`. With valid authority and intact P0 files, an
absent meaning receipt and G0 receipt is the expected pending-confirmation
state: `status` names explicit caller attestation as `next_action`, not
`HOLD`. The confirmation API checks that the caller-supplied id matches the
configured semantic authority and refuses on HOLD or P0 integrity failure;
the CLI and local Board do not authenticate the caller's identity. If semantic
confirmation exists but its G0 receipt is missing, status keeps G0 open and
asks to restore the receipt. A missing receipt can be restored after round
release only when the intact meaning receipt proves confirmation preceded that
release. Labeling → Definition exposes `Restore G0 receipt` for exactly that
case; the existing round resumes afterward. An invalid or semantically
unbound G0 receipt requires separate integrity repair and cannot be silently
overwritten. Status also checks the confirmation time when a matching G0
receipt exists: a confirmation later than a released round remains blocked.
A new attestation
cannot retroactively authorize an already released round. A prior bound receipt can be upgraded only
when its existing G0 receipt still verifies; the old receipt is archived under
`gates/g0/history/` before replacement. Corrupt or unverified receipts are never
overwritten.

Human confirmation is a separate explicit caller attestation; never infer it
from chat or flip a boolean by hand. `--attest-as-human` records the caller's
claim to be the configured human; neither the CLI nor the Board authenticates
that identity. Do not treat this receipt as identity proof in a multi-user or
adversarial environment. `--accept-current-schema` means the caller confirms
the current construct, class schema, seven regions,
uncertainty/unresolved disposition, and G_00 manifest. `confirm` records
what was confirmed (construct, classes, regions, uncertainty) in
`authority.meaning_receipt` and writes `gates/g0/receipt.json` with the same
content. A new confirmation refuses while a definition discussion is open;
restoring a missing G0 receipt from an intact pre-release attestation can proceed
even if an obsolete discussion Ticket remains open after round release. It is
idempotent when G0 is already valid. Without both semantic and G0 receipts,
the compatibility status remains P0. The G0 receipt must declare the canonical schema,
`status: passed`, the same identified human, and the same confirmed content;
presence alone never passes the gate.

```bash
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/job.py" confirm \
  --page-file <page-home>/<page>.md \
  --job-root <page-home>/labeling \
  --human-id <human> --accept-current-schema --attest-as-human
```

The Board Labeling screen is a second confirmation channel:
`Labeling → Definition → Confirm meaning`, after the caller ticks the attestation
box and accepts the browser confirmation dialog. The receipt explicitly says
`identity_assurance: caller_attested_not_authenticated`; the Board origin check
reduces cross-origin writes but does not authenticate the caller. Both channels
refuse before writing a byte when the submitted id differs from the configured
id, when the job is on HOLD, or when P0 integrity fails. The
door's own checks are in
`../label-building-workflow/haipipe-workbench-labeling/SKILL.md` §Write and authority law.

A discussion Run covers every label: `close` refuses until each label is
settled. To change one label, settle the others with `decide --keep`.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
