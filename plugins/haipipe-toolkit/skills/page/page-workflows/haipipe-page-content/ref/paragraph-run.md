# Paragraph Writing Run · explicitly delegated / existing Results

For interactive human-feedback writing, use
`../../haipipe-page-workflow/ref/interactive-writing-run.md` instead. That
profile supports several paragraphs, Versions and feedback Steps under one
Run. This file remains the contract consumed by `promote_paragraph.py`; it
must not force a new Run per paragraph during adoption of agreed text.

CONTENT/WRITE commissions one paragraph, addressed `C<n>.P<m>`. The Page
Folder owns its Ticket; the Folder dialect resolves its Result. A paragraph
is the target, not a new hierarchy level. This profile owns the `.md` Ticket
dialect: a named worker reads and follows the Ticket rather than executing it
as shell code. An agent or explicitly commissioned human may be that worker.

## Files and identity

```text
runs/r02_page-writing_c01-p02.md
results/r02_page-writing_c01-p02/
├── paragraph.md
├── trace.md
└── runtime.yaml
```

The local filename uses zero-padded C/P numbers; `target: C1.P2` is the stable
plan address. Increment rNN monotonically across all local Run kinds. A
cross-Folder reference carries the owner's full Run identity or the Page path
plus local stem; it never identifies work by P2 alone. Paper identity fields
remain Paper-owned; this profile does not rename its evidence namespace.
Job-backed Results stay at the resolved `$OUTPUT_ROOT/results/<task>/<run>/`.
No scripts, separate prompt file, or parallel status ledger is required.

## One authored Ticket, including the prompt

Use this structure, replacing sample values with current addressed inputs.
The Ticket is a frozen commission derived from Context and Outline, not a
second plan. Retain the referenced content in versioned storage or the Ticket
when its source is mutable; a hash without recoverable content is not enough.

```markdown
---
run: r02_page-writing_c01-p02
family: page
operation: paragraph-writing
target: C1.P2
page: <owning Page path>
result: results/r02_page-writing_c01-p02/
worker: haipipe-writing
---

## Inputs
- Context: <record path, version/hash; resolved requirements and style policy>
- Plan: <approved version/hash; C1.P2 job and B1..Bn>
- Evidence: <each Bullet's folded Item → full Local Run → Result path/hash>
- Current prose: <Page version/hash and this paragraph's prior text, if any>
- SHAPE preview: <outline/<stem>-preview.md addressed slice and frozen text/hash,
  or absent; candidate prose, not accepted Content>
- Continuity: <whole argument reference, previous accepted paragraph/version,
  next paragraph's approved job; use an explicit boundary for first/last>
- Narrative Decision: <Page Outline decision id/scope/summary/source for this
  paragraph's organization, or not specified>
- Style examples: <approved excerpt references/version, or not specified>
- Writing DNA: <frozen adapter packet with profile id/status/hash, five artifact
  refs, selected exemplars, target and shortfall count, and reason; or not
  applicable>
- Anti-slop audit: <HAI adapter version, rules path/hash, one selected
  reference from Tools/references/anti-ai-writing-skills.md, and threshold if
  any; or not applicable>
- Feedback/Decisions: <applicable record ids, attribution and exact ruling>

## Paragraph requirements
- Reader job: <one specific question or understanding this paragraph serves>
- Organization decision: <how the declared Narrative Decision fixes the
  paragraph's reader order/form, or not specified; do not invent one>
- Must establish: <the approved Bullet expectations, in order>
- Must not say: <claim-strength, scope and evidence boundaries>
- Form: <owner's length, sentence and citation requirements, or not specified>
- Voice: <concrete observations from the named policy/exemplars>
- Writing DNA application: <observable L1/L2/L3-L5/L6 choices and conflict rule>
- Anti-slop handling: <audit-only scope, or not applicable; never an
  undetectability promise>

## Prompt
Write only C1.P2 using the inputs above in three passes:

1. Map the reader job, each approved Bullet, its sentence slot, folded Evidence
   Result, declared Narrative Decision, neighboring seam, and handoff. Use the
   Decision to understand the approved organization, but do not create or
   rewrite one from raw feedback. If the job is unclear or support is missing—
   or the approved claim is stronger than its Evidence Result—report the
   specific gap and owning phase instead of drafting around it or silently
   weakening the claim.
2. Revise the supplied SHAPE candidate when present, or draft a neutral,
   evidence-bound paragraph in the approved order. Preserve useful reviewed
   wording and resolve candidate placeholders against the ready Evidence.
   Cover the
   assigned point, bound evidence, interpretation or consequence, and handoff;
   preserve numbers, citations, qualifiers, and claim strength. This pass must
   remain correct if all style inputs are removed.
3. Render the fixed paragraph with the named requirements and frozen Writing
   DNA packet. Apply only observable language, rhythm, and compatible structure
   choices. Do not take facts, quotations, citations, numbers, examples, or
   unsupported framing from style examples. If DNA conflicts with the content,
   evidence, venue, or reader-order contract, keep that contract and record the
   conflict.

Return one paragraph with the owner's sentence/trace notation and keep the
content map and style decisions recoverable in `trace.md`.

If the Ticket names the anti-slop adapter, run its read-only audit after Pass C
and record the JSON report in the Result. Treat findings as a bounded CONTENT
revision list. Do not invoke an external auto-fix command. If the revision
changes existing prose, compare the before/after fact tokens, then use
`wdiff.py` for the durable change record.

## Acceptance
Cover every target Bullet; trace every factual claim; preserve numbers,
citations and claim strength; meet the named style and paragraph requirements;
pass the neighboring-context check. Honor the declared Narrative Decision, or
record `not specified`; a Decision conflict routes to OUTLINE. Confirm the
approved claim strength is supported by the bound Evidence Results; otherwise
record an upstream block.
Make the Writing DNA profile identity,
version/hash, artifacts, exemplars, applied observations, and conflicts
recoverable in the trace. No unsupported final-mode placeholders.
When anti-slop is selected, keep its report beside the Result and treat its
score as diagnostic only; it is not an acceptance gate.

## Output
paragraph.md + trace.md + runtime.yaml, plus `anti-slop.json` when the Ticket
selects the adapter, at the resolved Result address.
```

