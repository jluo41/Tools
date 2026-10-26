---
name: haipipe-draft-review
description: "The judge of prose and of a built Page, never of its own text. Mode 1 reviews any text (plain English, rubric, anti-AI, humanizer evaluators, sentence-by-sentence logic) and returns located findings; Mode 2 is the Page check gate (CLOSE, CONTEXT, OUTLINE, EVIDENCE, CONTENT or HOLD). Trigger: review prose, too AI, humanize, plain English check, page check, quality gate, /haipipe-draft-review, /haipipe-writing, /haipipe-draft-check."
metadata:
  version: "0.4.0"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
---

# /haipipe-draft-review · judge prose, never write it

This skill replaces two older ones: the evaluate side of `haipipe-writing` and the
Page gate `haipipe-draft-check`. The drafting side of `haipipe-writing` now lives in
`haipipe-draft-writing` (`../haipipe-draft-writing/ref/writing.md`). `/haipipe-writing` and
`/haipipe-draft-check` still reach this skill as trigger words; if the request is to
write or revise, go to `haipipe-draft-writing`.

## 🚨 Highest-priority rule · independence

```text
writer ──▶ candidate ──▶ reviewer (a different actor) ──▶ findings ──▶ writer fixes
   ❌ the reviewer edits the text         ❌ the writer reviews its own text
```

- This skill **never edits** the text it judges. No rewrite, no "small fix", no
  auto-fix command. It returns located findings and the smallest suggested fix; the
  owner of the text applies it, under `haipipe-draft-writing`.
- **Whoever wrote a text never reviews it.** A model that drafted a passage and then
  loads this skill in the same context is doing self-review; label it `self`, and it
  cannot CLOSE a Page or count as independent. For an independent review, run it in a
  fresh context or another actor (for a Page, `haipipe-draft-check-agent`).
- Token checks, scores and the audit scripts are diagnostics. They cannot prove
  meaning kept, facts true, independent review or human acceptance.
- Preserve the author's claims, causal strength, numbers, citations, terms, qualifiers
  and comments in every suggested fix; send content or evidence problems to their
  owner instead of fixing them through style. Academic voice keeps evidence-tied
  hedging and legitimate passive voice.

## Two modes

