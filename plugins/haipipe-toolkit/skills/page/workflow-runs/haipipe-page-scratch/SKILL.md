---
name: haipipe-page-scratch
description: >-
  The Scratch Run of a Board Page (`run-scratch-<MMDD>-<target>`): a person's rough
  thinking for one Section (`C1`) or whole paragraph group (`C1.P1`), captured
  from Draft Space, saved as often as they like, and closed by a manually
  triggered Finish that asks the AI for a Summary. It edits no Draft prose
  and replaces no Structure, Section, or Paragraph Run. Trigger: scratch,
  scratch note, rough thinking, finish scratch, scratch summary,
  /haipipe-page-scratch.
metadata:
  version: "0.2.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-scratch · the person thinks first, on the record

**LOAD `../../haipipe-page-workflow/SKILL.md` FIRST.** It is the list of Runs
this one belongs to. This file owns the Scratch Run's delta: who may open one,
what it captures, how it closes, and what it must never touch. The Run contract
itself is `../../../run/haipipe-run/SKILL.md`; the identity grammar is
`../../haipipe-page/ref/page-run-families.md`.

```text
identity   run-scratch-<MMDD>-<target>  target C1 or C1.P1 (older: rp-scratch-NN_<target>)
ticket     runs/run-scratch-<MMDD>-<target>.md, written at the first note
result     results/run-scratch-<MMDD>-<target>/  working.md · runtime.yaml · v001.md, written at Finish
surface    Draft Space › Scratch view: click a Section or paragraph heading
           (haipipe-workbench-page); the Runs panel lists it under Scratch
writer     the person, through the Draft Space Scratch editor; the AI writes
           only the closing Summary the person asked for
```

## 🎯 What it is for

Scratch is available once a selected Outline exists. It records a person's
rough thinking before any candidate prose is written: a Section (`C1`) or a
whole paragraph group (`C1.P1`) in the current Outline grammar. There is no
separate subsection node, and the B/symbol rows are reading material only, so
they are never Scratch targets. The Run exists so that the person's own words
about what a passage should do are durable, addressable, and visible to the
writer of the later Section or Paragraph Run, instead of living only in a chat.

## 🔁 How it runs

Records only at the two ends (JL 260928):

1. **Open.** The person clicks a Section or paragraph heading in the Scratch
   view and types. The first note opens `run-scratch-<MMDD>-<c1-p2>`: one ticket
   in `runs/`, nothing in `results/`. Scratch may open while the Structure run
   is still being settled; it is the one Page Writing Run not gated on Structure.
2. **Save.** Every autosave changes only the notes under the heading in
   `## 2 · Scratch` of the Draft Markdown. The Runs panel shows the run Running.
3. **Finish.** The person manually triggers Finish Scratch. The AI returns a
   non-empty Summary; that is the close: `results/<run>/` (`v001.md` with the
   notes and the Summary, `runtime.yaml`, `working.md`) and one log line. A
   Finish with an empty Summary does not close the Run.

A closed Scratch Run is immutable. A new thought about the same target is a
new `run-scratch-<MMDD>-<target>` (a second one the same day gets `-2`), never a reopened Version.

## 🔒 Boundaries

- It edits no Draft prose, no Bullet, no Evidence Item, no Content.
- It does not replace the Structure, Section, or Paragraph Run that will write
  the passage; those Runs read the Summary as input.
- The browser writes only the selected Outline's `## Scratch` registry and the
  Run's own journal; `--read-only` on the Page server disables both.
- Run Space shows the card as `Scratch · <scope> · <target>`; the opened card
  shows the raw notes first and the Summary when it exists.

## 📂 Files

- `../../haipipe-page-workflow/SKILL.md` · the Run list and the `scratch` Run Spec row
- `../../haipipe-page-workflow/ref/workflow-table.md` · the Spec × Space projection
- `../../haipipe-page/ref/page-run-families.md` · the RP identity grammar
- `../../haipipe-workbench-page/ref/run-space.md` · the card in Run Space
- `../../../../servers/workbench-page/outline_scratch.py` · the allocation and Save/Finish doors
- `../../../../servers/workbench-page/runs.py` · the presenter's Scratch card
