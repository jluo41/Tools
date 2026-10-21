---
name: haipipe-draft-writing
description: >-
  THE writer of a Page: drafting and revising prose from the plan (outline to
  prose, plain English rewrite), the sentence contract (a sentence's dotted
  address, comment lanes, change records), and the WRITE step of a Board Page
  (`run-section-<slug>`, `run-paragraph-<slug>`): after all planned Page Runs and
  required evidence Task Results complete, WRITE adopts human-agreed prose in one
  Page-level pass, integrates authorized evidence, builds declared delivery
  projections, and pre-checks one exact version before independent CHECK. It never
  reviews its own text: the judge is haipipe-draft-review. Evidence on a span of
  words is haipipe-evidence's `anchor`. Retains the explicitly delegated
  single-paragraph path. Trigger: draft prose, outline-to-prose, plain English
  rewrite, revise this paragraph, comment on this sentence, edit this sentence,
  sentence address, page content, adopt agreed text, writing Run, WRITE cycle,
  publish page, build page, /haipipe-draft-writing, /haipipe-writing draft,
  /haipipe-sentence. Also auto revise (rounds until good enough, big decisions held): auto revise, revise until good, revise rounds. Also the Revise Run (the old haipipe-draft-revise, now
  ref/revise.md): revise, compare before and after, what changed, track
  changes, change ledger, run-revise, /haipipe-draft-revise.
metadata:
  version: "0.25.2"
  last_updated: "2026-10-20"
  # version history: ./CHANGELOG.md
---

