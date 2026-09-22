---
name: haipipe-writing
description: >-
  Draft, revise or evaluate scoped prose, including Page Section/Paragraph
  candidates and standalone files. Preserve the author's meaning and edit
  boundary, select requested writing/style/evaluation methods, and review the
  candidate against a shared rubric. Use for outline-to-prose, plain English,
  academic voice, humanize, writing feedback and prose evaluation.
  Page owns planning, Run state and acceptance. Trigger: /haipipe-writing.
metadata:
  version: "0.22.0"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-writing · draft, revise and evaluate prose

Prose in this repo is written by someone who already knows the subject.
That is the starting point for both paths: an approved plan still needs prose,
and an existing draft still needs a reader-facing pass. The author cannot see
their own jargon, and a long sentence reads as precise to the person who built it.

**What this skill is FOR**: realizing an approved plan/evidence slice as prose,
revising authored prose for its intended reader, or evaluating a candidate.
Return genuine changes and located findings in the host's record format.

The plan and evidence remain owned by the host workflow. This skill owns prose
realization, readability, evaluation and change trace; it does not create a competing
outline, evidence ledger, or claim authority.

## 🚨 Highest-priority rule · surgical revision

When prose already exists, **preservation is the default**. Treat the person's
request as an edit boundary, not as permission to regenerate the passage. A
request to revise a word, clause, sentence, transition, Bullet, or named
paragraph authorizes only that target and the smallest seam needed to keep it
grammatical. It never authorizes a fresh draft of the surrounding text.

Before editing, name the boundary from the person's words, then:

- freeze every untouched claim, logical relation, order, example, citation,
  hedge, term, voice choice, and paragraph function;
- make the smallest viable patch inside the named boundary;
- change an adjacent transition only when the target cannot work without that
  seam, and disclose that extra change;
- report broader problems as suggestions without fixing them unless the person
  explicitly expands the scope.

Never turn a local wording request into paragraph reorganization, argument
replacement, example substitution, claim expansion or contraction, or a
general style pass. Rewrite or restructure a paragraph or section only when
the person explicitly requests that scope. When scope is ambiguous, choose the
smaller edit. Afterward, compare before and after and confirm that everything
outside the declared boundary stayed unchanged. The existing draft is
cumulative author work, not raw material for regeneration.

## Run invocation and selected methods

A Workflow is a list of Runs. Page Section and Paragraph Runs commission this
same worker with different scopes. Read [ref/writing-request.md](ref/writing-request.md)
for the shared input/return contract. Reuse the current Run/Version/Step;
reading, drafting, evaluating, revising and tool calls are internal actions.
Standalone file work needs no Page or Run allocation.

The owning agent loads the skill and executes the scoped request; a YAML
worker name is not an automatic model launcher. Page saves the returned
candidate, changes, evaluation and unresolved findings in its existing record.
Use clean Before/After for Page review, with the presenter computing the visual
diff. Other hosts use their declared recording contract.

When a method is selected, load [ref/method-adapter-contract.md](ref/method-adapter-contract.md)
and only the selected method's catalog entry. The default catalog is
[ref/writing-methods.yaml](ref/writing-methods.yaml); an explicit project catalog
uses the same contract.
Roles are writer, style and evaluator. External skills provide candidates,
style choices or findings under the shared scope/preservation rules; they
cannot change authoritative plans, Evidence, Page acceptance or delivery.
Freeze the actual entry/version/hash in the host's effective packet. A required
unavailable method blocks; an optional one is visibly skipped. No method is
selected by default. An explicitly supplied DNA or anti-slop packet selects
its existing adapter once.

The external skills this worker can call are vendored beside it, one numbered
folder per role: `../1_style/writing-dna-skill/` (the Writing DNA distiller)
and `../2_evaluate/academic-humanizer/`, `../2_evaluate/humanizer/` (the two
evaluators: academic register, general register). Pick one evaluator per
candidate by register, never both. Every other anti-AI writing skill is read,
not called: [ref/external/README.md](ref/external/README.md) says what each is
and what of it already lives in `ref/anti-slop-rules.json` and `ref/ai-tells.md`.

## Evaluate before returning

