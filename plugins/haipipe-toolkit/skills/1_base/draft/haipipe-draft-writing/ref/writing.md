# Writing prose · the rules, then realize, weave, revise, record

This is the writing step of `haipipe-draft`. Until 2026-10-16 it was the skill `haipipe-writing`; the judging half
(rules, anti-slop audit, rubric, humanizers, Page check) moved to `haipipe-draft-review`, and the writer never
reviews its own text there. Page owns planning, Run state and acceptance.

Prose in this repo is written by someone who already knows the subject.
That is the starting point for both paths: an approved plan still needs prose,
and an existing draft still needs a reader-facing pass. The author cannot see
their own jargon, and a long sentence reads as precise to the person who built it.

**What this step is FOR**: realizing an approved plan/evidence slice as prose, or
revising authored prose for its intended reader. Return genuine changes and the
change record in the host's format. A candidate you wrote is judged by
`haipipe-draft-review` (another actor), not by you; a self-check against the
rubric is allowed and is labeled self-review.

The plan and evidence remain owned by the host workflow. This step owns prose
realization, readability and change trace; it does not create a competing
outline, evidence ledger, or claim authority.

## 📚 0 · Examples first: read how the venue's papers write this Section

Before a Section is written, or rewritten whole, read how 3 to 4 published papers of the same venue write the same
Section, and write to follow them (JL 261022: "你应该先找 example，看看别人是怎么写 abstract 的，然后再看怎么写 ...
在 write 的时候，你应该先找到相应的 example，这样我们就可以 follow 别人的参考了").

1. **Find them.** The Section's examples are a Studio topic `sNN-<task>-<venue>-examples`, made by `/excalidraw read`:
   two papers close to the topic, two the venue's author guide quotes, each one's Section read whole (`reads/pNN-
   <author><year>/reading.yaml`, its blocks shot from the PDF). The Section canvas names it by `examples:`, and the
   workbench shows it as 📚 Examples in 1 · Plan and 2 · Write. With none, make it first; do not write without it.
2. **Read what they share.** For each paragraph (or each heading of a structured abstract): its move, the words that
   carry it, its length. One line each, kept in the topic face's `key:` and each reading's `logic:`; for example,
   "Importance · 30 to 38 words, 1 to 2 sentences, no number, why it matters, then 'but' or 'however'".
3. **Write to that pattern**, paragraph by paragraph, in our own words and facts; never copy their sentences.
4. **Name each departure** with its reason (an author's ruling, our design, a cap): "Question asks three, not one
   (R11)". A departure with no reason is a fix.

The examples set the shape a reader of the venue expects; the plan (§1) sets what we say. When they disagree, the plan
wins and the departure is named.

## 📏 The rules every sentence is written by

One list, kept in one place: `../../haipipe-draft-review/ref/plain-rules.md`. The writer writes by it and the reviewer
checks by the same page (`anti_slop.py` runs its machine-checkable rules), so the two can never disagree. Read it
before writing; its sections are:

1. **The test**: can a reader who does not read English well follow this?
2. **Words**: a common word when it keeps the exact meaning; no idiom; defined terms stay, explained.
3. **Sentences**: one reader move a sentence, split at the hinge; avoid semicolons where possible.
4. **Headings and shapes**: a heading names its consequence, not its mechanism; a good/bad pair gets ✅ and ❌ lines.
5. **The AI tells**: the stock shapes this repo has produced (the reversal flourish, a bolted-on "which is why", "not
   only … but also", the four-slot house skeleton), and the paste test.

The house style for a Page paragraph is below (`## ✍️ Default Page writing style`). A venue's or a Page's own rule
(its requirement record) is added on top, never instead.

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
same step with different scopes. Read [writing-request.md](writing-request.md)
for the shared input/return contract. Reuse the current Run/Version/Step;
reading, drafting, revising and tool calls are internal actions.
Standalone file work needs no Page or Run allocation.

The owning agent loads the skill and executes the scoped request; a YAML
worker name is not an automatic model launcher. Page saves the returned
candidate, changes and unresolved findings in its existing record.
Use clean Before/After for Page review, with the presenter computing the visual
diff. Other hosts use their declared recording contract.

When a method is selected, load
[the method adapter contract](../../haipipe-draft-review/ref/method-adapter-contract.md)
and only the selected method's catalog entry
(`../../haipipe-draft-review/ref/writing-methods.yaml`). The only method this step
applies itself is the style input (Writing DNA, [writing-dna-adapter.md](writing-dna-adapter.md));
evaluators (the two humanizers, anti-slop) belong to `haipipe-draft-review`.
No method is selected by default.

## 🤝 Interactive Page writing

When the host is a collaborative Page Writing Run, load
`../../haipipe-draft-workflow/ref/interactive-writing-run.md`.
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
`../../haipipe-draft/ref/user-check-packet.md` controls the full-paragraph return and
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
[`realize-from-plan.md`](realize-from-plan.md) before writing. It turns
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
5. If the Ticket names the HAI anti-slop adapter (`../../haipipe-draft-review/ref/anti-slop-adapter.md`), runs its read-only audit
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
[`writing-dna-adapter.md`](writing-dna-adapter.md) if a Writing DNA
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

## ⚖️ 2 · Why the diff is code

**The three mistakes**: each was made twice in one evening, by an author who knew the rule.

```
❌ record appended at the end of a block   ──▶ attaches to the WRONG sentence
❌ diff written as one whole sentence      ──▶ shows nothing that survived
❌ heading names the MECHANISM             ──▶ reads as jargon

✅ wdiff.py apply    anchors under the FIRST new line, by position
✅ difflib           marks only the words that moved
✅ haipipe-draft-review/cli/score.py --headings   ranks headings (review side)
```

This is the whole design argument.
A model asked to "show the diff" writes a whole-sentence swap, because that is what a diff feels like from the inside.
It also appends the record wherever it finished writing, which quietly attaches it to a sentence it does not describe.
Both happened on `QB4` on 260801, twice each.
So neither is left to judgment: `cli/wdiff.py` computes the diff with `difflib` and inserts the record by position.
## 🧾 3 · The change record

**The grammar**: one line, under the sentence it changed. `change-record.md` is the full contract.

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

## 📎 Files

### Engine
- `cli/wdiff.py` (in `haipipe-draft/cli/`)
  Computes the word-level diff and anchors the record. `record`, `apply`, `check`.
  Test: `tests/test_wdiff_roundtrip.py`.

### Contracts (this folder)
- `change-record.md`: the `✎` grammar, the anchoring law, and how a non-board host records a change.
- `weaving.md`: paragraph-to-paragraph arc, hinges, and rhythm within the host's approved scope.
- `holes.md`: what to do about what you do not know: never invent, every hole names an owner, sweep after writing.
- `realize-from-plan.md`: realize an approved outline/evidence slice without a second plan, claim ledger or evidence authority.
- `writing-dna-adapter.md`: the frozen paragraph-Run packet for a Writing DNA profile, three-pass method, conflict rules, style trace.
- `writing-request.md`: the shared Section/paragraph/file request, protected meaning and return contract.

### Used from `haipipe-draft-review`
- `../../haipipe-draft-review/ref/plain-rules.md`: the plain-English rules this step writes to.
- `../../haipipe-draft-review/cli/anti_slop.py audit`: the read-only post-draft diagnostic, when the Ticket selects it.
- `../../haipipe-draft-review/cli/holes.py`: the read-only placeholder audit that `holes.md` refers to.

## 🔗 4 · It plugs into an apparatus that already exists

A `>` line under a sentence belongs to that sentence. `1_base/draft/haipipe-draft-writing/ref/sentence.md`
owns that contract, and `QB4 §3.3.3` names its three kinds: nine ⚑ typed lanes, a
💬 comment, and the ✎ change record this skill writes.

**This step owns one lane out of eleven, and none of the machinery around it.**
The lanes, the evidence card, and the archive-and-restore lifecycle are not
redefined here. Three of their rules bind it directly:

- a lane is APPENDED, never edited in place
- a signed `> WHO:` or `> ✎` line is NEVER erased; it is the durable review trail
- a lane with no signature is not a lane

`cli/wdiff.py apply` enforces all three. It appends to the end of the lane run,
it refuses to rewrite a lane, and it refuses to write a result holding fewer `✎`
lines than it started with.

## 🚧 What this step does NOT own

It does not own OUTLINE, EVIDENCE, venue selection, or final acceptance. A failed
plan/evidence gate routes backward to its authority; it is not hidden by a fluent
paragraph. It does not judge: review, anti-AI audit, humanizing evaluation and the
Page check are `haipipe-draft-review`, by a different actor than the writer.
Paper/Page supplies venue, content and source-of-record authority; this step
protects scientific meaning and the host owns acceptance and publication.
`ref/change-record.md` §4 documents the legacy Paper notation and its checking limitation.
