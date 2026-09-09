# Writing DNA adapter for paragraph realization

This reference defines the seam between the external
[`writing-dna-skill`](https://github.com/larashero3-dotcom/writing-dna-skill)
and a HAI Paragraph Writing Run.

The distiller turns an author's corpus into reusable style artifacts. The HAI
host still owns the Context, approved Outline, Evidence Items, venue contract,
and claim strength. `haipipe-writing` owns the prose realization and its trace.
The adapter carries style across that boundary without making style a second
source of facts or a second planning system.

## 1. Boundary

```text
Writing DNA Distiller   corpus → metadata + layered DNA + Writing-DNA.md
        │
        ▼ frozen profile/version/hash
HAI Paragraph Run       outline + evidence + neighbors → one paragraph
        │
        ▼
trace.md                 content coverage + evidence map + style application
```

- Distillation is an upstream operation. Do not re-distill the author's corpus
  inside every paragraph Run.
- A profile changes expression, paragraph rhythm, and compatible structural
  choices. It never supplies a number, citation, example, causal link, topic,
  or factual interpretation.
- The raw corpus remains project-owned and may be private. Do not copy source
  articles into this skill or a public repository.
- A profile is optional. If the user explicitly requests a named author's style
  and the required profile or exemplars are missing, route to CONTEXT/HOLD;
  an unspecified optional voice does not block writing.

## 2. The Writing DNA packet

The Paragraph Writing Ticket freezes the profile used by that Run. The external
skill does not define a HAI runtime schema, so the host records this compact
adapter envelope in the Ticket rather than inventing a new authority artifact.

```yaml
writing_dna:
  profile_id: <author-or-publication>/<profile-name>
  producer: writing-dna-skill
  source: <profile directory or repository reference>
  status: full                 # full | partial
  language: en                 # en | zh | mixed
  corpus:
    article_count: 20
    raw_root: <path or private>
    metadata_root: <path or private>
  artifacts:
    integrated: <path>/Writing-DNA.md
    language: <path>/language-dna.md
    structure: <path>/structure-patterns.md
    cognitive: <path>/cognitive-framework.md
    visual: <path>/visual-style-guide.md
  profile_hash: <sha256 or host identity>
  exemplars:
    - <raw article path/version>
    - <raw article path/version>
  selection:
    article_type: <matching type or not specified>
    topic_tags: [<matching tags>]
    raw_exemplar_target: 5
    raw_exemplar_shortfall: 0
    reason: <why these exemplars fit this paragraph>
```

`status: full` means the profile meets the distiller's corpus requirement
(at least 20 complete articles). A smaller corpus may be carried as
`partial`, with its lower confidence visible; it must not be described as a
stable author profile.

### Page-owned Narrative Decision

When the Page Outline declares one, the Paragraph Writing Ticket also freezes
the paragraph-level `Narrative Decision` that explains the approved reader
order or form. It is normally a projection of a human-resolved
Feedback/Discussion/Requirement decision; raw discussion is not itself a
decision. The field is Page/Outline-owned, not produced by the DNA distiller:

```yaml
narrative_decision:
  id: <D<nn> or not specified>
  scope: <C<n>.P<m>>
  summary: <approved reason for this paragraph's reader order/form>
  source: <Feedback/Discussion/Requirement/human ruling refs>
```

`Narrative Decision` answers “why is this paragraph organized this way?”; the
Writing DNA packet answers “which compatible surface choices help express it?”
Neither field supplies Evidence. If the Decision conflicts with the approved
Outline, reopen OUTLINE; do not let fluent prose or DNA silently choose a new
organization. If no decision is declared, record `not specified` rather than
inventing one from the prose.

For a normal writing Run, read all five distilled artifacts and five raw
articles closest to the target content type and topic. If fewer than five
relevant raw articles exist, record the shortfall. The raw articles calibrate
cadence and paragraph joins; they are not evidence for the new paragraph.

For a technical or academic Page, read all layers but constrain their use:
L1/L2/L6 may guide language, structure, and presentation; L3–L5 may be used
only when they agree with the approved argument. None may change the topic,
claim, evidence, or scientific reader order.

## 3. Prepare one paragraph

The worker prepares the paragraph in three passes. The first pass is content
work; the second is style work; the third is an audit. Do not blend them into
one vague instruction to “write in this style.”

### Pass A · Build the content map

Read the frozen Context, approved plan slice, folded Evidence Results, and
adjacent accepted paragraphs. Build an internal map with the same stable
addresses as the Ticket:

```text
reader job → Narrative Decision (if declared) → planned Bullet order
           → sentence slot → Evidence Result → exit/handoff
```

Confirm that the paragraph has one reader job and that every factual move has
an exact Evidence Item or declared static source, and that the approved claim
strength is supported by those Results. If the job is unclear, route to
OUTLINE. If support is missing or the approved proposition is stronger than
the evidence, route to OUTLINE/EVIDENCE. Do not silently weaken or strengthen
the approved claim, invent a Narrative Decision, or use Writing DNA to hide
either gap.

### Pass B · Draft the truthful paragraph

Write a neutral content pass in reader order:

```text
assigned point → bound evidence → interpretation/consequence → handoff
```

Use one sentence per planned Bullet for a Section Page unless the Page Face
owner declares another form. Preserve numbers, citations, qualifiers, and
claim strength. If the approved claim and the Evidence Result disagree on
strength, stop with an upstream block rather than repairing the mismatch in
prose. At this stage, the paragraph must be correct even if the style profile
is removed.

### Pass C · Render the style

Read the frozen Writing DNA packet and apply only compatible observations:

- L1: preferred vocabulary, sentence rhythm, punctuation, and language mix;
- L2: an article/paragraph shape that fits this content type;
- L3–L5: compatible emphasis or framing, never new subject matter or facts;
- L6: only when the Page Face owns visual or display choices.

Then reread the paragraph against the content map. If a DNA rule would require
adding a fact, changing a claim, moving evidence out of reader order, or
breaking a venue rule, do not force the prose to fit. Record the conflict and
keep the higher-authority form.

After this render, a Paragraph Run may select the separate HAI anti-slop
adapter for a read-only surface audit. It is not another DNA layer: it cannot
change the profile, select a new voice, or write a replacement. Any resulting
revision remains subordinate to the content map and goes through `wdiff.py`.

## 4. Priority and conflict handling

The worker uses two different responses for two kinds of conflict:

```text
content / evidence / venue conflict
  → stop and route to the owning authority

surface / voice conflict under a fixed content contract
  → follow the explicit user or venue instruction, then use Writing DNA softly
```

For an unchanged paragraph commission, the effective order is:

```text
Context, discipline, and venue contract          HARD
approved Outline, Evidence, and claim strength   HARD
Page Narrative Decision, when declared            HARD
paragraph job and neighboring seam                HARD
explicit user request about surface or voice     STRONG
Writing DNA profile                               SOFT
readability and de-template checks                DIAGNOSTIC
```

An explicit request that changes the paragraph's topic, promise, claim order,
or evidence boundary is not a style override. It reopens the relevant owner
through CONTEXT, OUTLINE, or EVIDENCE.

## 5. Style trace in the Result

`trace.md` keeps the evidence trace and style trace separate. Add this section
after the plan-to-sentence table:

```markdown
## Style application

- Profile: <profile_id>
- Producer/source: <writing-dna-skill and path>
- Profile status: full | partial
- Profile hash: <hash>
- Distilled artifacts read: <five paths, versions, or not specified>
- Raw exemplars read: <selected paths and selection reason>
- Raw exemplar shortfall: <0, or count not available>
- Applied observations:
  - L1 language: <observable choices>
  - L2 structure: <observable choice or not applied>
  - L3-L5 framing: <compatible choice or not applied>
  - L6 visual: <choice or not applicable>
- Conflicts and decisions: <higher-authority rule that won, or none>
- Style verdict: pass | revise | not-applicable
```

“Sounds like the author” is not enough for a trace. Name observable choices:
directness, hedging, transition pattern, sentence-length variation, paragraph
shape, citation integration, or an equivalent concrete feature. Do not record
approval, preference, or a cognitive rule that the profile does not state.

## 6. Acceptance

A DNA-aware paragraph Result is ready only when:

- every planned Bullet is covered in order;
- any declared Narrative Decision is honored, and its id/scope/source are
  recoverable (or `not specified` is recorded);
- every factual sentence maps to its own bound Evidence Result or declared
  static source;
- the approved claim strength is supported by the bound Evidence Results, or
  the Result is an explicit upstream block;
- no fact, quotation, citation, number, or example came from the DNA corpus;
- the paragraph's form follows the Page Face and venue contract;
- the profile identity, version/hash, artifacts, and exemplars are recoverable;
- conflicts are recorded rather than silently resolved by fluent prose;
- the paragraph still hands the approved understanding to its next neighbor.

No AI-detector score, “undetectable” promise, or similarity percentage is a
style acceptance criterion.

## 7. Missing or partial profiles

```text
profile absent + voice optional       → write under venue/host rules
profile absent + named style required → CONTEXT/HOLD
profile partial                       → write cautiously; mark partial
profile changed after Ticket freeze   → new Run or supersedes, never silent refresh
```

The profile is an input to a Run, not a mutable global setting. A later
distillation produces a new profile identity and requires a new Run when it
materially changes the requested style.
