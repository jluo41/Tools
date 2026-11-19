# Paper Story integration with Page, work, Sections, and Compile

Read this reference for an actual migration, workflow handoff, Section
binding, or compile-order edit. The eight Content divisions and their semantic
meaning live only in `../SKILL.md`; routers resolve that contract directly.

On the ladder a telling feeds each version: its seed, roadmaps and §8 Section
Narrative stay on its Story topic, and its research questions are Board Questions
with reports. §8 owns what every version shares: title, story, explanation and the
claims C1..Cn with their numbers, and no per-Section rows. Each writing version's
`## Narrative` holds that venue's layout (claims to displays, display Runs, one row
per Section, compile order); it points at §8 and copies no claim. Story and Displays read the same Story topic; they do not create a
second argument source. Older Boards retain their existing Story Page bindings.

## Page and workflow records

The shared Page shell remains Opening → Outline → Content → Aims. Outline
plans the telling's content; §6/§7 describe the paper's research plan.
Do not mistake those two levels of planning for each other.

G0–G5 are owned by `haipipe-paper-workflow`. Existing human selection,
release, settlement and Section-release records stay in the Story's
`draft/records/` log and the shared `workflow/` receipts, using their existing
schemas. Work owners keep job/run state, budgets, commands and accepted
Results. §6/§7 may link those records; §5 summarizes their evidential meaning.
Preserve every existing receipt during a content revision. No Story row,
CHECK pass or requested edit constitutes a new execution release.

On returned evidence: read the Result and its limitations, update the §5
proposition and §3 answer as justified, then revise affected §6/§7 needs and
§8 claims, then the affected version rows. A halted run is not a null result. A null result
is not automatically evidence of no relationship. Receipt acceptance and
claim support are different decisions.

New drafts can describe unavailable evidence and proposed Sections. CHECK
judges whether those plans and uncertainties are adequately described; it
does not require completion of the study. Existing approved Page artifacts
remain historical; a changed structure gets a new unapproved v0.x draft.

## Section rows

The version face's `## Narrative` rows own reader question, ordered moves,
the claims each Section carries (by id), display allocation, entry/exit,
transitions and cut rules; §8 holds none of them (JL 261111). The compact
section-map projection must agree with those rows. Keep the shared
Outline presenter and its supported projection mechanism; do not hand-copy a
generated table into the Page's Outline.

A planned row can exist before its Section Page. Once instantiated, retain its
exact `section-id`, target/category, Story version and `story-row:` binding.
Resolve the shared argument by claim id within §8. Ladder Section bindings use
`story-row:` anchors to the writing version's rows. Preserve these anchors and
reconcile those rows with §8's claims; update an anchor only as part of the
affected Page's authorized revision. An older Board whose §8 still holds Section
rows keeps them until that version is next touched, then they move to its face. This distinction does not migrate or rename existing records.

Section-local paragraph detail may elaborate the Story's ordered moves but
cannot change its central claim, evidential limit or reader transition. A
version row or §8 that moved since a sign is one quiet note on the version Job while Sections draft, a WARN at the
final gate, never a Section FAIL or a re-sign (must-check M-D09; `page.py sync-narrative`, then one sign). The selected
Venue contract supplies the desk rules, not new research findings.

## Compile projection

Use the existing compiler marker syntax for the currently selected Section
order:

```text
<!-- haipipe:compile-order:start -->
main:
- t00_abstract
- t01_introduction
appendix:
- t21_variables
<!-- haipipe:compile-order:end -->
```

These ids illustrate the format only; emit only the paper's actual Section ids.
On the ladder the block lives in the writing version's `## Narrative` and is
derived from its Section rows, aligned with the selected Story's Section Narrative claims.
Before Section files exist, keep their intended reader order in
`s04-paper-workflow/` (haipipe-paper-plan) without inventing compilable paths.
Before assembly, require an unambiguous selected target and real Section ids
consistent with `delivery/paper-build.toml`. Use one active marker block;
additional candidate Section orders stay in `s04-paper-workflow/` until a target is selected or the
declared builder explicitly supports target-qualified selection. Do not
promise multiple identical marker blocks to a single-block parser.

`haipipe-paper-assemble` owns build configuration, fragments, bibliography,
manifests and DRAFT/ready checks. A content-layout correction preserves an
existing valid compile block and its Section identities. Assembly does not
approve the Story skill, a Story outline, work releases, or submission.

## Existing Story migration

Inspect the current Page, outline, Aims, accepted sources and any unmerged
source content before editing. Map source/proposition/boundary content into
§5, external inquiries into §6, study evidence plans into §7, and claims,
argument and reader journey into §8, and Section plans into the version face's
`## Narrative`. Retain Seed identity and
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
