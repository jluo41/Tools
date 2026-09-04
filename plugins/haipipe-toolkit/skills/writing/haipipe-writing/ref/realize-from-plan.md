# Realize prose from an approved plan

Read this reference when a writing worker receives an approved outline,
narrative row, section handoff, or division writing ticket together with ready
evidence. It defines how to turn that input into prose without creating a
second plan or evidence system.

## 1. Boundary

The host workflow owns the plan and evidence. Realization owns the prose that
implements them.

The approved plan is authoritative for:

- the reader question and the section or paragraph job;
- the order of claims and planned moves;
- what the section must establish and what it must refuse;
- the handoff to the next section.

The bound Evidence Results are authoritative for factual material. A related
link, an unlanded result, a remembered number, or a plausible transition is not
evidence.

Realization may choose wording, sentence shape, explanation, content-bearing
hinges, and rhythm. It may not silently:

- add, delete, reorder, broaden, or narrow a planned claim;
- create a number, citation, example, causal link, or factual explanation;
- change the Evidence Item contract or edit the approved outline in place;
- turn a missing input into fluent prose.

If the requested prose cannot be written under these rules, route to the owner:

```text
argument / section job / promise is wrong     → OUTLINE
evidence missing, stale, or unsuitable        → EVIDENCE
context, requirement, or venue is unresolved  → CONTEXT / HOLD
prose realization needs work                  → CONTENT
final built version needs judgment            → CHECK
```

## 2. Temporary writing packet

Build this packet from the host's existing records. Do not save a second copy as
an authority unless the host already requires a writing-run receipt.

```text
address:        section, division, or paragraph address
reader_job:     the question this unit answers
paragraph_job:  the one job this paragraph performs
planned_move:   the approved order of explanation
claims:         stable claim ids and their exact propositions
evidence:       folded Evidence Result ids and source pointers
must_establish: what the reader should understand at exit
must_not_say:   unlicensed scope, causal, or generality extensions
handoff:        what the next unit may assume
requirements:   venue, host, language, and formatting rules
voice:          optional author or team profile
```

The packet is complete only when the worker can answer both questions:

1. Is there enough material to write without inventing facts?
2. Is the unit's message specific enough to write in one sentence?

Failure of the first question routes to EVIDENCE. Failure of the second routes
to OUTLINE or the host's planning owner. Do not compensate with a generic
introduction or defensive caveat.

## 3. The realization pass

### 3.1 Shape from the existing plan

Read the plan row, claim system, argument arc, and evidence allocation as one
input. A logic graph is useful here as a read-only projection:

```text
reader question → paragraph job → claim → evidence → reader exit
```

Use the graph to find an uncovered claim, an orphaned Evidence Result, a broken
handoff, or a promise with no support. Do not generate a competing outline from
the graph. A graph finding routes to the authority that owns the broken edge.

### 3.2 Choose a small recipe

Select only the moves that serve this unit. A reliable default is:

```text
point → evidence → interpretation or consequence → handoff
```

Possible optional moves include:

- lead with the assigned point rather than setup about the writing;
- place evidence beside the claim it supports;
- explain a technical term at first use when the reader needs it;
- use a content-bearing hinge rather than a bare “Moreover” or “Furthermore”;
- vary sentence length while keeping one idea per sentence;
- remove empty intensifiers and generic self-defense.

Do not apply every available rule. A recipe is a small, reviewable choice, not a
new universal style law.

### 3.3 Apply voice and surface rules

An optional Writing DNA profile calibrates language, paragraph rhythm, and
recurring structural choices. It never supplies facts from its source corpus.
The priority order is:

```text
explicit user request
  > approved outline/evidence and venue contract
  > paragraph job and claim strength
  > author/team voice profile
  > readability and de-template rules
```

For paper or technical prose, use the structure-before-surface idea only as a
discourse check after the approved argument is fixed. Do not apply narrative
rules that would break scientific reader order or causal meaning.

### 3.4 Write and trace

Write the complete unit, then check it against the packet. For a revision, pass
the old and new prose to `cli/wdiff.py`; the model does not hand-author the
word-level record. For a first draft, keep the plan/evidence addresses in the
host writing receipt so the realization remains reviewable.

## 4. Final audit

Before promoting the prose, confirm:

- every planned job and required claim is covered;
- every factual claim maps to the named Evidence Result or declared static source;
- no number, citation, defined term, display reference, or causal qualifier was
  changed without authority;
- the verb strength does not exceed the evidence strength;
- every unresolved hole has an owner;
- the paragraph still hands the promised understanding to the next unit;
- each added sentence has a reader, a job, or a required disclosure.

The last test is the sentence-consumer test: if deleting a sentence changes no
reader decision, interpretation, or required record, drop or tighten it. Keep a
limitation, uncertainty, or disclosure when the reader must use it to interpret
the evidence or make a decision.

## 5. Method provenance

This is a local synthesis, not a runtime dependency. The ideas are deliberately
kept at the level each method can support:

| Method | Local use |
|---|---|
| paper-logic-graph | read-only claim/evidence/reader-flow projection |
| Compound Writing | readiness gate and small recipe selection |
| writing-dna-skill | optional author-owned voice profile |
| sepia | discourse and surface de-templating after content shape is fixed |
| Stop That Shit Slop | sentence-consumer test and task-boundary reminder |

These methods do not call one another, add dependencies, or gain authority over
the host's outline and evidence. `haipipe-writing` remains self-contained; the
host decides when this reference applies.
