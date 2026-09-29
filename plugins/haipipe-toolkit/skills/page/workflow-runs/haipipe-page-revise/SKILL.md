---
name: haipipe-page-revise
description: >-
  The Revise Run of a Board Page (`run-revise-<MMDD>-<target>`): compare two frozen
  texts of one target, before and after, and settle every difference. Its
  Result is a change ledger, one row per change with Before, After, kind, Why,
  decision, and inferred preference, listed in the Draft Space Runs panel
  (Revise edits) and rendered as red/green cards in the All-runs view.
  Two doors: the person edits Draft sentences in place in Draft Space → Revise
  (the first Save opens the run, later Saves change only the Draft, close writes
  the ledger), or an agent compares two frozen
  texts. Page Content is never touched; accepted Drafts reach the Page through
  the writing Run's Version. Trigger: revise, edit this sentence, compare
  before and after, what changed, track changes, review the revision, accept
  or reject changes, /haipipe-page-revise.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-revise · two texts in, decisions out

**LOAD `../../haipipe-page-workflow/SKILL.md` FIRST.** This file owns the
Revise Run's delta. The Run contract is `../../../run/haipipe-run/SKILL.md`;
the ledger format is `ref/change-ledger.md`; the identity grammar is
`../../haipipe-page/ref/page-run-families.md`.

```text
identity   run-revise-<MMDD>-<target>  target: C1 · C1.P1 · P03-P05 · or `page` (older: rp-revise-NN_<target>)
inputs     text A and text B, named by path and version: two Versions of one writing
           Run, an accepted Version and a delegated paragraph Result, or two
           built Page versions (their delivery manifests)
ticket     runs/run-revise-<MMDD>-<target>.md, written when the run opens; keeps the text before
result     results/run-revise-<MMDD>-<target>/  runtime.yaml · working.md · v001.md, written at close
           the journal's Saved result holds the change ledger (ref/change-ledger.md)
actor      a fresh agent or the person; never the writer of text B
close      every change decided; the accepted text is handed to the owning
           writing Run as its next Version (NEW_VERSION), or nothing changes
surface    Draft Space Runs panel → Revise edits; the All-runs view (lens=run) → Page Writing → Revise shows each row as one red/green card
```

## 🎯 Why it is a Run and not a Step

The comparison passes the six Run tests: a bounded target and two frozen
inputs, a stable type, a Ticket that names a reviewer who is not the writer,
a close rule (every row decided), a durable Result, and closure independent
of the browser. Until now the same comparison lived inside a writing Step as
`#### Track changes` and died with it: it could not be commissioned against
two arbitrary versions, had no card of its own, and its decisions were not
addressable. Revise gives the comparison an identity; it does not give it
prose authority.

## ✏️ The direct door · Draft Space → Revise

The person opens the Revise view of Draft Space. Every paragraph is one box
pre-filled with what Reading shows (its Draft, or the Page's own realized
sentences where no Draft exists yet), one sentence per line with a blank line
between points, and one `Save`. The blank-line blocks map back to the
paragraph's Bullets in order (no blank lines: each line is one point; extra
blocks join the last Bullet, missing blocks clear the rest); a Save writes the changed Draft fields
into the selected Outline under the page lock, guarded by the Bullet and Draft
tokens the page was rendered with. Records only at the two ends (JL 260928):
the first Save on a paragraph opens its `run-revise-<MMDD>-<c1-p2>` run, one
ticket in `runs/` that keeps the paragraph's text before the Save (`## Before`,
one `C1.P2.B1 · sentence` line per Bullet); later Saves change only the Draft,
and an optional Why is kept in that ticket. When the person says close,
`page.py close-run <page> <run>` compares that Before with the Draft now and
writes `results/<run>/v001.md`: one `## Step s001`, one `##### Rnn · <kind>` card
per changed Bullet with `###### Before`, `###### After`, `###### Why`,
`###### Decision` `accept`, and `###### Preference status` naming the direct
edit, plus `runtime.yaml`, `working.md` and one log line. The All-runs view renders
the cards red/green. Adding or removing points is not a Revise edit but a
Structure change. Server: `servers/workbench-page/
outline_revise.py`, POST `/_board/draft` with `action: revise`.

## 🔁 The compare door · two frozen texts

1. **Commission.** Name the target and the two texts by path and version number. The
   usual pair is the current accepted Version and the newest candidate of the
   same writing Run; other legal pairs are an accepted Version against a
   delegated `paragraph.md`, or two built Page versions by their
   delivery files (`delivery/web/<page>.md`).
2. **Compare.** Compute word and punctuation level differences per sentence
   (`haipipe-writing/cli/wdiff.py`; whole-sentence red/green only when a
   sentence is removed or added). One ledger row per material change; pure
   whitespace and formatting are not rows.
3. **Classify and explain.** Each row gets a kind from the Step template's
   change types (wording · claim · evidence · structure · citation · tone) and
   a Why that names the feedback item or purpose it answers. Where the change
   reveals a durable taste, record an `Inferred preference` with its status.
4. **Decide.** The person, or the reviewer with the person's standing
   authorization, marks each row `accept`, `reject`, or `modify: <text>`. A row
   without a decision keeps the Run `Waiting`.
5. **Close.** When every row is decided, assemble the accepted text and hand
   it to the owning writing Run as `NEW_VERSION`; the writing Run stays the
   sole prose authority. Revise records the handoff (Run id, Version) and
   closes. If every row is `reject`, close with no handoff.

## 🔒 Boundaries

- Never edits `<page>.md`, a Version journal of another Run, an Evidence
  Result, or a delivery artifact. The compare door writes only its own ticket
  and Result; the direct door additionally writes Draft fields of the selected
  Outline, nothing else in it.
- Never judges the whole Page: `haipipe-page-check` does that on a built
  version. Never mines patterns across closed Runs: post-run analysis does.
- A modified row is still a decision in this Run; the modified text reaches
  the Page only through the writing Run's Version.
- Inferred preferences are candidates for `haipipe-writing`, never rules.

## 📂 Files

- `ref/change-ledger.md` · the Result format the All-runs view renders, both doors
- `../../../../servers/workbench-page/outline_revise.py` · the direct door: Revise view rows, `action: revise`, ledger writer
- `../../haipipe-page-workflow/SKILL.md` · the Run list and the `revise` row
- `../../haipipe-page-workflow/ref/writing-step-template.md` · the `#### Track changes` block the ledger reuses
- `../../haipipe-page-workflow/ref/post-run-analysis.md` · the pattern review this Run is not
- `../../haipipe-workbench-page/ref/run-space.md` · the Revise card
- `../../../writing/haipipe-writing/cli/wdiff.py` · the word diff
- `../../../../servers/workbench-page/runs.py` · the presenter: `rp-revise-*` cards and the Decision line