Apply [ref/evaluation.md](ref/evaluation.md) and the shared
[base rubric](ref/evaluation-rubric.md): Mechanics, Function, Evidence and
Readability, with resolved host/venue/user criteria. Record actual spans,
evidence, verdicts and the smallest fixes. A local edit checks its protected
meaning and affected seam; a Section draft also checks coverage and argument
across paragraphs. Do not turn a local check into a whole-Page review.
Host-specific overlays, such as the Paper submission-readiness `SUB-*` rows,
reuse this rubric and remain scoped to the host's requested artifact.

Default: candidate → evaluate → at most one authorized revision pass →
evaluate the revised candidate → return. The request can set another bounded
revision budget. Stop on missing required inputs or no progress and report
remaining findings. In evaluate mode, report without editing. No-op feedback
creates no change card or invented second review pass.

Self-review is labeled as such, including when it uses an external method.
Token checks and style scores are diagnostics. They cannot prove semantic
equivalence, factual truth, independent review or human acceptance. Preserve
claims, causal strength, numbers, citations, terms, qualifiers and comments;
return content/evidence decisions to their owner instead of fixing them through
style. Academic voice retains evidence-tied hedging and legitimate passive voice.

## 🤝 Interactive Page writing

When the host is a collaborative Page Writing Run, load
`../../page/haipipe-page-workflow/ref/interactive-writing-run.md`.
The host saves original feedback and the Step result; this worker owns the
requested prose patch, not Run allocation, human acceptance or publication.

SHAPE's candidate preview may be written before approval/evidence completion.
State every unsupported slot explicitly; never treat a placeholder as evidence.
Work from either the sentence or its Bullet, returning dependent plan changes
to SHAPE. A Section uses one functional Bullet per sentence. Give each feedback
item a disposition and concrete reason; preserve its original text separately
from interpretation. Do not turn `applied` into `accepted`.

Use the existing effective policy/exemplar packet for a local turn; do not
re-read the whole corpus, rescore the whole Page or run broad humanization
after every comment. Whole-passage review happens when requested or at a
checkpoint. For each prose-changing Step, save clean Before/After text and its
local reason. Use `wdiff.py` only where the host requires its record format;
Page's presenter computes its own visual changes. For a Step with no prose
change, record only the disposition and reason. Never inject diff apparatus
into a preview sentence field that permits prose only.
For material Page-hosted wording feedback, return the requested change type and
the local editing reason to the host. During a record-first interactive Page
Step, do not infer a broader preference or build a taxonomy; the host records
`Analysis status: deferred` and post-run analysis handles that work after the
Page Run closes. A different host may explicitly request a provisional,
Page-local preference inference, but that is not part of the default Page Step.
The host, not this worker, stores and presents any such field. For feedback
that changes no prose, return no Before/After or preference card; the host
records the ordinary disposition.

On a Page handoff, the host's
`haipipe-page/ref/user-check-packet.md` controls the full-paragraph return and
three final Draft Space, Evidence Space, and Current Run links. No
chat-only polishing, implicit acceptance, or silent rewrite of accepted/out-of-scope
paragraphs.

For a follow-up local feedback turn, follow the host's rapid foreground mode:
reuse the loaded context, inspect only the target sentence and its dependent
Bullet, make the smallest viable patch, and return after the narrow check. Do
not rescore the Page, reread the whole corpus, infer a broader preference, or
perform optional export and review work before the person sees the updated
candidate. Record the local editing reason; the host performs post-run
preference analysis only after explicit Page Run closure.

The rapid foreground target is under two minutes. Do not create or wait for a
sub-agent, update plan metadata for a wording-only change, or widen the read
when the named target and current Run record are available. If they are not
available, return the missing record as one blocker instead of searching the
whole repository.

When the host is between interactive Steps or Runs, do not start optional
builds, exports, broad checks, delegated Task Runs, or sub-agent analysis on
your own. Return the scoped action and wait for the host's explicit approval.

## ✍️ Default Page writing style

For Page paragraph realization, use a concrete-before-polished register unless
the resolved Page Face owner, venue, or frozen Context supplies a narrower
policy. Start with the real subject and a reader-relevant verb; keep one main
reader move per sentence; use specific nouns and verbs; vary rhythm without a
formula; and preserve the exact claim strength, uncertainty, numbers, and
citation boundary. Keep process instructions in the Ticket or Outline, never
in the manuscript. In particular, do not write “this paragraph discusses,”
“the following section,” “it is important to note,” or planner commands such as
“explain,” “show,” and “introduce” as visible prose.

