---
name: haipipe-writing
description: >-
  The WRITING verb: co-draft scoped Page candidates with human feedback, turn
  an approved outline and evidence packet into readable
  prose, or revise prose someone already wrote for a weak-English reader,
  recording every edit as a word-level change under the sentence it changed.
  The core operations are `score`, `audit`, `rewrite`, and `check`; plan-aware
  realization is an input path, not a second planning authority. Trigger:
  write from an outline, draft from evidence, rewrite this, make this readable,
  too long, sounds like AI, plain English, ✎, /haipipe-writing.
metadata:
  version: "0.12.0"
  last_updated: "2026-09-11"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-writing · realize or rewrite prose, and leave a trail

Prose in this repo is written by someone who already knows the subject.
That is the starting point for both paths: an approved plan still needs prose,
and an existing draft still needs a reader-facing pass. The author cannot see
their own jargon, and a long sentence reads as precise to the person who built it.

**What this skill is FOR**: realizing an approved plan/evidence slice as prose,
or rewriting authored prose so a person whose English is weak can follow it,
and recording each edit next to the sentence it changed.

The plan and evidence remain owned by the host workflow. This skill owns prose
realization, readability, and its `✎` trail; it does not create a competing
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

## 🤝 Interactive Page writing

When the host is a collaborative Page Writing Run, load
`../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md`.
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
checkpoint. Record genuine wording changes with the existing `wdiff.py`
adapter where its host format supports it; the Step's before/after text and
reasons are always required. Never inject diff apparatus into a preview
sentence field that permits prose only.

On a Page handoff, the host's
`haipipe-page/ref/user-check-packet.md` controls the full-paragraph return and
two final Workspace links. No chat-only polishing, implicit acceptance, or
silent rewrite of accepted/out-of-scope paragraphs.

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

**The loop**: two input paths share one writing and checking contract. Only the
candidate prose needs judgment; code computes the worklist, records the diff,
and audits the result.

```
🧭 approved outline + folded evidence ──► paragraph/section contract
📄 authored prose ──────────────────────► ranked worklist
                         \\
                          \\
                           ▼
                 1️⃣ realize or rewrite  🧠 JUDGMENT
                           |
                           ▼
                    ✍️ candidate prose
      |
      | 2️⃣ wdiff.py apply   🤖 CODE · computes the diff, anchors the record
      v
📝 prose + ✎ record under the sentence it changed
      |
      | 3️⃣ wdiff.py check   🤖 CODE · every record well-formed and anchored
      v
✅ readable, and reviewable
```

🔒 the JUDGMENT is the realization/rewrite step, and ONLY that step
🚫 a model never writes the diff and never places the record

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
   route back to the owning phase instead of repairing it in prose.

For a Page-changing host response, return the direct Bullet Workspace
(`&lens=div`) and Evidence Workspace (`&lens=workspace&seg=items`) links from
the same verified public Board URL using the host's user-check packet. A
compact Page link or embedded Evidence iframe is secondary and never a
substitute for those direct workspace views.

For a first draft, the writing run/host receipt is the trace of realization. For
a revision of existing prose, `wdiff.py` is the only writer of the word-level
`✎` record.

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
then let `wdiff.py` compute and place the `✎` record. Do not use an external
auto-fix command or edit the Page directly from this audit.

## ⚖️ 2 · Why the diff is code

**The three mistakes**: each was made twice in one evening, by an author who knew the rule.

```
❌ record appended at the end of a block   ──▶ attaches to the WRONG sentence
❌ diff written as one whole sentence      ──▶ shows nothing that survived
❌ heading names the MECHANISM             ──▶ reads as jargon

✅ wdiff.py apply    anchors under the FIRST new line, by position
✅ difflib           marks only the words that moved
✅ score.py          flags a heading before anyone reads it
```

This is the whole design argument.
A model asked to "show the diff" writes a whole-sentence swap, because that is what a diff feels like from the inside.
It also appends the record wherever it finished writing, which quietly attaches it to a sentence it does not describe.
Both happened on `QB4` on 260801, twice each.
So neither is left to judgment: `cli/wdiff.py` computes the diff with `difflib` and inserts the record by position.

## 📐 3 · The rules it applies

They are not invented here. They were ruled by JL while rewriting `QB4` and they live in full in `ref/plain-rules.md`; this is the short form.

**The test**: can a reader who does not read English well follow this? That is harder than "is it correct", and it is the one that catches what correctness misses.

- A shorter common word always beats a precise rare one. ✅ `settles a decision` ❌ `argues one choice to a close`
- A heading names its CONSEQUENCE, not its mechanism. ✅ `A blank line decides what people see` ❌ `The opening paragraph ends at the first blank line`
- One idea per sentence. A sentence past about 30 words is usually two.
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

🚫 the caller never converts the marks by hand. That was the arrangement until
   0.5.0, and it put a hand step inside the one tool built because this exact
   class of hand step gets done wrong.

## 📎 5 · Files

### Engines
- `cli/wdiff.py`
  Computes the word-level diff and anchors the record. `record`, `apply`, `check`.
- `cli/score.py`
  Ranks prose against the weak-English test. Read-only, and it never rewrites.
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
  Paragraph-to-paragraph arc, hinges, and rhythm. Migrated 260801 out of `haipipe-paper-revise-content`, which still owns when the pass runs.
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

## 🔗 6 · It plugs into an apparatus that already exists

A `>` line under a sentence belongs to that sentence. `board/haipipe-sentence`
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

**Three checkers, three questions**: none of them rewrites anything.

```
cli/wdiff.py check FILE     is every record well-formed and anchored?
cli/holes.py       FILE     does every hole in ONE file have a real owner?
cli/anti_slop.py   FILE     what exact AI-tell spans need a second look?
cli/agree.py       DIR...   do TWO files stating one fact agree?
tests/test_roundtrip.py     does what `apply` writes, `check` accept?
```

`agree.py` exists because three defects surfaced on 260802 in one afternoon and all three were one shape: two halves of a contract, stating one fact, disagreeing, with nothing comparing them. It compares the two that are static, a declared version against its changelog and a cited path against the disk. The third was a round trip, which no grep can see, so it is a test instead.

⚠️ It is a FLOOR, not a proof. It checks the two disagreements that have actually bitten, and it stays quiet about path-shaped nouns a skill merely describes, such as `results/` or `outline/evidence/`, because a checker that cries wolf stops being read.

## 🚧 8 · What this does NOT own

The plan-aware path does not own OUTLINE, EVIDENCE, venue selection, or final
acceptance. A failed plan/evidence gate routes backward to its authority; it is
not hidden by a fluent paragraph.

`haipipe-paper-revise-humanizer` rewrites ACADEMIC prose for a venue: it keeps scholarly precision, evidence-tied claims, and a journal's voice, and it writes `%%` comments into LaTeX.
This skill has a different reader (someone whose English is weak) and a different host (any file).
They share machinery. They do not share judgment.
So the machinery moved here and the judgment stayed there (JL 260801).
This skill now holds the general AI-tell catalogue and the weaving method.
The humanizer calls `cli/wdiff.py` for its diffs instead of writing them by hand.
What stayed in `paper/` is everything a venue owns.
How loudly a paper may claim, how it cites, which gates a claim must pass, how a funding proposal sounds, and the `%%` comment grammar LaTeX needs.
`ref/change-record.md` §3 is where the two host dialects are written down together, so they cannot drift into two ideas.
