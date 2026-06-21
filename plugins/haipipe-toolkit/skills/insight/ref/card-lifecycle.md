Insight Card Lifecycle Policy
=============================

This file defines how insight cards evolve after they are created.

The core rule:

```text
Card IDs are stable. Evidence evolves.
```

Do not create a new card every time a new experiment, source, or ask session
touches the same reusable knowledge unit. Prefer `merge` / `update` when the
new material strengthens, weakens, or clarifies the same unit. Create a new
card only when the new material is a different unit or supersedes the old one.


Lifecycle Actions
=================

```text
file       create a new card
merge      add new evidence to an existing card without changing the core claim
update     revise metadata/body wording while preserving the same card identity
supersede  create a new card that replaces an old active card
stale      mark a card as no longer action-relevant but not false
skip       do not archive; explain why
blocked    cannot decide yet; missing evidence or ambiguous scope
```


When To Merge
=============

Use `merge` when new material supports the same reusable unit.

Examples:

```text
New task result confirms D01's same observation     -> merge into D01
New D card reinforces I03's same pattern            -> merge into I03
New probe supports K04's same scoped belief         -> merge into K04
New ask session cites W02 but does not change action -> update ref_by only
```

Merge updates may change:

- `updated`
- `sources`
- `ref_by`
- evidence bullets / evidence table
- confidence rationale, if the same claim becomes stronger or weaker
- caveats / counter-evidence
- `## Change log`

Merge updates must NOT silently change:

- the card's core `claim` / `rec` / `pattern` / `headline`
- the scope from one unit into a broader unit
- the card id


When To Update
==============

Use `update` for same-card maintenance:

- add `ref_by` from a narrative/application/paper
- correct a typo or stale title
- clarify scope wording without changing the underlying claim
- mark `status: stale` for an old W whose action window passed
- improve metadata/tags for retrieval

Every meaningful update should append a `## Change log` entry.


When To Supersede
=================

Use `supersede` when the old card's core unit is no longer the right
knowledge unit.

Examples:

```text
K04 says "FiLM helps OOD"; new judged probe refutes it
  -> create K09 negative belief, mark K04 superseded_by: K09

W02 recommends "run param-matched FiLM"; the experiment has been run
and a different next action is now needed
  -> mark W02 acted_on or stale, create W05 if a new action exists

I03 describes a pattern that a new batch systematically reverses
  -> create I07 for the new pattern; mark I03 superseded/contested
```

Supersede does not delete. It preserves history and the citation trail.


Card Body Change Log
====================

Every card SHOULD end with a small change log.

```markdown
## Change log
- 2026-06-20 — created from probe:P.0619_film_ood.
- 2026-06-24 — merged task:T.A01.04; confidence stayed medium because OOD caveat remains.
- 2026-07-02 — superseded by K09 after probe:P.0701_param_matched refuted the original scope.
```

Rules:

- One line per meaningful change.
- Mention the source ref or card id that caused the change.
- Explain whether the update changed confidence, scope, status, or action.
- Do not paste raw logs. Keep the trail readable.


Frontmatter Fields
==================

Cards MAY include these fields when relevant:

```yaml
status: active | stale | superseded | contested | acted_on
supersedes: [K02]
superseded_by: K09
merged_from: [task:T.A01.04, probe:P.0701_param_matched]
```

Use body `## Change log` for human-readable history. Use frontmatter only for
machine routing.


INSIGHT_REVIEW.yaml Fields
===================

For non-`file` actions, `candidate_cards[]` SHOULD include:

```yaml
candidate_id: C7
action: merge
target: K04
sources: [probe:P.0701_param_matched]
reason: "same scoped claim; new evidence changes confidence but not identity"
change:
  kind: evidence_added | confidence_changed | scope_changed | status_changed | ref_added
  summary: "adds param-matched OOD evidence; confidence medium -> low"
  append_change_log: true
```

For supersede:

```yaml
candidate_id: C8
action: supersede
target: K04
replacement_layer: K
replacement_title: "FiLM validation gains do not establish OOD transfer"
sources: [probe:P.0701_param_matched]
reason: "new judged probe refutes K04's original scope"
change:
  kind: superseded
  summary: "mark K04 superseded_by:<new K>; create replacement K"
  append_change_log: true
```


Reviewer Gate
=============

Reviewers should fail or block lifecycle updates when:

- `merge` changes the core claim/action so much that it should be `supersede`
- `file` duplicates an active card and should be `merge`
- `update` changes evidence without a `## Change log`
- `supersede` deletes or hides the old card instead of linking it
- status changes are not explained

When in doubt:

```text
same unit + more evidence        -> merge
same unit + wording/metadata     -> update
old unit false or wrong scope    -> supersede
different unit                   -> file
not reusable                     -> skip
```
