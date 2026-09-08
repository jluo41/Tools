# Paper Story integration with Page, work, Sections, and Compile

Read this reference for an actual Page migration, workflow handoff, Section
binding, or compile-order edit. The eight Content divisions and their semantic
meaning live only in `../SKILL.md`; routers resolve that contract directly.

## Page and workflow records

The shared Page shell remains Opening → Outline → Content → Aims. Outline
plans the Story Page's content; C6/C7 describe the paper's research plan.
Do not mistake those two levels of planning for each other.

G0–G5 are owned by `haipipe-paper-workflow`. Existing human selection,
release, settlement and Section-release records stay in the Story's
`outline/` log and the shared `workflow/` receipts, using their existing
schemas. Work owners keep job/run state, budgets, commands and accepted
Results. C6/C7 may link those records; C5 summarizes their evidential meaning.
Preserve every existing receipt during a content revision. No Story row,
CHECK pass or requested edit constitutes a new execution release.

On returned evidence: read the Result and its limitations, update the C5
proposition and C3 answer as justified, then revise affected C6/C7 needs and
C8 claims/Section moves. A halted run is not a null result. A null result
is not automatically evidence of no relationship. Receipt acceptance and
claim support are different decisions.

New drafts can describe unavailable evidence and proposed Sections. CHECK
judges whether those plans and uncertainties are adequately described; it
does not require completion of the study. Existing approved Page artifacts
remain historical; a changed structure gets a new unapproved v0.x draft.

## Section rows

C8's detailed Section Narrative rows own reader question, ordered moves,
claims, evidence/display allocation, entry/exit, transitions and cut rules.
The compact section-map projection must agree with those rows. Keep the shared
Outline presenter and its supported projection mechanism; do not hand-copy a
generated table into the Page's Outline.

A planned row can exist before its Section Page. Once instantiated, retain its
exact `section-id`, target/category, Story version and `story-row:` binding.
Resolve by semantic row id within C8; do not assume the subsection is §8.1.
Current Section bindings use `story-row:` anchors; update an anchor only as
part of the affected Page's authorized revision.

Section-local paragraph detail may elaborate the Story's ordered moves but
cannot change its central claim, evidential limit or reader transition. A
material Story-row revision reopens affected Section checks. The selected
Venue contract supplies the desk rules, not new research findings.

## Compile projection

Use the existing compiler marker syntax for the currently selected Section
order:

```text
<!-- haipipe:compile-order:start -->
main:
- S-MISQ-Main-Abstract
- S-MISQ-Main-Introduction
appendix:
- S-MISQ-Appendix-Variables
<!-- haipipe:compile-order:end -->
```

These ids illustrate the format only; emit only the paper's actual Section ids.
The block is derived from the selected C8 rows. Before Section files exist,
keep their intended reader order in C8 without inventing compilable paths.
Before assembly, require an unambiguous selected target and real Section ids
consistent with `delivery/paper-build.toml`. Use one active marker block;
additional candidate Section orders stay in C8 until a target is selected or the
declared builder explicitly supports target-qualified selection. Do not
promise multiple identical marker blocks to a single-block parser.

`haipipe-paper-assemble` owns build configuration, fragments, bibliography,
manifests and DRAFT/ready checks. A content-layout correction preserves an
existing valid compile block and its Section identities. Assembly does not
approve the Story skill, a Story outline, work releases, or submission.

## Existing Story migration

Inspect the current Page, outline, Aims, accepted sources and any unmerged
source content before editing. Map source/proposition/boundary content into
C5, external inquiries into C6, study evidence plans into C7, and claims,
argument, reader journey and Section plans into C8. Retain Seed identity and
source references.
Preserve actual findings and historical approvals as evidence of past state;
do not carry an old approval to the new shape or promote a preliminary claim.

Capture valuable operational material in its existing workflow record before
removing it from Content. Fix corresponding current Aims and outline addresses
together. Do not delete, rename or archive paper files as a side effect of a
skill-only change; any explicitly requested cleanup is a separate scoped action.
Do not recreate deleted child planning pages or compatibility registries. A live Page migration uses the Page workflow and its
rendering checks; a skill test can instead draft the proposed revision in a
temporary fixture, explicitly unapproved.
