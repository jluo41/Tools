# Anti-slop adapter for a HAI Paragraph Run

This adapter is the controlled seam between the ten external anti-AI-writing
references in `Tools/references` and `haipipe-writing`. It adds a post-draft
diagnostic. It does not create a second writer, outline, evidence source, or
Page promotion path.

## The organic join

```text
approved Outline + folded Evidence + seam
                 │
                 ▼
       HAI content pass, reader order
                 │
                 ▼
       frozen Writing DNA render
                 │
                 ▼
       anti_slop.py audit  ·  read-only
                 │
       ┌─────────┴─────────┐
       │                   │
   no finding          bounded revision
       │                   │
       └─────────┬─────────┘
                 ▼
  compare facts when prose changed
                 │
                 ▼
  wdiff.py computes and records ✎
                 │
                 ▼
  trace.md + runtime.yaml + CONTENT promotion
```

The order matters. Anti-slop sees the paragraph after the content contract and
Writing DNA have done their work. If it suggests a change, the worker judges
that exact span against the evidence and voice. A score never decides whether
the paragraph is acceptable.

## The copied/adapted code

The active implementation is `cli/anti_slop.py` and its rules are
`ref/anti-slop-rules.json`.

| Capability | Carried from | HAI adaptation |
| --- | --- | --- |
| Rules as data and exact findings | `soundshuman/bin/sloplint.js` + `rules/slop-rules.json` | Python stdlib, line/column spans, HAI-local rule identity, no write mode |
| Pattern-density and structure signals | `soundshuman` and `humanizer-adam/cli/lib/metrics.js` | Stable `pattern_score` + `uniformity_score`; short-sample confidence remains visible |
| Fact preservation | `humanizer-adam/cli/lib/facts.js` plus HAI citation extension | URLs, emails, dates, percentages, versions, numbers, acronyms, citation tokens, and quoted terms; missing tokens are review findings |
| Preservation/density boundary | `slopkit` checks and the external anti-slop skills | Diagnostic guidance only; no detector claim, no automatic rewrite |

The full provenance and MIT notices are in
`ref/anti-slop-attribution.md`. The external repositories remain submodules so
their original files can be inspected and updated independently.

## Ticket input

The field is optional and is frozen when a Paragraph Run is commissioned:

```yaml
anti_slop:
  adapter: haipipe-writing/anti-slop
  rules: ref/anti-slop-rules.json
  rules_sha256: <hash>
  selected_reference: references/<one-source-name> | not-specified
  mode: audit
  ignore_quotes: false
  fail_above: null
```

`selected_reference` records which external material guided the human review;
it does not make that repository a runtime dependency. Use at most one selected
reference per Run; the source name must resolve through the ten-item map in
`Tools/references/anti-ai-writing-skills.md`. If no audit is requested, record
`not applicable` rather than silently running every reference.

## Result and trace

When selected, the worker writes:

```text
results/<RUNNAME>/
├── paragraph.md
├── trace.md
├── anti-slop.json       # diagnostic companion
└── runtime.yaml
```

`anti-slop.json` records the adapter, rules version/hash, input paragraph hash,
score, confidence, statistics, and exact findings. The report must not contain
the full prompt, private evidence, or raw corpus. `trace.md` adds:

```markdown
## Anti-slop audit

- Adapter: haipipe-writing/anti-slop · <version>
- Rules: <path> · <version/hash>
- Selected reference: <one source or not specified>
- Input: paragraph.md · <sha256>
- Report: anti-slop.json · <sha256>
- Findings: <count> · score <n>/100 · confidence <low|medium|high>
- Decision: <kept / bounded revision / routed upstream>
- Fact comparison: <not applicable / pass / review required>
- Limitation: diagnostic signal; not an AI-origin verdict or acceptance gate
```

If a candidate revision changes existing prose, run:

```bash
python3 <haipipe-writing>/cli/anti_slop.py compare \
  --before <old-paragraph.md> --after <paragraph.md> \
  --check-facts --format json
```

Then call `wdiff.py` with the old and new text. Never ask the audit tool to
apply a replacement: doing so would bypass the word-level `✎` record and the
Page Paragraph promotion guard.

## Routing

| Finding | Route |
| --- | --- |
| generic wording, empty transition, or a repeated surface pattern | CONTENT; inspect and revise only the addressed paragraph |
| missing number, URL, date, version, citation token, quote, or tracked acronym after revision | CONTENT; restore or route to EVIDENCE/OUTLINE if the source is unclear |
| proposed edit changes claim strength, evidence order, or reader job | OUTLINE or EVIDENCE; do not fix through humanization |
| named voice/profile is missing | CONTEXT/HOLD; anti-slop cannot substitute for Writing DNA |
| score is high only because of a legitimate domain term or short sample | record a false positive/limitation and keep the prose |

The adapter may be run again after a bounded revision. The Result remains
immutable after acceptance; a material post-acceptance change gets a new Run
with `supersedes`.