When someone says “too AI,” report the concrete span and failure (generic
setup, inflated importance, repeated syntax, empty transition, unsupported
framing, or restatement). Repair that span in context; do not use a word
blacklist, invent an author's voice, or promise undetectability. A missing
required style policy or approved exemplar routes to CONTEXT/HOLD.

## 🧭 1 · What it does, in one picture

Two input paths share the same scoped writing and evaluation contract:

```
approved plan + evidence OR existing prose + bounded request
  → candidate → rubric review → authorized revision → final review
  → host saves candidate + evaluation + genuine change record
```

The writer judges meaning and readability. Tools compute the host's visual
diff or durable change record; a model never hand-authors word-level marks.

## 🧩 Outline/evidence-aware realization

This section is the approved/publication realization path; interactive SHAPE
rehearsal uses the bounded candidate path above. Use this path when the host
has an approved plan, outline, narrative row, or
division writing ticket and the evidence it names is ready. Read
[`ref/realize-from-plan.md`](ref/realize-from-plan.md) before writing. It turns
the host's existing plan/evidence fields into a temporary writing packet; the
packet is a view of existing authority, not a new artifact that can override it.

The realization worker:

1. Confirms that the addressed plan slice has one reader job, a bounded
   paragraph/section move, and all evidence needed for its factual claims.
2. Reads the exact folded Evidence Results and the host's requirements or venue
   policy. It does not treat a related link, a plausible fact, or an unfinished
   Run as evidence.
3. Writes the planned job in reader order. It may choose sentence shape,
   explanation, a content-bearing hinge, and paragraph rhythm; it may not add,
   reorder, broaden, or silently weaken the approved argument.
4. Applies optional voice and surface rules only after the content job is
   stable. A style profile changes how the assigned material is expressed, not
   which facts or claims are present.
5. If the Ticket names the HAI anti-slop adapter, runs its read-only audit
   after the candidate exists. It reports exact spans and structure signals;
   it does not rewrite, gate acceptance, or decide that text is human.
6. Audits coverage, claim/evidence fit, protected numbers and citations, holes,
   and introduced AI tells. If the problem is the plan, evidence, or promise,
   route back to the owning authority instead of repairing it in prose.

For a Page-changing host response, return the direct Draft Space
(`&lens=div`) and Evidence Space (`&lens=evidence`) links from
the same verified public Board URL using the host's user-check packet. A
compact Page link or embedded Evidence iframe is secondary and never a
substitute for those direct workspace views.

For a first draft, the host receipt traces realization; no fake Before/After.
For a revision in a host using `✎`, `wdiff.py` computes that record. Page
feedback stores clean text and uses its existing presenter.

### 🧬 Writing DNA is a frozen Run input

When the host commissions one paragraph, read
[`ref/writing-dna-adapter.md`](ref/writing-dna-adapter.md) if a Writing DNA
profile is supplied. The profile is a versioned style input, not a source of
facts or a second outline. Prepare the paragraph in three passes:

1. **Map content**: bind the reader job and each planned Bullet to its folded
   Evidence Result, adjacent seam, and handoff.
2. **Draft truthfully**: write the assigned point, evidence, interpretation,
   and handoff in the approved order; the paragraph must work with style
   removed.
3. **Render and audit style**: apply observable language, rhythm, and
   structure choices from the frozen DNA packet, then record the artifacts,
   selected raw exemplars, applied choices, and any conflicts in `trace.md`.

If the profile would require a new fact, citation, number, example, claim, or
reader-order change, keep the higher-authority content contract and record the
conflict. A named style without its required profile or exemplars routes to
CONTEXT/HOLD; an optional unspecified voice does not block the Run.

### 🧹 Anti-slop is a post-draft diagnostic

The external anti-slop references are combined through the HAI adapter in
[`ref/anti-slop-adapter.md`](ref/anti-slop-adapter.md). The adapter carries
forward two useful pieces of code: a rules-as-data scanner with transparent
pattern/structure signals, and a preservation-sensitive fact comparison for a
before/after rewrite. Its rules and provenance are in
`ref/anti-slop-rules.json` and `ref/anti-slop-attribution.md`.

Run it only when the current Ticket or revision request selects the adapter:

```bash
python3 cli/anti_slop.py audit <result>/paragraph.md --format json \
  > <result>/anti-slop.json
python3 cli/anti_slop.py compare --before <old.md> --after <new.md> \
  --check-facts --format json
```

