> This page was the skill `haipipe-draft-revise` until 2026-10-16 (s41-D11). Its Run names are unchanged; the owner is now `haipipe-draft-writing` (ref/revise.md; s41-D17: revising is the writer's second pass).

# /haipipe-draft-revise · two texts in, decisions out

**A Section's Revise cards** (the draft Task's 5 · Revise tab, b32 s41): `/haipipe-draft <task> revise` reads the
person's notes and writes `draft/records/<stem>-revise.md`, one card per change, each a `### ` heading named by its
kind and sentence (`### Edit · S1 · split into three sentences`; kinds Edit, Review, Section question, never R1-R7),
then four lines: `Why:`, `Original:`, `Expected:`, `State: proposed`. The person accepts or rejects each; an accepted
card goes into `## 3 · Draft` by its sentence's address as the next version.

Each revise run is one **pass**, and the file keeps only the latest (JL 261020: "we just need one of it, do you get
it? always keep the latest version"): the run rewrites the file as `## Pass <k> · <yymmdd> · on draft v<N>` with its
cards under it, carrying over the last pass's cards that are still undecided and still true and dropping the rest (git
keeps them; a file with no Pass heading is pass 1). The tab shows that one pass, each card its own card as old → new, with no
frame around the pass (never a box in a box). Before writing a pass, think as the Section's reviewer: say in
three lines who you are (the venue's reviewer, from the draft's or the version's `desk:`), what you look for, and how
you will review (the argument and its paragraphs first, then claims and evidence, then sentences) (JL 261020: "think
about yourself，就是你是一个什么样的 reviewer，你是怎么审这篇文章的"). A pass opens with its report, `### Revise
review report`, one line each: `Reviewer:` (those three lines), `Verdict:`, then one line per axis of
haipipe-draft-review's rubric, `Mechanics:`, `Function:`, `Evidence:`, `Readability:`, then `Coherence:` (each join
from one sentence to the next), `Anti-AI:` (run haipipe-draft-review's `cli/anti_slop.py audit` on the text and read
its `ref/ai-tells.md`) and `Venue:` for the desk's own rule, each `<MEETS | NEEDS WORK | NOT VERIFIABLE | N/A> ·
<0-10>/10 · how the draft reads · Fix: the smallest fix` (the score bands and the two
extra rows are haipipe-draft-review's `ref/evaluation-rubric.md`); then `Cards:`, how the cards' own text scores on the same
audit (self-review when the reviewer wrote them), then `Now:` and `Proposed:` (the paragraphs as `P1 <job> (S1 to
S4) · P2 …`). The tab shows the mean score as a reading aid, never a pass mark (JL 261021: "你这个 rubric 怎么没有
分数？... 句子连贯性、反 AI 写法"). The cards are sentence by sentence: one card per sentence that has a finding, its
Why naming the rubric row it answers; a sentence with no finding gets no card (JL 261021: "还是一个 sentence 一个
sentence 改吧 ... 每个 sentence 你加一些理由"). It has no State and nothing to accept; the tab
shows it as its own section, 📋 Revise Review Report, above the text and its cards (JL 261021: "先写一个 review
report，然后再 propose 怎么去改这些内容"; "above the section of 'The text and its Revise cards' you should give me
the section 'Revise Review Report' and tell me for each rubric, how you feel about this draft"). An older file's
`### Current draft review report` reads the same. Then come its Section questions on structure, then its Edit and Review cards; an Edit over a paragraph
(`### Edit · S7 to S10 · …`) shows a row per sentence. A sentence the person wrote is carded as a Review, never an Edit. While a pass or a blind review runs, write one line to `draft/records/<stem>-running.md`
(`- [5 · Revise] <what> · since <yyyy-mm-dd HH:MM>`, the time from the clock) and remove it when the run ends, so
the workbench shows ⏳ Running now under Operation. Keep the author's rulings for the Section in `draft/records/<stem>-revise-rules.md`, one line
each with his words and the date, added the day he gives one; the tab shows it as 📜 Revise rules, and each blind
reviewer gets it as constraints.

**LOAD `../../haipipe-draft-workflow/SKILL.md` FIRST.** This file owns the
Revise Run's delta. The Run contract is `../../../project/haipipe-run/SKILL.md`;
the ledger format is `ref/revise/change-ledger.md`; the identity grammar is
`../../haipipe-draft/ref/page-run-families.md`.

```text
identity   run-revise-<target>  target: C1 · C1.P1 · P03-P05 · or `page` (older: rp-revise-NN_<target>)
inputs     text A and text B, named by path and version: two Versions of one writing
           Run, an accepted Version and a delegated paragraph Result, or two
           built Page versions (their delivery manifests)
ticket     runs/run-revise-<target>.md, written when the run opens; keeps the text before
result     results/run-revise-<target>/  runtime.yaml · working.md · v001.md, written at close
           the journal's Saved result holds the change ledger (ref/revise/change-ledger.md)
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

The person opens the Revise view of Draft Space. Every paragraph shows what
Reading shows (its Draft, or the Page's own realized sentences where no Draft
exists yet), one sentence a row, each row labelled with its sentence id (`S2`)
and naming its Bullet (JL 261020). The person types freely; leaving the
paragraph (or Cmd+Enter) saves it, Esc puts it back. A row keeps its Bullet, so
typing inside a row edits that sentence; a row the person makes (Enter, paste)
is a new sentence, and its Save adds a Bullet with the id before it plus the
next free letter (`S2` → `S2a`), its point (`[Added] …`, for the person to
rename) in `## 1 · Structure` and its sentence in `## 3 · Draft`; no Bullet is
renumbered, a deleted row empties its Bullet and keeps the slot, and an empty
planned point takes the next new sentence first. "+ paragraph" adds an empty
paragraph after one (its address the page's highest paragraph number + 1), which
opens on one empty row. A Save writes the changed Draft fields
into the selected Outline under the page lock, guarded by the Bullet and Draft
tokens the page was rendered with. Records only at the two ends (JL 260928):
the first Save on a paragraph opens its `run-revise-<c1-p2>` run, one
ticket in `runs/` that keeps the paragraph's text before the Save (`## Before`,
one `C1.P2.B1 · sentence` line per Bullet); later Saves change only the Draft,
and an optional Why is kept in that ticket. When the person says close,
`page.py close-run <page> <run>` compares that Before with the Draft now and
writes `results/<run>/v001.md`: one `## Step s001`, one `##### Rnn · <kind>` card
per changed Bullet (an added one is a `first draft`) with `###### Before`, `###### After`, `###### Why`,
`###### Decision` `accept`, and `###### Preference status` naming the direct
edit, plus `runtime.yaml`, `working.md` and one log line. The All-runs view renders
the cards red/green. Moving or dropping a point between paragraphs is a
Structure change. Server: `servers/workbench/workbench-task-draft/
outline_revise.py`, POST `/_board/draft` with `action: revise` (rows) or
`action: add-paragraph`.

## 🔁 The compare door · two frozen texts

1. **Commission.** Name the target and the two texts by path and version number. The
   usual pair is the current accepted Version and the newest candidate of the
   same writing Run; other legal pairs are an accepted Version against a
   delegated `paragraph.md`, or two built Page versions by their
   delivery files (`delivery/web/<page>.md`).
2. **Compare.** Compute word and punctuation level differences per sentence
   (`haipipe-draft/cli/wdiff.py`; whole-sentence red/green only when a
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
- Never judges the whole Page: `haipipe-draft-review` does that on a built
  version. Never mines patterns across closed Runs: post-run analysis does.
- A modified row is still a decision in this Run; the modified text reaches
  the Page only through the writing Run's Version.
- Inferred preferences are candidates for `haipipe-draft`, never rules.

## 📂 Files

- `ref/revise/change-ledger.md` · the Result format the All-runs view renders, both doors
- `../../../../../servers/workbench/workbench-task-draft/outline_revise.py` · the direct door: Revise view rows, `action: revise`, ledger writer
- `../../haipipe-draft-workflow/SKILL.md` · the Run list and the `revise` row
- `../../haipipe-draft-workflow/ref/writing-step-template.md` · the `#### Track changes` block the ledger reuses
- `../../haipipe-draft-workflow/ref/post-run-analysis.md` · the pattern review this Run is not
- `../../../workbench/workbench-task-draft/ref/run-space.md` · the Revise card
- `../../haipipe-draft/cli/wdiff.py` · the word diff
- `../../../../../servers/workbench/workbench-task-draft/runs.py` · the presenter: `rp-revise-*` cards and the Decision line