Select the actual writing worker through the Page Face owner; `haipipe-writing`
is the reusable plan-aware worker, not a mandate to impose its plain-English
register on every journal. Applicable owner/venue/style requirements govern.

## Style is an input and a test

Shared style requirements remain in Context and its authoritative requirement
records. A Ticket references those and adds only the paragraph-specific slice.
Translate "too AI" into concrete findings: generic setup, unsupported
importance claims, repeated sentence/paragraph templates, empty transitions,
or unnecessary restatement. Check their effect in context, not a word blacklist.
When a named author's voice is requested, use identifiable, approved examples
and describe observable choices (directness, hedging, terminology, rhythm).
Never invent that person's preferences, approval, or feedback. If required
exemplars are missing, route CONTEXT/HOLD; an optional unspecified voice does
not block otherwise-authorized writing. No AI-detector score or promise of
undetectability is an acceptance criterion.

## Anti-slop is one optional post-draft audit

The HAI adapter lives at
`../../../../writing/haipipe-writing/ref/anti-slop-adapter.md` and the
executable is `../../../../writing/haipipe-writing/cli/anti_slop.py` relative
to this Page Content skill. A selected audit reads the final candidate after
content and Writing DNA rendering, masks code/frontmatter as configured, and
records exact spans plus transparent structure signals. It does not change
`paragraph.md`, `trace.md`, the Page, or the Run status.

The ten external anti-slop skills remain comparison sources. Select at most one
reference/rule profile per Run. A high score or finding does not mean the text
was generated by AI; it means the worker should inspect the named span in
context. If a revision is warranted, it is a new candidate under the same Run
before acceptance, or a new `supersedes` Run after acceptance. Preserve the
approved plan, Evidence, claim strength, citations, numbers, and seam.

## Result and promotion

`paragraph.md` contains exactly one prose paragraph in the owner's source
notation. One sentence per source line is allowed; do not mistake those lines
for different paragraphs. Keep headings, diagnostics, and alternatives out of
the paragraph body. Preserve existing required sentence addresses/change
records using the owner's tools; those annotations are not reader prose.

`trace.md` contains:

