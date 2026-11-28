> This page was the skill `hai-draft-revise` until 2026-10-16 (s41-D11). Its Run names are unchanged; the owner is now `hai-draft-writing` (ref/revise.md; s41-D17: revising is the writer's second pass).

# /hai-draft-revise · two texts in, decisions out

**Structure first, then sentences (JL 261111).** A pass on a Section first reads the plan: `approved:` without ✅
sends the turn to 1 · Plan and writes no cards. With a signed plan, the pass checks the structure before any sentence:
does each paragraph do one move of the governing Narrative row, in its order, at the venue examples' lengths? If not,
the pass holds `### Section question` cards only (what to move, merge or cut, and why), its report says
`Verdict: structure first`, and the Section returns to Plan for the person's new word. Sentence cards wait until the
structure holds.

**A Section's Revise cards** (the draft Task's 5 · Revise tab, b32 s41): `/hai-draft <task> revise` reads the
person's notes and writes `draft/records/<stem>-revise.md`, one card per change, each a `### ` heading named by its
kind and sentence (`### Edit · s1 · split into three sentences`; kinds Edit, Review, Section question, never R1-R7),
then four lines: `Why:`, `Original:`, `Expected:`, `State: proposed`. **`Why:` scans (JL 261115: "the previous version and content is good,
Just think about how to make it more readable"):** keep the full reason, written as numbered points on one line,
`(1) … (2) … (3) …`, which the card draws one per row below the change. A source's quoted words or a list of candidate
papers go in an optional fifth line, `Detail:`, which the card shows closed (must-check M-D21). **Every problem gets a card (JL 261115: "for the
sentences with problem, please show the editing card with reasoning and suggestion options"):** after a sentence
review, each sentence under 8 on any score, with a weak or broken link, or over the point rule gets an `### Edit` card:
its Why the reviewer's problem as numbered points, its Expected the Fix, and, when the reviewer gave `A … | B …`, an
Option per choice. A split's Expected holds the sentences in order; Accept writes each on its own row (s12, s12a)
until the next renumber (must-check M-D22). The person accepts or rejects each; an accepted
card goes into `## 3 · Draft` by its sentence's address as the next version. A pass that rewrites the cards file reads
it first and keeps every decision the person made (a `State:` accepted, rejected or edited, a `Chosen:` option), the card
otherwise refreshed; only a card still proposed, or written by the writer, takes a new State (JL 261021, whose ✓ on a
Section question was once written back to proposed).
**Small changes, or a solid reason (JL 261113).** An Edit card changes the fewest words that fix the problem and
keeps the rest of the sentence word for word. The workbench prints each card's similarity to its Original (`difflib`
ratio, "73% same"), in red below 60%. A card below 60% is allowed only when its `Why:` names a defect that a small edit
cannot fix (a wrong fact, a claim the evidence does not carry, a sentence that breaks the paragraph's logic, or the
author's own ruling); a reason of style, flow or "reads better" is not enough, and the card is not written. When
in doubt, offer the small edit as Option A and the larger rewrite as Option B.
A card from a sentence review may add two lines before `State:` (0.29.0, JL 261110): `Score: <n>/10`, the blind
reviewer's score of the original sentence, and `Readable: <verdict>`, the fresh A/B readers' verdict on the rewrite
(`rewrite easier, same meaning`, `original easier`, `rewrite changes meaning` or `no gain`; hai-paper-draft,
Co-authors' patterns). The Revise step shows both beside the card's state: easier to read in green, original easier
or the meaning changed in amber, no gain in grey.

Each revise run is one **pass**, and the file keeps only the latest (JL 261020: "we just need one of it, do you get
it? always keep the latest version"): the run rewrites the file as `## Pass <k> · <yymmdd> · on draft v<N>` with its
cards under it, carrying over the last pass's cards that are still undecided and still true and dropping the rest (git
keeps them; a file with no Pass heading is pass 1). The tab shows that one pass, each card its own card as old → new, with no
frame around the pass (never a box in a box). Before writing a pass, think as the Section's reviewer: say in
three lines who you are (the venue's reviewer, from the draft's or the version's `desk:`), what you look for, and how
you will review (the argument and its paragraphs first, then claims and evidence, then sentences) (JL 261020: "think
about yourself，就是你是一个什么样的 reviewer，你是怎么审这篇文章的"). A pass opens with its report, `### Revise
review report`, one line each: `Reviewer:` (those three lines), `Verdict:`, then one line per axis of
hai-draft-review's rubric, `Mechanics:`, `Function:`, `Evidence:`, `Readability:`, then `Coherence:` (each join
from one sentence to the next), `Anti-AI:` (run hai-draft-review's `cli/anti_slop.py audit` on the text and read
its `ref/ai-tells.md`) and `Venue:` for the desk's own rule, each `<MEETS | NEEDS WORK | NOT VERIFIABLE | N/A> ·
<0-10>/10 · how the draft reads · Fix: the smallest fix` (the score bands and the two
extra rows are hai-draft-review's `ref/evaluation-rubric.md`); then `Cards:`, how the cards' own text scores on the same
audit (self-review when the reviewer wrote them), then `Now:` and `Proposed:` (the paragraphs as `P1 <job> (s1 to
s4) · P2 …`). The tab shows the mean score as a reading aid, never a pass mark (JL 261021: "你这个 rubric 怎么没有
分数？... 句子连贯性、反 AI 写法"). The cards are sentence by sentence: one card per sentence that has a finding, its
Why naming the rubric row it answers; a sentence with no finding gets no card (JL 261021: "还是一个 sentence 一个
sentence 改吧 ... 每个 sentence 你加一些理由"). It has no State and nothing to accept; the tab
shows it as its own section, 📋 Revise Review Report, above the text and its cards (JL 261021: "先写一个 review
report，然后再 propose 怎么去改这些内容"; "above the section of 'The text and its Revise cards' you should give me
the section 'Revise Review Report' and tell me for each rubric, how you feel about this draft"). An older file's
`### Current draft review report` reads the same. Then come its Section questions on structure, then its Edit and Review cards; an Edit over a paragraph
(`### Edit · s7 to s10 · …`) shows a row per sentence. A sentence the person wrote is carded as a Review, never an Edit. While a pass or a blind review runs, write one line to `draft/records/<stem>-running.md`
(`- [5 · Revise] <what> · since <yyyy-mm-dd HH:MM>`, the time from the clock) and remove it when the run ends, so
the workbench shows ⏳ Running now under Operation. Keep the author's rulings for the Section in `draft/records/<stem>-revise-rules.md`, one line
each with his words and the date, added the day he gives one; the tab shows it as 📜 Revise rules, and each blind
reviewer gets it as constraints.

**Every sentence passes.** After the axis rows, the report lists `Sentences:`, one line per sentence
read in its context (hai-draft-review `ref/sentence-logic.md`: its link to the sentence before, the specific
problem, a logic, a read and an ai score out of 10, the rewrite when any is below 8), then a `Flow P<k>:` line per paragraph; the
tab shows them as a table. The loop of blind reviews ends only when every sentence scores 8 or more on all three, with no
broken link (JL 261021: "你需要给每一个 sentence 句句过关"; "每句话都要看一下上下文，review 它的逻辑关系是否通顺").

**Sentence numbers follow the text.** After a pass adds, moves or merges a sentence, run `page.py renumber <page>`
(`--merged s15=s14` for a merged one): the sentence ids become s1, s2, … (an older S8 reads as s8) in reading order in the Draft, the evidence cards,
the Revise cards and rules and the comments (JL 261021: "我这 index 是不是要与时俱进一下？").

**Options when the fix is a choice.** Where a sentence can be fixed more than one way (another order, another
emphasis, another link to the sentence before), its card gives 2 or 3 options, each a whole sentence with its
approach in a few words: `Option A (<the approach>): <the sentence>`, then `Chosen: A`. The pass applies A by
default and the card's Expected is A; the person can pick B with ↳ Use B, which makes B the card's words, accepted,
for the apply step. A mechanical fix (a typo, a number) gets no options (JL 261021: "未必一下子只给一种修改结果，也
可以说可以用 A、B、C 几个不同的方法去修改，propose 一些选项").

**A person's comments come first.** A person leaves comments on sentences in 5 · Revise; they are in
`draft/records/<stem>-comments.md`, one `### Comment <n> · S<k>` block each (`Quote:` the words selected, `State:`,
then `- Note · <time>: …` lines). Each pass reads the open ones before the blind review and treats each as the
author's ruling: change the sentence as an Edit card carrying `Answers: Comment <n>` (one per sentence, as always),
or say why not; then append `- Reply · <yyyy-mm-dd HH:MM>: <what changed, and its rule>` (the time from the
clock), at most two short sentences and 30 words, since the page shows it as the AI's message in the thread and set `State: answered`. Never write a Note line, mark a comment done or delete one: those are the
person's. Every review and edit pass reads the Writing Rubric first (the Draft view's 4 · Writing Rubric, JL 261113: "when AI work on this reviewing or edit, will it consider this writing rubric?"): the page's `<stem>-requirement.md` (venue V and Section W rules), its `<stem>-revise-rules.md`, the Board's `writing-patterns.md`, and hai-draft-review `ref/plain-rules.md` and `ref/ai-tells.md`; each card names the rule it applies. The rubric holds writing rules only, how a sentence is written; a ruling on what a Section must claim or refuse is a decision and goes into its contract (the face's must-establish and must-refuse, or a D-thread), never the rubric (JL 261113, of "Lead with the osteoarthritis result": "this is more like the decisions to make"). The Writing Rubric grows as the work goes (JL 261113: "this rubric or writing patterns can be accumulated along the way, when we have more edit, or comments"): a comment, a co-author's tracked change or a decided card that states a rule for the whole Section goes into the Revise rules as a new R# (shown under 4 · Writing Rubric › This Section); one that holds for every Section of the paper (a co-author's pattern) goes into the Board's `writing-patterns.md` as a new numbered pattern with its Fix (› Coauthors). Say which rule a card added. A blind
reviewer never sees the comments; it sees the rules (JL 261021: "你每次改的时候，能不能通过我的 comments 来回复那种？";
"你的 change 怎么跟我的 comments 一起来做交互、解决我的 comments 呢？").

**Every new version is reviewed before it is shown as done (JL 261111: "where is the reviwing loops? ... loop by
loop, and then give the rubic review scores").** After a rewrite becomes draft v<N+1>, run one blind round on it: a
reviewer who did not write it scores each sentence (topic, link, logic /10, read /10) and the four rubric axes; a
sentence under 8 gets a rewrite; a fresh A/B reader compares the rewrite with the version in place; only a rewrite the
reader finds easier with the same meaning becomes the next version. Report each round's scores to the person as a
table (round, version, overall, the main problem). ScalingGlucose t00_abstract went 6.5 → 7.0 → 8.0 → 8.5 in four rounds
(r04 to r06 and an A/B read, 261111); v0.11 to v0.13 had been shown unreviewed, which is what the person caught.

**A title is chosen the same way.** Give 3 or 4 candidates, have a blind reviewer score each on accuracy to the findings,
clarity, the venue's title style and searchability, and let the person pick. The preposition carries the claim:
"Scaling laws are not universal for glucose foundation models" says general laws do not carry over, while "Scaling laws
of glucose foundation models …" and "Glucose foundation models' scaling laws …" say the models have their own laws,
which the paper never fitted (JL picked the first, 261111). Avoid a possessive on a long noun phrase in a title.

**LOAD `../../hai-draft-workflow/SKILL.md` FIRST.** This file owns the
Revise Run's delta. The Run contract is `../../../project/hai-run/SKILL.md`;
the ledger format is `ref/revise/change-ledger.md`; the identity grammar is
`../../hai-draft/ref/page-run-families.md`.

```text
identity   run-revise-<target>  target: C1 · C1.P1 · P03-P05 · or `page` (older: rp-revise-NN_<target>)
inputs     text A and text B, named by path and version: two Versions of one writing
           Run, an accepted Version and a delegated paragraph Result, or two
           built Page versions (their delivery manifests)
ticket     runs/run-revise-<target>/run-revise-<target>.md, written when the run opens; keeps the text before
result     runs/run-revise-<target>/passes/pNN-<MMDD>/  runtime.yaml and the ledger, one pass per close
           (an older Page: runs/run-revise-<target>.md and results/run-revise-<target>/)
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
exists yet), one sentence a row, each row labelled with its sentence id (`s2`)
and naming its Bullet (JL 261020). The person types freely; leaving the
paragraph (or Cmd+Enter) saves it, Esc puts it back. A row keeps its Bullet, so
typing inside a row edits that sentence; a row the person makes (Enter, paste)
is a new sentence, and its Save adds a Bullet with the id before it plus the
next free letter (`s2` → `s2a`), its point (`[Added] …`, for the person to
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
   (`hai-draft/cli/wdiff.py`; whole-sentence red/green only when a
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
- Never judges the whole Page: `hai-draft-review` does that on a built
  version. Never mines patterns across closed Runs: post-run analysis does.
- A modified row is still a decision in this Run; the modified text reaches
  the Page only through the writing Run's Version.
- Inferred preferences are candidates for `hai-draft`, never rules.

## 📂 Files

- `ref/revise/change-ledger.md` · the Result format the All-runs view renders, both doors
- `../../../../../servers/workbench/workbench-task-draft/plan_outline/outline_revise.py` · the direct door: Revise view rows, `action: revise`, ledger writer
- `../../hai-draft-workflow/SKILL.md` · the Run list and the `revise` row
- `../../hai-draft-workflow/ref/writing-step-template.md` · the `#### Track changes` block the ledger reuses
- `../../hai-draft-workflow/ref/post-run-analysis.md` · the pattern review this Run is not
- `../../../draft/workbench-task-draft/ref/run-space.md` · the Revise card
- `../../hai-draft/cli/wdiff.py` · the word diff
- `../../../../../servers/workbench/workbench-task-draft/run_views/runs.py` · the presenter: `rp-revise-*` cards and the Decision line