# /haipipe-draft-writing · write the text, adopt agreed text, deliver one Page version

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means every delivery artifact, and `## Content` itself (`cli/page.py adopt` writes it from the Draft's `## 3 · Draft`): change the Draft or the exporter, then rerun. A one-sentence change is the haipipe-draft fast path.

> ⛔ **No content hashes** (hard rule, JL 260928; AGENTS.md rule 9). A version is its number and date; staleness is file time or `git diff`. Never write, check, compare or pin a sha256 in a Result, receipt or runtime.yaml.

Load, in order: `haipipe-draft`, `haipipe-draft-workflow`, this skill,
Folder-owning workflow or canonical family skill, exact Page Face owner,
`workbench-task-draft/ref/plan-grammar.md`, applicable policy and the
selected integration/delivery workers. Load an owner only once when it fills
both roles. For `folder-kind: task`, load the reader-facing
`haipipe-page-task` companion for its display/form contract.

At adoption, build, or release, apply `../haipipe-draft/ref/release-decisions.md`
for profile precedence and reuse of existing human decisions.

## 🧱 What this skill holds

```text
haipipe-draft-writing/
├── SKILL.md              the WRITE step (below) and this map
├── ref/writing.md        writing prose: the rules it writes by, realize, weave, revise (start here)
├── ref/writing-request.md  the shared request and return
├── ref/realize-from-plan.md · weaving.md · writing-dna-adapter.md
├── ref/change-record.md · holes.md
├── ref/sentence.md       the sentence contract: address, lanes, change records
├── ref/paragraph-run.md  the delegated single-paragraph profile
├── cli/promote_paragraph.py   (test: tests/test_promote_paragraph.py)
└── ref/history/          the retired haipipe-sentence changelog
```

Independence: whoever writes never reviews. The judge is `../haipipe-draft-review/SKILL.md`; a model that wrote a passage and then reviews it in the same context is self-review and cannot close a Page.
`haipipe-draft/cli/wdiff.py` (the word-level change record) stays in `haipipe-draft`; call it from here.

## ✍️ Writing prose

Realize an approved plan and evidence slice as sentences, weave paragraphs, and revise existing prose by the surgical-revision rule. Read `ref/writing.md` first (its rules section is what every sentence is written by); it points to the rest of `ref/`. The plan, the evidence and the venue belong to the host workflow; a Page's human gate belongs to a person.

## 🔤 The sentence

One prose line is one sentence, with a dotted address (`QB8.C1.P1.S1`), `>` comment lanes beneath it, and a change record for every edit. The full contract is `ref/sentence.md`. Evidence on a span of words is not defined here: it is `haipipe-evidence`'s `anchor` (`../../evidence/haipipe-evidence/SKILL.md`).

## 🧭 Run Workflow placement

CONTENT owns the Page release/adoption controller operation. It consumes closed
writing Results and ready Evidence Results, then reruns the declared lanes'
fixed Delivery Runs (`page.py export`). Adoption and pre-check are controller
actions; delivery builds belong to those Delivery Runs. The CONTENT compatibility label
does not create an additional Run or a Step outside an owning Run.
The Workflow Runtime and the independent CHECK completion gate decide whether
the Page release can close.

## The Revise Run

`run-revise-<target>` compares two frozen texts of one target and settles every
difference in a change ledger. It was the skill `haipipe-draft-revise` until
2026-10-16 (s41-D11); the page is `ref/revise.md`, the ledger format
`ref/revise/change-ledger.md`, its history `ref/history/haipipe-draft-revise-CHANGELOG.md`.
The Run name and the Revise view in Draft Space are unchanged.

**Auto revise** (s41-D13): rounds of this skill revising a candidate copy and a fresh haipipe-draft-review agent
judging it, until no rubric axis needs work, a round stops improving, or 3 rounds pass. Small fixes are applied to the
copy; anything that changes a claim, a number, a citation, the order of the argument or the plan is held as a decision
card for the person. Rules: `ref/auto-revise.md`; record and stop rule: `cli/auto_revise.py`; the loop is run by
haipipe-draft-workflow.

## Which request is this?

| Request | Owner / action |
|---|---|
| Draft, revise, discuss sentences, act on human annotations | `haipipe-draft-workflow/ref/interactive-writing-run.md` → SHAPE + `haipipe-draft` |
| Accept or close one paragraph Page Run | Interactive workflow; settle its text, Bullets and Evidence without adopting Content |
| Adopt all agreed passages into Content | This skill, after the Page release barrier |
| Fill an agreed evidence slot | This skill after LAND/EMBED; no invented or changed claim |
| Export the adopted Page | This skill + owner's delivery workers |
| Explicitly delegate a fresh paragraph without interactive review | Optional `ref/paragraph-run.md` profile |
| Judge whole-Page completion | `haipipe-draft-review`, not the writer |

A candidate may be drafted while Shape is unapproved or evidence is missing.
It stays in the selected Outline Markdown as each Bullet's Draft.
Those discussions do not have to wait for CONTENT's publication gates.
Conversely, a saved Draft alone is not human
acceptance or a completed Writing Result.

## Page release barrier

Do not enter CONTENT merely because one Section or paragraph Page Run closes.
The release barrier requires the planned `run-structure-<slug>`, `run-section-<slug>`, and
`run-paragraph-<slug>` Runs, and every
required evidence Task Result to be complete and bound. Until then,
the working Shape and candidate prose remain current in the Draft Space;
`<page>.md` and `delivery/` remain unchanged and are labelled stale by design.

When the barrier opens, perform one Page-level CONTENT pass. Apply all accepted
candidates through scoped, source-checked patches, integrate their bound
evidence, generate the declared web/LaTeX/Word outputs once, and pre-check that
one exact Page version. This is one release pass, not a claim that the available
writer provides a multi-paragraph atomic transaction.

For the interactive Page profile, an explicit user instruction such as “go ahead
to the content and delivery” is the release decision once every planned Page Run
and required Evidence Result is complete. Do not send the person back to OUTLINE
solely because a historical `approved:` field still shows `⬜`; record the exact
instruction in the CONTENT receipt and suggest the next step after this pass.

## WRITE · four movements, not four Run identities

```text
Adopt       accepted Writing Run/Version/Step → exact Page prose
Integrate   ready evidence at authorized locations; preserve agreed meaning
Build       requested/current declared delivery projections
Pre-check   formal non-closing readiness judgment → independent CHECK
```

Adopt is code: run `haipipe-draft/cli/page.py adopt <page> --dry-run`, show the diff, then
run it without `--dry-run`. It refuses rather than guess (paragraphs that differ, a sentence to
place among untagged blocks); fix what it names in the Draft or the Page, then adopt again.
Never retype adopted sentences into `## Content` by hand.

CONTENT does not manage the feedback loop, allocate one replacement writing
Run per accepted paragraph, or automatically humanize an agreed passage.
The interactive workflow owns original feedback, Steps, Versions and scoped
human acceptance; this Run owns the adopted Page and delivery trace.

## Entry gates · publication, not rehearsal

Before adoption, read the current Context, selected plan, accepted writing
snapshot and destination Page. Follow only selected Evidence Result pointers,
not historical Result trees unless a pointer disagrees.

| Check | Required fact |
|---|---|
| Authority | Current Folder/Page Face owner and Context policy resolved |
| Runs | Every planned Page Run complete; required evidence Task Results ready and bound |
| Shape | current checked Shape, or an explicit interactive user instruction to adopt the accepted Shape; do not block this Page profile on a duplicate `approved:` tick |
| Writing | Exact target text accepted by the person, with actor, quoted decision and reviewed Run/Version/Step; no inferred acceptance |
| Evidence | Every Bullet declares typed Items or justified `none`; required locally attainable Results ready and folded; CITE verification satisfied |
| Source | Destination Page not saved since the adoption base was read (file time or `git diff`); target mapping matches |
| Form | Owner's actual paragraph/word/sentence/citation/display requirements measured; missing policy is `not specified`, not a guessed venue rule |

A failed authority/source row stops adoption. Missing evidence routes to
EVIDENCE; a changed claim/job/order routes to SHAPE and the affected Writing
Step. A named server/person gate can permit **explicitly authorized draft
mode** with `[E## pending]` at exactly the owed slot. This is not a final claim;
final mode rejects every unresolved marker. Never replace missing evidence
with a plausible number or citation.

For Section Pages, use the owner's `haipipe-paper-draft/cli/section-stats.py`
when a form audit is needed. Keep CITE Item count, source entries,
citation-bearing sentences and key mentions separate. A form warning blocks
only when the named authority makes it binding; report the actual tradeoff.

## Adopt · no second draft

1. Read the accepted full passage and the exact scoped human decision from
   the Writing Result. Agent `applied`/model completion is not acceptance.
2. Freeze the destination identity and exact target paragraphs. Preserve
   unrelated paragraphs, comment lanes, headers, Aims and approved Shape files.
3. Adopt the accepted wording via a scoped Markdown patch. Preserve the Page
   owner's sentence apparatus: a Section maps one Bullet to one sentence with
   its stable `realizes:` link. Keep internal process metadata out of prose.
4. Recheck the base immediately before writing. If a concurrent session changed
   it, stop/rebase explicitly; do not overwrite or silently trust an old read.
   Existing source-writer locks/token checks remain mandatory where available.
5. Read the result back. Compare accepted and saved prose and every protected
   target. Record Run/Version/Step, accepted text version, target addresses,
   the Page's saved time before/after and exact authorized integration edits in
   the CONTENT receipt. No extra writing Run is required.

The current implementation permits scoped source editing; this skill update
does not introduce a multi-paragraph atomic promoter. Do not claim transactional
all-or-nothing adoption unless the selected writer actually provides it.
Interrupted/partial adoption stays explicit; inspect the live source and trail
before retrying. Never record `promoted` before the saved output is verified.

## Integrate · evidence does not authorize rewriting

Ready citations/numbers may fill only explicitly agreed locations, within the
accepted claim strength. Each placement traces to that Bullet's own CITE,
VALUE or DISPLAY Item; no sibling/paragraph-level evidence inheritance.
`Evidence: none` is not permission to add an empirical claim.

Preserve calibrated uncertainty, numbers, terminology, examples and reader
order. If evidence contradicts the text, changes its interpretation, or calls
for a different sentence, return the affected question to the interactive Run.
Background work may propose a change, never overwrite accepted text.

After integration, read the assembled division/Section for duplicate claims,
abrupt seams and terminology drift. Report out-of-scope findings; do not repair
them by silently rewriting accepted paragraphs. Reopen only the affected
targets with explicit authorization. The default style is owned once by
`haipipe-draft`; the Context's specific policy/exemplars take precedence.
Writing DNA supplies surface choices, never evidence or a new claim.

## Optional delegated single-paragraph path

Only when explicitly selected, load `haipipe-run` and `ref/paragraph-run.md`.
That existing profile uses:

```text
family: page
operation: paragraph-writing
target: exactly one C<n>.P<m>
Run: owner-native Markdown ticket with embedded prompt
Result: paragraph.md + trace.md + runtime.yaml
```

The worker is `haipipe-draft` plus owner-selected policy/revision workers.
Read the profile's prompt, evidence, Writing DNA, trace and readiness rules.
A sentence request stays surgical. A worker cannot expand a commission into a
whole-Section rewrite. Optional anti-slop scores are diagnostic, never human
acceptance or a promise of human authorship.

```bash
python3 <haipipe-draft-writing>/cli/promote_paragraph.py --page <page>.md --result <resolved-result> --dry-run
python3 <haipipe-draft-writing>/cli/promote_paragraph.py --page <page>.md --result <resolved-result>
```

This promoter requires a complete single-paragraph runtime and the time the
Run read the Page (`read_at` on its `page-source` input, else `started_at`). It
locks the Page, refuses it when saved after that time, preserves unsupported apparatus
by refusing unsafe writes, and records verified promotion with recovery for an
interrupted application. It **does not accept** interactive Version folders.
Do not manufacture per-paragraph Run wrappers to feed agreed interactive text
into it. Job-backed Task Results stay at their owning Job address.

Historical division-writing and paragraph-writing Results remain read-only
provenance. The delegated profile's new-Run-on-material-change rule does not
apply to ordinary interactive feedback: that profile advances Steps/Versions.

## Build and formal check

After the Page release barrier opens, build only the projections requested or required at the formal handoff:
`delivery/latex/`, `delivery/word/`, slides/render outputs as declared by the
owner. Routine interactive Steps and individual Page Run closures do not write
Content or rebuild any delivery. Separately commissioned expensive exports may
use delegated Task Runs; a routine mechanical command does not need an invented
Run.

Use frozen source identity for background work. Before adoption or calling an
artifact current, compare its consumed source with the latest accepted Page.
A stale/failed build is reported as such, never relabeled latest. Task Pages
must include the declared substantive display units, not prose-only substitutes
or mere figure references. Page-level delivery does not assemble or rename the
Paper master's folders.

For a complete delivery, provide the requested PDF/Word outputs and PDF page
count. DISPLAY review uses current standalone `preview.pdf`; Page delivery
uses `delivery/latex/<stem>.pdf`, never a paper master or legacy flat lane.
Draft PDFs may be offered honestly while named evidence remains owed.

At formal completion, use a fresh read-only pre-check of the built version:
`ready → CHECK`, `another pass → owning authority`, or a named missing-input
route. A review finding does not authorize a prose-changing worker over
accepted text. The independent `haipipe-draft-review` judges the exact final
source/render identity and alone emits whole-Page CLOSE. This is not the
person's scoped writing Version closure.

## Receipt and reader handoff

```text
Run: CONTENT
cycle: WRITE
context: <current identity>
plan: <exact approved/inherited Shape>
decision: <exact user instruction that authorizes CONTENT when this is the interactive Page profile>
writing: <accepted Run/Version/Step and human-decision source>
adoption: <targets; accepted text version; Page saved before/after; scoped changes>
integration: <Item/Result bindings; continuity findings; reopened targets>
page: <source identity>
delivery: [<actual outputs; frozen input identity; current/stale>]
pre_check: ready | another-pass | blocked | not-requested
route: CONTENT | CONTEXT | OUTLINE | EVIDENCE | CHECK | HOLD
reason: <actual next authority>
```

A controller-dispatched receipt also obeys
`../haipipe-draft-workflow/ref/producer-contract.md`'s exact schema; never pass
`not-requested` as a completed formal pre-check.

Use `../haipipe-draft/ref/user-check-packet.md`. Routine writing returns
complete selected paragraphs and concise item-based reasons; formal delivery
adds the actual evidence/PDF states. Put direct verified **Draft Space**
(`lens=div`) and **Evidence Space** (`lens=evidence`) links at
the end, not raw HTML, localhost or a file download. Do not claim a saved or
updated Workspace until the source has been saved and read back.

## Boundaries

No invented evidence; no in-place approved Shape edit; no agent-created human
approval; no fresh Run per feedback Step; no accepted-text rewrite disguised
as adoption/export; no CHECK verdict by the producer; no unrecorded Page patch.