```text
1  prose review    any text  ──▶ rubric + rules + audit + evaluator ──▶ findings
2  page check      one built Page version ──▶ gate ──▶ CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

1. **Prose review** takes a Page Section or Paragraph, a file, or plain text with no
   Page at all (an email, a paragraph pasted in chat). No Run or Page is needed.
2. **Page check** judges the BUILT deliverable of a Board Page and names its next
   authority. The full contract is [ref/page-check.md](ref/page-check.md); read it
   before judging a Page. It uses mode 1's rubric as its base.

## Mode 1 · prose review

Apply [ref/evaluation.md](ref/evaluation.md) and the shared
[base rubric](ref/evaluation-rubric.md): Mechanics, Function, Evidence and
Readability, with resolved host, venue and user criteria. Record actual spans,
evidence, verdicts and the smallest fixes. A local edit checks its protected
meaning and affected seam; a Section also checks coverage and argument across
paragraphs. Do not turn a local check into a whole-Page review.

0. **Sentence by sentence logic**: [ref/sentence-logic.md](ref/sentence-logic.md). For a paragraph or a Section,
   every sentence is read in its context and gets its own line: its link to the sentence before (the relation, and
   carried, weak or broken), whether every pointer and every setup's payoff hold, the specific problem, a logic
   score and a read score out of 10, and the rewrite when it is below 8. It runs first, because a sentence that
   does not follow cannot be fixed by its words (JL 261021: "每句话都要看一下上下文，review 它的逻辑关系是否通顺").
1. **Plain rules**: [ref/plain-rules.md](ref/plain-rules.md), including the semicolon
   rule. The test is whether a reader who does not read English well can follow it.
2. **AI tells**: [ref/ai-tells.md](ref/ai-tells.md) says how a machine writes. When
   someone says "too AI", report the concrete span and failure (generic setup,
   inflated importance, repeated syntax, empty transition, unsupported framing,
   restatement). Do not use a word blacklist or promise undetectability.
3. **Anti-slop audit** (read-only, run when the request or Ticket selects it):

   ```bash
   python3 cli/anti_slop.py audit <file> --format json
   python3 cli/anti_slop.py compare --before <old.md> --after <new.md> --check-facts --format json
   python3 cli/score.py <file>            # house-word counts; add --headings for headings only
   ```

   Adapter and provenance: [ref/anti-slop-adapter.md](ref/anti-slop-adapter.md),
   [ref/anti-slop-attribution.md](ref/anti-slop-attribution.md). A finding routes to the
   writer for a bounded revision; it is not an AI detector or an acceptance threshold.
4. **Evaluators by register**: pick one per candidate, never both.
   `_parts/academic-humanizer/` for papers, theses, rebuttals and proposals;
   `_parts/humanizer/` for general register. Upstream both are rewriters; here
   they return findings only (adapters: [ref/methods/](ref/methods/)). Every other
   anti-AI skill is read, not called: [ref/external/README.md](ref/external/README.md).
5. **Style input**: `_parts/writing-dna-skill/` distills an author corpus into a
   frozen Writing DNA. It is an input the writer applies and the reviewer checks
   against, never a fact source. Selection and trace:
   [ref/method-adapter-contract.md](ref/method-adapter-contract.md) and the catalog
   [ref/writing-methods.yaml](ref/writing-methods.yaml). A required missing method
   blocks; an optional one is visibly skipped. No method is selected by default.

Return `ready-for-review`, `needs-work` or `blocked` with the unresolved findings;
readiness never means human-accepted or CHECK-passed. When the candidate changes
after review, the verdict does not transfer. If a wording problem is really a plan,
evidence or promise problem, say so and name the owner.

The request shape (candidate, baseline, requirements, methods) is the same envelope
the writer uses: `../haipipe-draft-writing/ref/writing-request.md`, mode `evaluate`.

## Mode 2 · page check

Read [ref/page-check.md](ref/page-check.md). In short: read-only on the judged version;
judge the built PDF or docx, not only the Markdown; the actor that produced a version
may not be its checker; only `verdict: pass` may route to CLOSE.

## Checking the tools

```text
cli/anti_slop.py audit FILE   what exact AI-tell spans need a second look?
cli/score.py       FILE       how many house words, and where? (floor, not proof)
cli/holes.py       FILE       does every placeholder in ONE file have a real owner?
cli/agree.py       DIR...     do two statements of one fact agree (version, cited path)?
tests/test_anti_slop.py       rule and scanner regression tests
```

Run the tests with `python -m pytest -q tests` from this folder. The round trip of the
change record (`wdiff.py`) is tested in `haipipe-draft/tests/test_wdiff_roundtrip.py`.

## 📎 Files

```text
haipipe-draft-review/
├── SKILL.md                  the two modes and the independence rule
├── CHANGELOG.md              version history (older history in ref/history/)
├── ref/
│   ├── page-check.md         mode 2: the Page check gate
│   ├── sentence-logic.md     each sentence in context: link, pointers, setup and payoff, logic and read scores
│   ├── plain-rules.md        the plain-English rules and the ruling behind each
│   ├── ai-tells.md           how a machine writes
│   ├── evaluation.md · evaluation-rubric.md   the bounded review cycle and base-v1 rubric
│   ├── anti-slop-adapter.md · anti-slop-rules.json · anti-slop-attribution.md
│   ├── method-adapter-contract.md · writing-methods.yaml · method-attribution.md
│   ├── methods/              the two evaluator adapters
│   ├── external/README.md    the anti-AI writing shelf: what we call, what we only read
│   └── history/              changelogs of haipipe-writing and haipipe-draft-check
├── cli/                      anti_slop.py · score.py · holes.py · agree.py (all read-only)
├── tests/                    test_anti_slop.py
├── _parts/writing-dna-skill/            vendored style input
└── _parts/academic-humanizer/ · humanizer/   vendored evaluators
```

## 🚧 What this skill does NOT own

Drafting, revising, weaving, the change record and `wdiff.py` are `haipipe-draft-writing`
(`ref/`). The plan, the evidence, the venue and final acceptance belong to the
host workflow; a Page's human gate belongs to a person. Authority for what a Page
must say comes from its Page Face owner.