| Plan address | Sentence locator | Evidence Item → Local Result/hash | Finding |
|---|---|---|---|
| C1.P2.B1 | sentence 1 | exact bound Result, or declared none | covered / gap |

Then record the named requirements/style exemplars used, addressed feedback
decisions, the previous/next seam assessment, and `pass`, `revise`, or a named
upstream block with reasons. Missing evidence belongs to EVIDENCE; wrong
paragraph job/order/claim belongs to OUTLINE; unresolved policy belongs to
CONTEXT. Explicit draft-mode external gates follow the CONTENT skill's rule.

For the Page-owned organization choice, also record:

```markdown
## Narrative Decision

- Decision: <id, scope, summary, source, or not specified>
- Applied: <how it shaped the paragraph's reader order/form>
- Conflict: <none or route OUTLINE>
```

For a DNA-aware Run, add:

```markdown
## Style application

- Profile: <profile_id, status, and hash>
- Producer/source: <writing-dna-skill and profile path or reference>
- Distilled artifacts read: <integrated, language, structure, cognitive, visual>
- Raw exemplars read: <paths and why they match this paragraph>
- Raw exemplar shortfall: <0, or count not available>
- Applied observations: <concrete L1/L2/L3-L5/L6 choices>
- Conflicts and decisions: <higher-authority rule, or none>
- Style verdict: pass | revise | not-applicable
```

The DNA corpus is style-only and cannot support a new factual sentence.

Use `sentence 1`, `sentence 2`, and so on as the default sentence locators in
the table unless the Page Face owner declares a different source notation. Do
not infer an omitted word budget or sentence count; record `not specified`.

`runtime.yaml` follows `haipipe-run`: `run`, `family: page`,
`operation: paragraph-writing`, `target`, `ticket`, resolved `result`, frozen
`inputs` paths/hashes, worker, status, timestamps, attempts/failure and
`supersedes` when applicable. Create it as `planned` when allocating the Run;
unfinished and failed work must remain visible. Mark `complete` only after
the paragraph and trace pass the declared Result gate, never just because a
model returned text. The Runs presenter does not perform semantic acceptance.

CONTENT separately promotes only the addressed paragraph. Resolve it from the
owner's structural/sentence addresses, never a cached byte offset or a global
text replacement. Verify its current text and consumed context before writing;
hold on concurrent overlapping edits. Preserve sibling paragraphs and signed
records. The CONTENT receipt records Run/Result hash, paragraph address, and
Page before/after identity; Result completion alone is not promotion or CHECK.

The bundled promoter implements this write path:

```bash
python3 Tools/plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/cli/promote_paragraph.py \
  --page <page>/page.md \
  --result <page>/results/<RUNNAME> \
  --dry-run
```

Run the same command without `--dry-run` only after the preview is correct.
The runtime receipt must contain:

```yaml
family: page
operation: paragraph-writing
target: C1.P2
status: complete
inputs:
  - role: page-source
    path: page.md
    sha256: <hash read before the Run>
```

The promoter then:

1. locks the Page promotion path and recomputes the current Page hash;
2. resolves `## Content`, its direct `###` divisions, and either explicit
   `####` paragraph headings or blank-line prose blocks;
3. checks the Result target, trace, candidate grammar, frozen hash, and source
   span, refusing stale or annotation-bearing/structural writes;
4. records `promotion.status: applying`, atomically replaces only that span,
   verifies the resulting hash and target text, then records
   `promotion.status: promoted` with the before/after hashes and locator.

`paragraph.md` and `trace.md` remain the accepted Result; `anti-slop.json`, when
selected, is a diagnostic companion. Only the Run's `runtime.yaml` receives
the promotion lifecycle receipt. If a process stops after the
`applying` receipt, a later invocation recovers it only when the planned Page
hash and Result hash still agree. If the Page changed, promotion stops and a
new Run or explicit re-freeze is required. Promotion is not CHECK: the Page
receipt still records the promoted Run, and the independent CHECK phase judges
the resulting Page identity.

Draft/revision calls may stay inside one unfinished Run under unchanged target,
inputs and acceptance. A material change to any of those, or a revision after
acceptance, gets a new Run linked by `supersedes`. Never overwrite an accepted
Result. Retain historical division Runs as history without synthesizing new
paragraph Results from them.