The report is a diagnostic Result artifact. A finding routes to CONTENT for a
bounded revision; it is not an AI detector, an undetectability promise, or an
acceptance threshold. If a revision changes prose, run the fact comparison,
then use the host's recording contract (`wdiff.py` for `✎`, clean Before/After
for Page Steps). Do not use an external auto-fix command or edit the Page
directly from this audit.

## ⚖️ 2 · Why the diff is code

**The three mistakes**: each was made twice in one evening, by an author who knew the rule.

```
❌ record appended at the end of a block   ──▶ attaches to the WRONG sentence
❌ diff written as one whole sentence      ──▶ shows nothing that survived
❌ heading names the MECHANISM             ──▶ reads as jargon

✅ wdiff.py apply    anchors under the FIRST new line, by position
✅ difflib           marks only the words that moved
✅ score.py --headings   ranks headings for review (headings only)
```

This is the whole design argument.
A model asked to "show the diff" writes a whole-sentence swap, because that is what a diff feels like from the inside.
It also appends the record wherever it finished writing, which quietly attaches it to a sentence it does not describe.
Both happened on `QB4` on 260801, twice each.
So neither is left to judgment: `cli/wdiff.py` computes the diff with `difflib` and inserts the record by position.

## 📐 3 · The rules it applies

They are not invented here. They were ruled by JL while rewriting `QB4` and they live in full in `ref/plain-rules.md`; this is the short form.

**The test**: can a reader who does not read English well follow this? That is harder than "is it correct", and it is the one that catches what correctness misses.

- Prefer a common word when it preserves the exact meaning; keep defined technical terms. ✅ `settles a decision` ❌ `argues one choice to a close`
- A heading names its CONSEQUENCE, not its mechanism. ✅ `A blank line decides what people see` ❌ `The opening paragraph ends at the first blank line`
- One reader move per sentence. Inspect long sentences; split only when meaning and the host's sentence/Bullet mapping permit it.
- A word this repo invented is explained where it is used, or it is not used.
- A good/bad pair gets its own line, marked ✅ and ❌, never buried in a sentence.

## 🧾 4 · The change record

**The grammar**: one line, under the sentence it changed. `ref/change-record.md` is the full contract.

```
> ✎ ~removed words~ *added words* · WHO · YYMMDD HHMM

  ~old~     renders struck through      *new*   renders inserted
  plain     words that SURVIVED         ← the reason this is word-level
```

⚑ it anchors to the SENTENCE its lane run sits under, not to the line directly
   above, because a record joins the END of a run that may already hold lanes
🔀 a rewrite that splits one sentence into three anchors on the FIRST

**Two hosts, one computation** (`--host`, 0.5.0): same difflib opcodes, two notations.

```
--host board   (default)  > ✎ ~old~ *new* · WHO · YYMMDD HHMM
--host paper              > Note: ~~old~~ **new** · WHO · WHEN
```

`check` validates Board `✎` records only. It does not validate legacy Paper
Notes; zero reported problems is not proof those Notes were checked. Page
candidates use clean Before/After and its presenter. Pass the actual author
label and host timestamp explicitly when generating a record.

🚫 the caller never converts the marks by hand. That was the arrangement until
   0.5.0, and it put a hand step inside the one tool built because this exact
   class of hand step gets done wrong.

## 📎 5 · Files

### Engines
- `cli/wdiff.py`
  Computes the word-level diff and anchors the record. `record`, `apply`, `check`.
- `cli/score.py`
  Ranks prose for review. `python3 cli/score.py FILE` checks body text;
  `python3 cli/score.py FILE --headings` checks headings only. Neither proves clarity.
- `cli/holes.py`
  Audits placeholders both ways: unowned holes, and holes pointing at an owner that does not exist. Read-only.
- `cli/anti_slop.py`
  Audits exact AI-tell spans and transparent structure signals, and compares
  preservation-sensitive fact tokens across a rewrite. Read-only.
- `cli/agree.py`
  Two statements of one fact, compared: a skill's declared version against its changelog, and every cross-skill path citation against what is on disk. Read-only.
  `python3 cli/agree.py --all --quiet <skills-root>`

### Contracts
- `ref/plain-rules.md`
  The rules, with the ruling that produced each one.
- `ref/change-record.md`
  The `✎` grammar, the anchoring law, and how a non-board host records a change.
- `ref/ai-tells.md`
  How a machine writes, in any register. Migrated 260801 out of the paper humanizer's Layer 1, which no paper owned.
- `ref/weaving.md`
  Paragraph-to-paragraph arc, hinges, and rhythm within the host's approved scope.
