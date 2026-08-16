---
name: haipipe-writing
description: >-
  The WRITING verb: take prose someone already wrote and make it readable by a person whose English is weak, recording every edit as a word-level change under the sentence it changed. Not a style guide and not a spec: it rewrites, and it leaves a trail a reviewer can read. Use it on any authored prose in the repo, a board page, a SKILL.md, a README, an application section; it is host-agnostic and knows where to put its records. Three verbs, two of them deterministic code: `score` ranks what is worth rewriting, `rewrite` changes prose and anchors a `✎` record per sentence, `check` audits the records. Trigger: rewrite this, make this readable, too long, sounds like AI, plain English, weak English reader, change record, word-level diff, ✎, /haipipe-writing.
metadata:
  version: "0.6.1"
  last_updated: "2026-08-02"
  summary: "cli/agree.py compares two statements of one fact, because the three defects of 260802 were all that shape; tests/test_roundtrip.py locks in the apply-versus-check repair, which no grep could have seen."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-writing · rewrite prose, and leave a trail

Prose in this repo is written by someone who already knows the subject.
That is the problem this skill exists for: the author cannot see their own jargon, and a long sentence reads as precise to the person who built it.
So the reader who pays is the one who knows least, and nobody in the room is that reader.

**What this skill is FOR**: rewriting authored prose so a person whose English is weak can follow it, and recording each edit next to the sentence it changed.

## 🧭 1 · What it does, in one picture

**The loop**: three verbs, and only the middle one needs judgment.

```
📄 authored prose
      |
      | 1️⃣ score.py         🤖 CODE · ranks what is worth rewriting
      v
📋 a ranked worklist ── a person reads it, nothing has changed yet
      |
      | 2️⃣ rewrite          🧠 JUDGMENT · the only step a model does
      v
✍️ new prose + old prose
      |
      | 3️⃣ wdiff.py apply   🤖 CODE · computes the diff, anchors the record
      v
📝 prose + ✎ record under the sentence it changed
      |
      | 4️⃣ wdiff.py check   🤖 CODE · every record well-formed and anchored
      v
✅ readable, and reviewable
```

🔒 the JUDGMENT is step 2, and ONLY step 2
🚫 a model never writes the diff and never places the record

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
cli/agree.py       DIR...   do TWO files stating one fact agree?
tests/test_roundtrip.py     does what `apply` writes, `check` accept?
```

`agree.py` exists because three defects surfaced on 260802 in one afternoon and all three were one shape: two halves of a contract, stating one fact, disagreeing, with nothing comparing them. It compares the two that are static, a declared version against its changelog and a cited path against the disk. The third was a round trip, which no grep can see, so it is a test instead.

⚠️ It is a FLOOR, not a proof. It checks the two disagreements that have actually bitten, and it stays quiet about path-shaped nouns a skill merely describes, such as `results/` or `1-probes/`, because a checker that cries wolf stops being read.

## 🚧 8 · What this does NOT own

`haipipe-paper-revise-humanizer` rewrites ACADEMIC prose for a venue: it keeps scholarly precision, evidence-tied claims, and a journal's voice, and it writes `%%` comments into LaTeX.
This skill has a different reader (someone whose English is weak) and a different host (any file).
They share machinery. They do not share judgment.
So the machinery moved here and the judgment stayed there (JL 260801).
This skill now holds the general AI-tell catalogue and the weaving method.
The humanizer calls `cli/wdiff.py` for its diffs instead of writing them by hand.
What stayed in `paper/` is everything a venue owns.
How loudly a paper may claim, how it cites, which gates a claim must pass, how a funding proposal sounds, and the `%%` comment grammar LaTeX needs.
`ref/change-record.md` §3 is where the two host dialects are written down together, so they cannot drift into two ideas.
