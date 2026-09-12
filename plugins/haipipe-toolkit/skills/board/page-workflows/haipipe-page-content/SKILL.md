---
name: haipipe-page-content
description: >-
  The 03 CONTENT phase of a Board Page. WRITE adopts human-agreed prose,
  integrates authorized evidence, builds declared delivery projections, and
  pre-checks one exact version before independent CHECK. Interactive drafting
  and feedback belong to haipipe-page-workflow plus haipipe-writing, not a new
  mandatory CONTENT Run per paragraph. Retains the explicitly delegated
  single-paragraph compatibility path. Trigger: page content, adopt agreed text,
  CONTENT phase, WRITE cycle, publish page, build page, /haipipe-page-content.
metadata:
  version: "0.12.0"
  last_updated: "2026-09-11"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-content · adopt agreed text and deliver one Page version

Load, in order: `haipipe-page`, `haipipe-page-workflow`, this skill,
Folder-owning workflow or canonical family skill, exact Page Face owner,
`haipipe-plugin-outline/ref/plan-grammar.md`, applicable policy and the
selected integration/delivery workers. Load an owner only once when it fills
both roles. For `folder-kind: task`, load the reader-facing
`haipipe-page-task` companion for its display/form contract.

## Which request is this?

| Request | Owner / action |
|---|---|
| Draft, revise, discuss sentences, act on human annotations | `haipipe-page-workflow/ref/interactive-writing-run.md` → SHAPE + `haipipe-writing` |
| Adopt the agreed passage into Content | This skill; preserve exact accepted wording |
| Fill an agreed evidence slot | This skill after LAND/EMBED; no invented or changed claim |
| Export the adopted Page | This skill + owner's delivery workers |
| Explicitly delegate a fresh paragraph without interactive review | Optional `ref/paragraph-run.md` profile |
| Judge whole-Page completion | `haipipe-page-check`, not the writer |

A candidate may be drafted while Shape is unapproved or evidence is missing.
It stays in `outline/<stem>-preview.md`. Those discussions do not have to wait
for CONTENT's publication gates. Conversely, a saved preview alone is not human
acceptance or a completed Writing Result.

## WRITE · four movements, not four phases

```text
Adopt       accepted Writing Run/Version/Step → exact Page prose
Integrate   ready evidence at authorized locations; preserve agreed meaning
Build       requested/current declared delivery projections
Pre-check   formal non-closing readiness judgment → independent CHECK
```

CONTENT does not manage the feedback loop, allocate one replacement writing
Run per accepted paragraph, or automatically humanize an agreed passage.
The interactive workflow owns original feedback, Steps, Versions and scoped
human acceptance; this phase owns the adopted Page and delivery trace.

## Entry gates · publication, not rehearsal

Before adoption, read the current Context, selected plan, accepted writing
snapshot and destination Page. Follow only selected Evidence Result pointers,
not historical Result trees unless a pointer/hash disagrees.

| Check | Required fact |
|---|---|
| Authority | Current Folder/Page Face owner and Context policy resolved |
| Shape | `G>=1`, with direct approval or a valid inherited `shape-base`; never publish from `v0.*` or an unapproved working Shape |
| Writing | Exact target text accepted by the person, with actor, quoted decision and reviewed Run/Version/Step; no inferred acceptance |
| Evidence | Every Bullet declares typed Items or justified `none`; required locally attainable Results ready and folded; CITE verification satisfied |
| Source | Current destination hash and target mapping match the adoption base |
| Form | Owner's actual paragraph/word/sentence/citation/display requirements measured; missing policy is `not specified`, not a guessed venue rule |

A failed authority/source row stops adoption. Missing evidence routes to
EVIDENCE; a changed claim/job/order routes to SHAPE and the affected Writing
Step. A named server/person gate can permit **explicitly authorized draft
mode** with `[E## pending]` at exactly the owed slot. This is not a final claim;
final mode rejects every unresolved marker. Never replace missing evidence
with a plausible number or citation.

For Section Pages, use the owner's `haipipe-paper-section/cli/section-stats.py`
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
   it, stop/rebase explicitly; do not overwrite or silently trust an old hash.
   Existing source-writer locks/token checks remain mandatory where available.
5. Read the result back. Compare accepted and saved prose and every protected
   target. Record Run/Version/Step, accepted text hash, target addresses, source
   before/after hashes and exact authorized integration edits in the CONTENT
   receipt. No extra writing Run is required.

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
`haipipe-writing`; the Context's specific policy/exemplars take precedence.
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

The worker is `haipipe-writing` plus owner-selected policy/revision workers.
Read the profile's prompt, evidence, Writing DNA, trace and readiness rules.
A sentence request stays surgical. A worker cannot expand a commission into a
whole-Section rewrite. Optional anti-slop scores are diagnostic, never human
acceptance or a promise of human authorship.

```bash
python3 <haipipe-page-content>/cli/promote_paragraph.py --page <page>.md --result <resolved-result> --dry-run
python3 <haipipe-page-content>/cli/promote_paragraph.py --page <page>.md --result <resolved-result>
```

This promoter requires a complete single-paragraph runtime and frozen
`page-source` hash. It locks/rechecks the Page, preserves unsupported apparatus
by refusing unsafe writes, and records verified promotion with recovery for an
interrupted application. It **does not accept** interactive Version folders.
Do not manufacture per-paragraph Run wrappers to feed agreed interactive text
into it. Job-backed Task Results stay at their owning Job address.

Historical division-writing and paragraph-writing Results remain read-only
provenance. The delegated profile's new-Run-on-material-change rule does not
apply to ordinary interactive feedback: that profile advances Steps/Versions.

## Build and formal check

Build only the projections requested or required at the formal handoff:
`delivery/latex/`, `delivery/word/`, slides/render outputs as declared by the
owner. Routine interactive sentence edits neither rebuild the PDF nor invoke
this full phase. Separately commissioned expensive exports may use delegated
Task Runs; a routine mechanical command does not need an invented Run.

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
accepted text. The independent `haipipe-page-check` judges the exact final
source/render identity and alone emits whole-Page CLOSE. This is not the
person's scoped writing Version closure.

## Receipt and reader handoff

```text
phase: CONTENT
cycle: WRITE
context: <current identity>
plan: <exact approved/inherited Shape>
writing: <accepted Run/Version/Step and human-decision source>
adoption: <targets; accepted text hash; Page before/after; scoped changes>
integration: <Item/Result bindings; continuity findings; reopened targets>
page: <source identity>
delivery: [<actual outputs; frozen input identity; current/stale>]
pre_check: ready | another-pass | blocked | not-requested
route: CONTENT | CONTEXT | OUTLINE | EVIDENCE | CHECK | HOLD
reason: <actual next authority>
```

A controller-dispatched receipt also obeys
`../haipipe-page-workflow/ref/producer-contract.md`'s exact schema; never pass
`not-requested` as a completed formal pre-check.

Use `../../haipipe-page/ref/user-check-packet.md`. Routine writing returns
complete selected paragraphs and concise item-based reasons; formal delivery
adds the actual evidence/PDF states. Put direct verified **Bullet Workspace**
(`lens=div`) and **Evidence Workspace** (`lens=workspace&seg=items`) links at
the end, not raw HTML, localhost or a file download. Do not claim a saved or
updated Workspace until the source has been saved and read back.

## Boundaries

No invented evidence; no in-place approved Shape edit; no agent-created human
approval; no fresh Run per feedback Step; no accepted-text rewrite disguised
as adoption/export; no CHECK verdict by the producer; no unrecorded Page patch.