- `ref/holes.md`
  What to do about what you do not know: never invent, every hole names an owner, sweep after writing. Migrated 260801 out of the paper DRAFT phase.
- `ref/realize-from-plan.md`
  How to realize an approved outline/evidence slice without creating a second
  plan, claim ledger, or evidence authority; includes the recipe and routing
  rules for optional style methods.
- `ref/writing-dna-adapter.md`
  The adapter for the external `writing-dna-skill`: its frozen paragraph-Run
  packet, three-pass realization method, conflict rules, and style trace.
- `ref/anti-slop-adapter.md`
  The optional post-draft audit seam between external anti-slop references and
  a HAI Paragraph Run.
- `ref/anti-slop-rules.json`
  Versioned rules-as-data used by `cli/anti_slop.py`.
- `ref/anti-slop-attribution.md`
  Provenance and license notices for adapted MIT-licensed material.
- `ref/writing-request.md`
  Shared Section/paragraph/file request, protected meaning and return contract.
- `ref/method-adapter-contract.md`, `ref/writing-methods.yaml`
  Resolve selected capabilities, permissions, inputs, outputs and method trace.
- `ref/methods/academic-humanizer.md`, `ref/methods/humanizer.md`
  The two evaluator adapters: academic register, general register.
- `ref/external/README.md`
  The anti-AI writing shelf: what we call, what we only read, what was taken from each.
- `../1_style/writing-dna-skill/` · `../2_evaluate/academic-humanizer/` · `../2_evaluate/humanizer/`
  The vendored external skills, each with its LICENSE and a CHANGELOG stamping the upstream commit.
- `ref/evaluation.md`, `ref/evaluation-rubric.md`
  Bounded self-review and the common criteria also used by Page CHECK.
- `ref/method-attribution.md`
  Provenance and notice for the retained academic pattern material.

## 🔗 6 · It plugs into an apparatus that already exists

A `>` line under a sentence belongs to that sentence. `page/haipipe-sentence`
owns that contract, and `QB4 §3.3.3` names its three kinds: eight ⚑ typed lanes, a
💬 comment, and the ✎ change record this skill writes.

**This skill owns one lane out of ten, and none of the machinery around it.**
The lanes, the evidence card, and the archive-and-restore lifecycle are not
redefined here. Three of their rules bind it directly:

- a lane is APPENDED, never edited in place
- a signed `> WHO:` or `> ✎` line is NEVER erased; it is the durable review trail
- a lane with no signature is not a lane

`cli/wdiff.py apply` enforces all three. It appends to the end of the lane run,
it refuses to rewrite a lane, and it refuses to write a result holding fewer `✎`
lines than it started with.

## 🧪 7 · Checking it

**Read-only checks** answer different questions; the rubric supplies semantic review.

```
cli/wdiff.py check FILE     are Board ✎ records well-formed and anchored?
cli/holes.py       FILE     does every hole in ONE file have a real owner?
cli/anti_slop.py audit FILE what exact AI-tell spans need a second look?
cli/agree.py       DIR...   do TWO files stating one fact agree?
tests/test_roundtrip.py     does what `apply` writes, `check` accept?
```

`agree.py` exists because three defects surfaced on 260802 in one afternoon and all three were one shape: two halves of a contract, stating one fact, disagreeing, with nothing comparing them. It compares the two that are static, a declared version against its changelog and a cited path against the disk. The third was a round trip, which no grep can see, so it is a test instead.

⚠️ It is a FLOOR, not a proof. It checks the two disagreements that have actually bitten, and it stays quiet about path-shaped nouns a skill merely describes, such as `results/` or `outline/evidence/`, because a checker that cries wolf stops being read.

## 🚧 8 · What this does NOT own

The plan-aware path does not own OUTLINE, EVIDENCE, venue selection, or final
acceptance. A failed plan/evidence gate routes backward to its authority; it is
not hidden by a fluent paragraph.

Writing is the common entry point for general and academic prose. Paper/Page
supplies venue, content and source-of-record authority. Selected external
methods add bounded capabilities through adapters. Writing protects scientific
meaning and reports its review; the host owns acceptance and publication.

The standalone HAI humanizer was retired in 0.20.0. Its retained provenance is
in `ref/method-attribution.md`; an actual external academic-humanizer may be
selected through the method catalog. `ref/change-record.md` §4 documents the
legacy Paper notation and its checking limitation.
